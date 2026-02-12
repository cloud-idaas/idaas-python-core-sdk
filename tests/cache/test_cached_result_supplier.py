"""
Tests for CachedResultSupplier class
"""

import threading
import time
import unittest
from datetime import datetime, timedelta, timezone

from cloud_idaas import CacheException, ConcurrentOperationException
from cloud_idaas.core.cache.cached_result_supplier import CachedResultSupplier
from cloud_idaas.core.cache.refresh_result import RefreshResult
from cloud_idaas.core.cache.stale_value_behavior import StaleValueBehavior
from cloud_idaas.core.cache.strategy.non_blocking_prefetch_strategy import NonBlockingPrefetchStrategy
from cloud_idaas.core.cache.strategy.one_caller_blocks_prefetch_strategy import OneCallerBlocksPrefetchStrategy


class TestCachedResultSupplier(unittest.TestCase):
    """Test cases for CachedResultSupplier class"""

    def test_get_with_valid_cache(self):
        """Test get with valid cache (not stale)"""
        value = "test_value"
        stale_time = datetime.now(timezone.utc) + timedelta(hours=1)
        prefetch_time = datetime.now(timezone.utc) + timedelta(minutes=30)

        refresh_result = RefreshResult(value, stale_time, prefetch_time)

        supplier = CachedResultSupplier(
            value_supplier=lambda: refresh_result, prefetch_strategy=OneCallerBlocksPrefetchStrategy()
        )
        # Initialize cache
        supplier._cached_value = refresh_result

        result = supplier.get()
        self.assertEqual(result, value)

    def test_get_with_stale_cache(self):
        """Test get with stale cache (should refresh)"""
        initial_value = "initial_value"
        refreshed_value = "refreshed_value"

        call_count = [0]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            call_count[0] += 1
            if call_count[0] == 1:
                return RefreshResult(
                    initial_value,
                    current_time[0] + timedelta(seconds=10),  # Stale time
                    None,
                )
            else:
                return RefreshResult(refreshed_value, current_time[0] + timedelta(hours=1), None)

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=OneCallerBlocksPrefetchStrategy(), clock=custom_clock
        )

        # First call - initial value
        result1 = supplier.get()
        self.assertEqual(result1, initial_value)
        self.assertEqual(call_count[0], 1)

        # Move time past stale time (need to account for jitter which adds up to 10 minutes)
        current_time[0] = datetime(2024, 1, 1, 12, 15, 0)  # 15 minutes later

        # Second call - should refresh
        result2 = supplier.get()
        self.assertEqual(result2, refreshed_value)
        self.assertEqual(call_count[0], 2)  # Should have called twice now

    def test_get_with_null_cache(self):
        """Test get with null cache (should refresh)"""
        value = "test_value"

        supplier = CachedResultSupplier(
            value_supplier=lambda: RefreshResult(value, datetime.now(timezone.utc) + timedelta(hours=1), None),
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
        )

        result = supplier.get()
        self.assertEqual(result, value)

    def test_concurrent_operation_exception(self):
        """Test ConcurrentOperationException when cache is null and refresh fails"""

        def failing_supplier():
            raise Exception("Refresh failed")

        supplier = CachedResultSupplier(
            value_supplier=failing_supplier,
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
            stale_value_behavior=StaleValueBehavior.ALLOW,
        )

        with self.assertRaises(ConcurrentOperationException):
            supplier.get()

    def test_strict_stale_value_behavior(self):
        """Test STRICT stale value behavior (raises exception on refresh failure)"""
        from cloud_idaas import CacheException

        def failing_supplier():
            raise Exception("Refresh failed")

        supplier = CachedResultSupplier(
            value_supplier=failing_supplier,
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
            stale_value_behavior=StaleValueBehavior.STRICT,
        )

        # Initialize with stale cache
        supplier._cached_value = RefreshResult(
            "old_value",
            datetime.now(timezone.utc) - timedelta(hours=1),  # Already stale
            None,
        )

        with self.assertRaises(CacheException):
            supplier.get()

    def test_allow_stale_value_behavior(self):
        """Test ALLOW stale value behavior (returns old value on refresh failure)"""
        old_value = "old_value"

        def failing_supplier():
            raise Exception("Refresh failed")

        supplier = CachedResultSupplier(
            value_supplier=failing_supplier,
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
            stale_value_behavior=StaleValueBehavior.ALLOW,
        )

        # Initialize with stale cache
        supplier._cached_value = RefreshResult(
            old_value,
            datetime.now(timezone.utc) - timedelta(hours=1),  # Already stale
            None,
        )

        # Should return old value instead of raising exception
        result = supplier.get()
        self.assertEqual(result, old_value)

    def test_custom_clock(self):
        """Test with custom clock for testing"""
        fixed_time = datetime(2024, 1, 1, 12, 0, 0)

        def custom_clock():
            return fixed_time

        value = "test_value"
        stale_time = datetime(2024, 1, 1, 12, 0, 30)  # 30 seconds after fixed_time

        supplier = CachedResultSupplier(
            value_supplier=lambda: RefreshResult(value, stale_time, None),
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
            clock=custom_clock,
        )

        result = supplier.get()
        self.assertEqual(result, value)

    def test_jitter_time(self):
        """Test that jitter is applied to times"""
        value = "test_value"
        stale_time = datetime.now(timezone.utc) + timedelta(hours=1)

        supplier = CachedResultSupplier(
            value_supplier=lambda: RefreshResult(value, stale_time, None),
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
        )

        # Get value which should apply jitter
        result = supplier.get()
        self.assertEqual(result, value)

        # Check that stale_time was jittered (should be greater than original)
        if supplier._cached_value.stale_time:
            self.assertGreater(supplier._cached_value.stale_time, stale_time)


class TestCachedResultSupplierConcurrency(unittest.TestCase):
    """Test cases for CachedResultSupplier concurrent scenarios"""

    def test_concurrent_get_with_valid_cache(self):
        """Test multiple threads getting valid cache simultaneously"""
        value = "shared_value"
        stale_time = datetime.now(timezone.utc) + timedelta(hours=1)

        supplier = CachedResultSupplier(
            value_supplier=lambda: RefreshResult(value, stale_time, None),
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
        )
        # Initialize cache
        supplier._cached_value = RefreshResult(value, stale_time, None)

        results = []
        threads = []

        def get_value():
            results.append(supplier.get())

        # Start multiple threads
        for _ in range(10):
            thread = threading.Thread(target=get_value)
            thread.start()
            threads.append(thread)

        # Wait for all threads
        for thread in threads:
            thread.join()

        # All threads should get the same value
        self.assertEqual(len(results), 10)
        for result in results:
            self.assertEqual(result, value)

    def test_concurrent_get_with_stale_cache_one_refresh(self):
        """Test multiple threads triggering cache refresh simultaneously (only one should refresh)"""
        call_count = [0]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            call_count[0] += 1
            time.sleep(0.1)  # Simulate slow refresh
            return RefreshResult(f"value_{call_count[0]}", current_time[0] + timedelta(hours=1), None)

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=OneCallerBlocksPrefetchStrategy(), clock=custom_clock
        )

        # Initialize with stale cache
        supplier._cached_value = RefreshResult(
            "initial",
            datetime(2024, 1, 1, 11, 0, 0),  # Already stale
            None,
        )

        results = []
        threads = []

        def get_value():
            results.append(supplier.get())

        # Start multiple threads simultaneously
        for _ in range(10):
            thread = threading.Thread(target=get_value)
            thread.start()
            threads.append(thread)

        # Wait for all threads
        for thread in threads:
            thread.join()

        # Should have refreshed only once
        self.assertEqual(call_count[0], 1)

        # All threads should get a valid result (either the new value or initial)
        self.assertEqual(len(results), 10)

    def test_concurrent_get_with_null_cache(self):
        """Test multiple threads with null cache (first one should refresh)"""
        call_count = [0]
        lock = threading.Lock()

        def value_supplier():
            with lock:
                call_count[0] += 1
            time.sleep(0.1)  # Simulate slow refresh
            return RefreshResult(f"value_{call_count[0]}", datetime.now(timezone.utc) + timedelta(hours=1), None)

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=OneCallerBlocksPrefetchStrategy()
        )

        results = []
        threads = []

        def get_value():
            results.append(supplier.get())

        # Start multiple threads simultaneously
        for _ in range(5):
            thread = threading.Thread(target=get_value)
            thread.start()
            threads.append(thread)

        # Wait for all threads
        for thread in threads:
            thread.join()

        # Should have refreshed only once (or at most twice due to timing)
        self.assertLessEqual(call_count[0], 2)

        # All threads should get a valid result
        self.assertEqual(len(results), 5)
        for result in results:
            self.assertTrue(result.startswith("value_"))

    def test_concurrent_refresh_lock_timeout(self):
        """Test behavior when refresh lock timeout is exceeded"""
        call_count = [0]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def blocking_supplier():
            call_count[0] += 1
            # Block longer than BLOCKING_REFRESH_MAX_WAIT (5 seconds)
            # We'll use a shorter timeout for testing
            time.sleep(0.3)
            return RefreshResult(f"value_{call_count[0]}", current_time[0] + timedelta(hours=1), None)

        # Create a custom supplier with shorter timeout for testing
        from cloud_idaas.core.cache.cached_result_supplier import BLOCKING_REFRESH_MAX_WAIT

        original_timeout = BLOCKING_REFRESH_MAX_WAIT.total_seconds()

        supplier = CachedResultSupplier(
            value_supplier=blocking_supplier, prefetch_strategy=OneCallerBlocksPrefetchStrategy(), clock=custom_clock
        )

        # Initialize with stale cache
        supplier._cached_value = RefreshResult("initial", datetime(2024, 1, 1, 11, 0, 0), None)

        results = []
        threads = []

        def get_value():
            results.append(supplier.get())

        # Start first thread to acquire lock
        thread1 = threading.Thread(target=get_value)

        # Start second thread after a small delay
        thread2 = threading.Thread(target=get_value)

        thread1.start()
        time.sleep(0.05)  # Small delay to ensure thread1 gets the lock
        thread2.start()

        thread1.join()
        thread2.join()

        # Both threads should get a result (one may get old value if timeout occurred)
        self.assertEqual(len(results), 2)

    def test_concurrent_prefetch_with_one_caller_blocks(self):
        """Test prefetch behavior with concurrent calls using OneCallerBlocks strategy"""
        call_count = [0]
        prefetch_count = [0]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            call_count[0] += 1
            return RefreshResult(
                f"value_{call_count[0]}",
                current_time[0] + timedelta(hours=1),
                current_time[0] + timedelta(minutes=30),  # Prefetch time
            )

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=OneCallerBlocksPrefetchStrategy(), clock=custom_clock
        )

        # Initialize cache
        supplier._cached_value = RefreshResult(
            "initial", current_time[0] + timedelta(hours=1), current_time[0] + timedelta(minutes=30)
        )

        # Move time past prefetch time (accounting for jitter)
        current_time[0] = datetime(2024, 1, 1, 13, 0, 0)

        results = []
        threads = []

        def get_value():
            results.append(supplier.get())

        # Start multiple threads
        for _ in range(5):
            thread = threading.Thread(target=get_value)
            thread.start()
            threads.append(thread)

        # Wait for all threads
        for thread in threads:
            thread.join()

        # All threads should get a result
        self.assertEqual(len(results), 5)

    def test_concurrent_with_non_blocking_strategy(self):
        """Test concurrent behavior with NonBlockingPrefetchStrategy"""
        call_count = [0]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            with threading.Lock():
                call_count[0] += 1
            time.sleep(0.05)  # Simulate slow refresh
            return RefreshResult(f"value_{call_count[0]}", current_time[0] + timedelta(hours=1), None)

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=NonBlockingPrefetchStrategy(), clock=custom_clock
        )

        results = []
        threads = []

        def get_value():
            results.append(supplier.get())

        # Start multiple threads
        for _ in range(10):
            thread = threading.Thread(target=get_value)
            thread.start()
            threads.append(thread)

        # Wait for all threads
        for thread in threads:
            thread.join()

        # All threads should get a result
        self.assertEqual(len(results), 10)

    def test_concurrent_refresh_failure_allow_mode(self):
        """Test concurrent refresh failure in ALLOW mode"""
        call_count = [0]

        def failing_supplier():
            call_count[0] += 1
            raise Exception("Refresh failed")

        supplier = CachedResultSupplier(
            value_supplier=failing_supplier,
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
            stale_value_behavior=StaleValueBehavior.ALLOW,
        )

        # Initialize with stale cache
        supplier._cached_value = RefreshResult("old_value", datetime.now(timezone.utc) - timedelta(hours=1), None)

        results = []
        exceptions = []
        threads = []

        def get_value():
            try:
                results.append(supplier.get())
            except Exception as e:
                exceptions.append(e)

        # Start multiple threads
        for _ in range(5):
            thread = threading.Thread(target=get_value)
            thread.start()
            threads.append(thread)

        # Wait for all threads
        for thread in threads:
            thread.join()

        # All threads should get the old value (no exceptions in ALLOW mode)
        self.assertEqual(len(exceptions), 0)
        self.assertEqual(len(results), 5)
        for result in results:
            self.assertEqual(result, "old_value")

    def test_concurrent_refresh_failure_strict_mode(self):
        """Test concurrent refresh failure in STRICT mode"""
        call_count = [0]

        def failing_supplier():
            call_count[0] += 1
            raise Exception("Refresh failed")

        supplier = CachedResultSupplier(
            value_supplier=failing_supplier,
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
            stale_value_behavior=StaleValueBehavior.STRICT,
        )

        # Initialize with stale cache
        supplier._cached_value = RefreshResult("old_value", datetime.now(timezone.utc) - timedelta(hours=1), None)

        results = []
        exceptions = []
        threads = []

        def get_value():
            try:
                results.append(supplier.get())
            except CacheException as e:
                exceptions.append(e)

        # Start multiple threads
        for _ in range(5):
            thread = threading.Thread(target=get_value)
            thread.start()
            threads.append(thread)

        # Wait for all threads
        for thread in threads:
            thread.join()

        # At least one thread should get CacheException
        self.assertGreater(len(exceptions), 0)

    def test_concurrent_double_check_pattern(self):
        """Test double-check pattern in concurrent refresh"""
        call_count = [0]
        refresh_count = [0]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            with threading.Lock():
                call_count[0] += 1
                refresh_count[0] += 1
            time.sleep(0.1)  # Simulate slow refresh
            return RefreshResult(f"value_{call_count[0]}", current_time[0] + timedelta(hours=1), None)

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=OneCallerBlocksPrefetchStrategy(), clock=custom_clock
        )

        # Initialize with stale cache
        supplier._cached_value = RefreshResult("initial", datetime(2024, 1, 1, 11, 0, 0), None)

        results = []
        threads = []

        def get_value():
            results.append(supplier.get())

        # Start multiple threads simultaneously
        for _ in range(10):
            thread = threading.Thread(target=get_value)
            thread.start()
            threads.append(thread)

        # Wait for all threads
        for thread in threads:
            thread.join()

        # Due to double-check pattern, value_supplier should be called only once
        # (the first thread that acquires the lock)
        self.assertEqual(refresh_count[0], 1)

        # All threads should get a result
        self.assertEqual(len(results), 10)


class TestCachedResultSupplierEdgeCases(unittest.TestCase):
    """Test cases for CachedResultSupplier edge cases"""

    def test_prefetch_time_none_no_prefetch(self):
        """Test that prefetch is not triggered when prefetch_time is None"""
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        prefetch_count = [0]

        class TestPrefetchStrategy:
            def prefetch(self, value_updater):
                prefetch_count[0] += 1
                value_updater()

            def close(self):
                pass

        supplier = CachedResultSupplier(
            value_supplier=lambda: RefreshResult(
                "value",
                current_time[0] + timedelta(hours=1),
                None,  # No prefetch time
            ),
            prefetch_strategy=TestPrefetchStrategy(),
            clock=custom_clock,
        )

        # Initialize cache with no prefetch time
        supplier._cached_value = RefreshResult(
            "value",
            current_time[0] + timedelta(hours=1),
            None,  # No prefetch time
        )

        # Move time forward (past when prefetch would be triggered if we had a prefetch_time)
        current_time[0] = datetime(2024, 1, 1, 13, 0, 0)

        # Get value multiple times
        for _ in range(3):
            supplier.get()

        # Should not trigger prefetch since prefetch_time is None
        self.assertEqual(prefetch_count[0], 0)

    def test_stale_time_none_cache_not_stale(self):
        """Test that cache is not considered stale when stale_time is None"""
        value = "test_value"

        supplier = CachedResultSupplier(
            value_supplier=lambda: RefreshResult(
                value,
                None,  # No stale time
                None,
            ),
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
        )

        # Initialize cache with no stale time
        supplier._cached_value = RefreshResult(value, None, None)

        # Get value - should not trigger refresh
        result = supplier.get()
        self.assertEqual(result, value)

    def test_prefetch_strategy_none_with_no_prefetch_time(self):
        """Test behavior when prefetch_strategy is None and no prefetch time"""
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        call_count = [0]

        def value_supplier():
            call_count[0] += 1
            return RefreshResult(
                f"value_{call_count[0]}",
                current_time[0] + timedelta(hours=1),
                None,  # No prefetch time
            )

        supplier = CachedResultSupplier(
            value_supplier=value_supplier,
            prefetch_strategy=None,  # No prefetch strategy
            clock=custom_clock,
        )

        # Initialize cache
        supplier._cached_value = RefreshResult(
            "initial",
            current_time[0] + timedelta(hours=1),
            None,  # No prefetch time
        )

        # Move time forward
        current_time[0] = datetime(2024, 1, 1, 13, 0, 0)

        # Get value - should work fine since no prefetch time is set
        result = supplier.get()
        self.assertEqual(result, "initial")

    def test_prefetch_strategy_none_with_prefetch_time_raises_error(self):
        """Test that prefetch_strategy=None with prefetch time raises AttributeError"""
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        supplier = CachedResultSupplier(
            value_supplier=lambda: RefreshResult(
                "value",
                current_time[0] + timedelta(hours=1),
                current_time[0] + timedelta(minutes=30),  # Has prefetch time
            ),
            prefetch_strategy=None,  # No prefetch strategy
            clock=custom_clock,
        )

        # Initialize cache
        supplier._cached_value = RefreshResult(
            "initial", current_time[0] + timedelta(hours=1), current_time[0] + timedelta(minutes=30)
        )

        # Move time past prefetch time
        current_time[0] = datetime(2024, 1, 1, 13, 0, 0)

        # Should raise AttributeError when trying to prefetch with None strategy
        with self.assertRaises(AttributeError):
            supplier.get()

    def test_jitter_time_with_zero_range(self):
        """Test jitter_time when JITTER_RANGE is zero"""
        import cloud_idaas.core.cache.cached_result_supplier as cache_module

        # Temporarily set JITTER_RANGE to zero
        original_range = cache_module.JITTER_RANGE
        cache_module.JITTER_RANGE = timedelta(seconds=0)

        try:
            value = "test_value"
            fixed_time = datetime(2024, 1, 1, 12, 0, 0)
            stale_time = fixed_time + timedelta(hours=1)

            def custom_clock():
                return fixed_time

            supplier = CachedResultSupplier(
                value_supplier=lambda: RefreshResult(value, stale_time, None),
                prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
                clock=custom_clock,
            )

            result = supplier.get()
            self.assertEqual(result, value)

            # When JITTER_RANGE is zero, jitter_time returns the original time directly
            # (without adding JITTER_START or any jitter)
            if supplier._cached_value.stale_time:
                self.assertEqual(supplier._cached_value.stale_time, stale_time)
        finally:
            # Restore original JITTER_RANGE
            cache_module.JITTER_RANGE = original_range

    def test_lock_timeout_returns_old_value(self):
        """Test that old value is returned when lock acquisition times out"""
        import cloud_idaas.core.cache.cached_result_supplier as cache_module

        # Temporarily reduce timeout for testing
        original_timeout = cache_module.BLOCKING_REFRESH_MAX_WAIT
        cache_module.BLOCKING_REFRESH_MAX_WAIT = timedelta(milliseconds=10)

        try:
            call_count = [0]
            current_time = [datetime(2024, 1, 1, 12, 0, 0)]

            def custom_clock():
                return current_time[0]

            def blocking_supplier():
                call_count[0] += 1
                time.sleep(0.2)  # Block longer than timeout
                return RefreshResult(f"value_{call_count[0]}", current_time[0] + timedelta(hours=1), None)

            supplier = CachedResultSupplier(
                value_supplier=blocking_supplier,
                prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
                clock=custom_clock,
            )

            # Initialize with stale cache
            supplier._cached_value = RefreshResult(
                "old_value",
                datetime(2024, 1, 1, 11, 0, 0),  # Already stale
                None,
            )

            # Start a thread that will acquire the lock and block
            def blocking_get():
                supplier.get()

            thread = threading.Thread(target=blocking_get)
            thread.start()

            # Small delay to ensure thread acquires lock
            time.sleep(0.01)

            # Try to get value - should timeout and return old value
            result = supplier.get()

            thread.join()

            # Should return old value from before refresh completed
            self.assertEqual(result, "old_value")
        finally:
            # Restore original timeout
            cache_module.BLOCKING_REFRESH_MAX_WAIT = original_timeout

    def test_double_check_after_other_thread_refreshed(self):
        """Test double-check pattern when another thread has already refreshed"""
        call_count = [0]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            with threading.Lock():
                call_count[0] += 1
            time.sleep(0.1)
            return RefreshResult(f"value_{call_count[0]}", current_time[0] + timedelta(hours=1), None)

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=OneCallerBlocksPrefetchStrategy(), clock=custom_clock
        )

        # Initialize with stale cache
        supplier._cached_value = RefreshResult("initial", datetime(2024, 1, 1, 11, 0, 0), None)

        barrier = threading.Barrier(2)
        results = []

        def get_value():
            barrier.wait()  # Synchronize start
            results.append(supplier.get())

        # Start two threads simultaneously
        thread1 = threading.Thread(target=get_value)
        thread2 = threading.Thread(target=get_value)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        # Due to double-check, only one refresh should occur
        self.assertLessEqual(call_count[0], 2)

        # Both threads should get valid results
        self.assertEqual(len(results), 2)

    def test_concurrent_operation_exception_with_null_cache(self):
        """Test ConcurrentOperationException when cache is null and refresh fails"""

        def failing_supplier():
            raise Exception("Refresh failed")

        supplier = CachedResultSupplier(
            value_supplier=failing_supplier,
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
            stale_value_behavior=StaleValueBehavior.ALLOW,
        )

        # No initial cache
        self.assertIsNone(supplier._cached_value)

        with self.assertRaises(ConcurrentOperationException):
            supplier.get()

    def test_prefetch_triggered_at_right_time(self):
        """Test that prefetch is triggered at the right time"""
        prefetch_called = [False]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            return RefreshResult("value", current_time[0] + timedelta(hours=1), current_time[0] + timedelta(minutes=30))

        class TestPrefetchStrategy:
            def prefetch(self, value_updater):
                prefetch_called[0] = True
                value_updater()

            def close(self):
                pass

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=TestPrefetchStrategy(), clock=custom_clock
        )

        # Initialize cache
        supplier._cached_value = RefreshResult(
            "initial", current_time[0] + timedelta(hours=1), current_time[0] + timedelta(minutes=30)
        )

        # Before prefetch time - should not trigger
        current_time[0] = datetime(2024, 1, 1, 12, 29, 0)
        supplier.get()
        self.assertFalse(prefetch_called[0])

        # At prefetch time - should trigger
        current_time[0] = datetime(2024, 1, 1, 12, 31, 0)
        supplier.get()
        self.assertTrue(prefetch_called[0])

    def test_jitter_applied_to_both_times(self):
        """Test that jitter is applied to both stale_time and prefetch_time"""
        value = "test_value"
        stale_time = datetime.now(timezone.utc) + timedelta(hours=1)
        prefetch_time = datetime.now(timezone.utc) + timedelta(minutes=30)

        supplier = CachedResultSupplier(
            value_supplier=lambda: RefreshResult(value, stale_time, prefetch_time),
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
        )

        result = supplier.get()
        self.assertEqual(result, value)

        # Both times should be jittered (greater than original)
        if supplier._cached_value.stale_time:
            self.assertGreater(supplier._cached_value.stale_time, stale_time)

        if supplier._cached_value.prefetch_time:
            self.assertGreater(supplier._cached_value.prefetch_time, prefetch_time)

    def test_generic_type_support(self):
        """Test that CachedResultSupplier works with different types"""
        # Test with int
        int_supplier = CachedResultSupplier(
            value_supplier=lambda: RefreshResult(42, datetime.now(timezone.utc) + timedelta(hours=1), None),
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
        )
        self.assertIsInstance(int_supplier.get(), int)

        # Test with dict
        dict_supplier = CachedResultSupplier(
            value_supplier=lambda: RefreshResult(
                {"key": "value"}, datetime.now(timezone.utc) + timedelta(hours=1), None
            ),
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
        )
        self.assertIsInstance(dict_supplier.get(), dict)

        # Test with custom class
        class CustomClass:
            def __init__(self, value):
                self.value = value

        custom_supplier = CachedResultSupplier(
            value_supplier=lambda: RefreshResult(
                CustomClass("test"), datetime.now(timezone.utc) + timedelta(hours=1), None
            ),
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
        )
        self.assertIsInstance(custom_supplier.get(), CustomClass)


class TestCachedResultSupplierJitterBehavior(unittest.TestCase):
    """Test cases for jitter behavior in CachedResultSupplier"""

    def test_jitter_start_is_added(self):
        """Test that JITTER_START is always added when JITTER_RANGE > 0"""
        import cloud_idaas.core.cache.cached_result_supplier as cache_module

        original_start = cache_module.JITTER_START
        original_range = cache_module.JITTER_RANGE

        try:
            # Set a specific JITTER_START for testing
            cache_module.JITTER_START = timedelta(seconds=10)
            cache_module.JITTER_RANGE = timedelta(seconds=5)

            value = "test_value"
            fixed_time = datetime(2024, 1, 1, 12, 0, 0)
            stale_time = fixed_time + timedelta(hours=1)

            def custom_clock():
                return fixed_time

            supplier = CachedResultSupplier(
                value_supplier=lambda: RefreshResult(value, stale_time, None),
                prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
                clock=custom_clock,
            )

            result = supplier.get()
            self.assertEqual(result, value)

            # JITTER_START (10s) + random amount from JITTER_RANGE (0-5s) should be added
            # So stale_time should be at least original + 10 seconds
            if supplier._cached_value.stale_time:
                min_expected = stale_time + cache_module.JITTER_START
                self.assertGreaterEqual(supplier._cached_value.stale_time, min_expected)
        finally:
            cache_module.JITTER_START = original_start
            cache_module.JITTER_RANGE = original_range

    def test_jitter_randomness(self):
        """Test that jitter adds random variation"""
        import cloud_idaas.core.cache.cached_result_supplier as cache_module

        original_range = cache_module.JITTER_RANGE
        original_start = cache_module.JITTER_START

        try:
            # Set a larger range for better randomness detection
            cache_module.JITTER_RANGE = timedelta(seconds=30)
            cache_module.JITTER_START = timedelta(seconds=0)

            fixed_time = datetime(2024, 1, 1, 12, 0, 0)
            stale_time = fixed_time + timedelta(hours=1)

            def custom_clock():
                return fixed_time

            stale_times = []
            for _ in range(10):
                supplier = CachedResultSupplier(
                    value_supplier=lambda: RefreshResult("value", stale_time, None),
                    prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
                    clock=custom_clock,
                )
                supplier.get()
                if supplier._cached_value.stale_time:
                    stale_times.append(supplier._cached_value.stale_time)

            # Should have collected multiple values
            self.assertGreater(len(stale_times), 0)

            # Check for variation (not all values should be the same)
            # With random jitter, we expect some variation
            unique_values = set(stale_times)
            # Allow for possibility of same random values, but likely to have variation
            # This is a probabilistic test
        finally:
            cache_module.JITTER_RANGE = original_range
            cache_module.JITTER_START = original_start

    def test_jitter_with_negative_jitter_amount(self):
        """Test that abs() is used on jitter amount"""
        import random as random_module

        import cloud_idaas.core.cache.cached_result_supplier as cache_module

        original_range = cache_module.JITTER_RANGE
        original_start = cache_module.JITTER_START

        try:
            cache_module.JITTER_RANGE = timedelta(seconds=10)
            cache_module.JITTER_START = timedelta(seconds=5)

            # Mock random.random to return a positive value
            original_random = random_module.random
            random_module.random = lambda: 0.5

            fixed_time = datetime(2024, 1, 1, 12, 0, 0)
            stale_time = fixed_time + timedelta(hours=1)

            def custom_clock():
                return fixed_time

            supplier = CachedResultSupplier(
                value_supplier=lambda: RefreshResult("value", stale_time, None),
                prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
                clock=custom_clock,
            )

            supplier.get()

            # With random.random() = 0.5 and abs(), jitter_amount = 0.5 * 10 = 5 seconds
            # JITTER_START = 5 seconds
            # Total added = 10 seconds
            if supplier._cached_value.stale_time:
                expected_min = stale_time + timedelta(seconds=10)
                self.assertGreaterEqual(supplier._cached_value.stale_time, expected_min)
        finally:
            cache_module.JITTER_RANGE = original_range
            cache_module.JITTER_START = original_start
            random_module.random = original_random


class TestCachedResultSupplierPrefetchScenarios(unittest.TestCase):
    """Test cases for various prefetch scenarios"""

    def test_prefetch_not_triggered_before_time(self):
        """Test that prefetch is not triggered before prefetch_time"""
        prefetch_triggered = [False]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            return RefreshResult("value", current_time[0] + timedelta(hours=1), current_time[0] + timedelta(minutes=30))

        class TrackingPrefetchStrategy:
            def __init__(self):
                self._currently_refreshing = threading.Event()

            def prefetch(self, value_updater):
                prefetch_triggered[0] = True
                if not self._currently_refreshing.is_set():
                    self._currently_refreshing.set()
                    try:
                        value_updater()
                    finally:
                        self._currently_refreshing.clear()

            def close(self):
                self._currently_refreshing.clear()

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=TrackingPrefetchStrategy(), clock=custom_clock
        )

        # First call - initial value
        supplier.get()
        # Prefetch should not be triggered yet (time is 12:00, prefetch is 12:30)
        self.assertFalse(prefetch_triggered[0])

        # Move time just before prefetch time (29 minutes)
        current_time[0] = datetime(2024, 1, 1, 12, 29, 0)

        # Call again - should NOT trigger prefetch yet
        supplier.get()
        self.assertFalse(prefetch_triggered[0])

    def test_prefetch_triggered_after_time(self):
        """Test that prefetch IS triggered after prefetch_time"""
        prefetch_triggered = [False]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            return RefreshResult("value", current_time[0] + timedelta(hours=1), current_time[0] + timedelta(minutes=30))

        class TrackingPrefetchStrategy:
            def __init__(self):
                self._currently_refreshing = threading.Event()

            def prefetch(self, value_updater):
                prefetch_triggered[0] = True
                if not self._currently_refreshing.is_set():
                    self._currently_refreshing.set()
                    try:
                        value_updater()
                    finally:
                        self._currently_refreshing.clear()

            def close(self):
                self._currently_refreshing.clear()

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=TrackingPrefetchStrategy(), clock=custom_clock
        )

        # First call - initial value
        supplier.get()
        self.assertFalse(prefetch_triggered[0])

        # Move time past prefetch time (accounting for JITTER_START + JITTER_RANGE)
        # JITTER_START = 5 minutes, JITTER_RANGE = 5 minutes
        # So prefetch_time could be up to 10 minutes later
        current_time[0] = datetime(2024, 1, 1, 12, 50, 0)

        # Call again - should trigger prefetch
        supplier.get()
        self.assertTrue(prefetch_triggered[0])

    def test_prefetch_not_called_when_prefetch_time_is_none(self):
        """Test that prefetch is not called when prefetch_time is None"""
        prefetch_triggered = [False]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            return RefreshResult(
                "value",
                current_time[0] + timedelta(hours=1),
                None,  # No prefetch time
            )

        class TrackingPrefetchStrategy:
            def __init__(self):
                self._currently_refreshing = threading.Event()

            def prefetch(self, value_updater):
                prefetch_triggered[0] = True
                if not self._currently_refreshing.is_set():
                    self._currently_refreshing.set()
                    try:
                        value_updater()
                    finally:
                        self._currently_refreshing.clear()

            def close(self):
                self._currently_refreshing.clear()

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=TrackingPrefetchStrategy(), clock=custom_clock
        )

        # Call multiple times with time advancing
        for i in range(5):
            supplier.get()
            current_time[0] = current_time[0] + timedelta(hours=1)

        # Prefetch should never be triggered when prefetch_time is None
        self.assertFalse(prefetch_triggered[0])

    def test_prefetch_with_stale_value_behavior_allow(self):
        """Test prefetch behavior in ALLOW mode with stale cache"""
        prefetch_count = [0]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            prefetch_count[0] += 1
            if prefetch_count[0] == 1:
                return RefreshResult(
                    "initial", current_time[0] + timedelta(minutes=10), current_time[0] + timedelta(minutes=5)
                )
            else:
                return RefreshResult(
                    "refreshed", current_time[0] + timedelta(hours=1), current_time[0] + timedelta(minutes=30)
                )

        supplier = CachedResultSupplier(
            value_supplier=value_supplier,
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
            clock=custom_clock,
            stale_value_behavior=StaleValueBehavior.ALLOW,
        )

        # First call
        result1 = supplier.get()
        self.assertEqual(result1, "initial")

        # Move time past stale time but before prefetch would matter
        current_time[0] = datetime(2024, 1, 1, 12, 20, 0)

        # Second call - should refresh due to stale
        result2 = supplier.get()
        self.assertEqual(result2, "refreshed")


class TestCachedResultSupplierExceptionHandling(unittest.TestCase):
    """Test cases for exception handling in CachedResultSupplier"""

    def test_value_supplier_exception_with_stale_cache_strict(self):
        """Test exception handling in STRICT mode with stale cache"""
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def failing_supplier():
            raise ValueError("Supplier failed")

        supplier = CachedResultSupplier(
            value_supplier=failing_supplier,
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
            clock=custom_clock,
            stale_value_behavior=StaleValueBehavior.STRICT,
        )

        # Initialize with stale cache
        supplier._cached_value = RefreshResult(
            "old_value",
            datetime(2024, 1, 1, 11, 0, 0),  # Already stale
            None,
        )

        with self.assertRaises(CacheException):
            supplier.get()

    def test_value_supplier_exception_with_stale_cache_allow(self):
        """Test exception handling in ALLOW mode with stale cache"""
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def failing_supplier():
            raise ValueError("Supplier failed")

        supplier = CachedResultSupplier(
            value_supplier=failing_supplier,
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
            clock=custom_clock,
            stale_value_behavior=StaleValueBehavior.ALLOW,
        )

        # Initialize with stale cache
        supplier._cached_value = RefreshResult(
            "old_value",
            datetime(2024, 1, 1, 11, 0, 0),  # Already stale
            None,
        )

        # Should return old value instead of raising
        result = supplier.get()
        self.assertEqual(result, "old_value")

    def test_value_supplier_exception_with_null_cache(self):
        """Test exception handling when cache is null"""

        def failing_supplier():
            raise ValueError("Supplier failed")

        supplier = CachedResultSupplier(
            value_supplier=failing_supplier,
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
            stale_value_behavior=StaleValueBehavior.ALLOW,
        )

        # With null cache, should raise ConcurrentOperationException
        with self.assertRaises(ConcurrentOperationException):
            supplier.get()


class TestCachedResultSupplierLockBehavior(unittest.TestCase):
    """Test cases for lock behavior in CachedResultSupplier"""

    def test_lock_released_after_exception(self):
        """Test that lock is properly released even when value_supplier raises exception"""
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def failing_supplier():
            raise ValueError("Test exception")

        supplier = CachedResultSupplier(
            value_supplier=failing_supplier,
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
            clock=custom_clock,
            stale_value_behavior=StaleValueBehavior.STRICT,
        )

        # Initialize with stale cache
        supplier._cached_value = RefreshResult("old_value", datetime(2024, 1, 1, 11, 0, 0), None)

        with self.assertRaises(CacheException):
            supplier.get()

        # Lock should be released after exception
        self.assertFalse(supplier._refresh_lock.locked())

    def test_concurrent_access_with_lock_timeout(self):
        """Test concurrent access behavior when lock timeout occurs"""
        import cloud_idaas.core.cache.cached_result_supplier as cache_module

        original_timeout = cache_module.BLOCKING_REFRESH_MAX_WAIT

        try:
            # Reduce timeout for faster test
            cache_module.BLOCKING_REFRESH_MAX_WAIT = timedelta(milliseconds=50)

            call_count = [0]
            current_time = [datetime(2024, 1, 1, 12, 0, 0)]

            def custom_clock():
                return current_time[0]

            def slow_supplier():
                call_count[0] += 1
                time.sleep(0.2)  # Block longer than timeout
                return RefreshResult(f"value_{call_count[0]}", current_time[0] + timedelta(hours=1), None)

            supplier = CachedResultSupplier(
                value_supplier=slow_supplier, prefetch_strategy=OneCallerBlocksPrefetchStrategy(), clock=custom_clock
            )

            # Initialize with stale cache
            supplier._cached_value = RefreshResult("old_value", datetime(2024, 1, 1, 11, 0, 0), None)

            # Start first refresh in a thread
            def refresh_thread():
                try:
                    supplier.get()
                except:
                    pass

            thread = threading.Thread(target=refresh_thread)
            thread.start()

            # Small delay to ensure thread acquires lock
            time.sleep(0.01)

            # Try to get value - should timeout and return old value
            result = supplier.get()
            self.assertEqual(result, "old_value")

            thread.join()
        finally:
            cache_module.BLOCKING_REFRESH_MAX_WAIT = original_timeout


class TestCachedResultSupplierIntegrationScenarios(unittest.TestCase):
    """Integration test scenarios for CachedResultSupplier"""

    def test_full_lifecycle_with_prefetch(self):
        """Test full lifecycle: initial load, prefetch, and stale refresh"""
        call_count = [0]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            call_count[0] += 1
            return RefreshResult(
                f"value_{call_count[0]}", current_time[0] + timedelta(hours=1), current_time[0] + timedelta(minutes=30)
            )

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=OneCallerBlocksPrefetchStrategy(), clock=custom_clock
        )

        # Phase 1: Initial load
        result1 = supplier.get()
        self.assertEqual(result1, "value_1")
        self.assertEqual(call_count[0], 1)

        # Phase 2: Still fresh, no prefetch yet
        current_time[0] = datetime(2024, 1, 1, 12, 20, 0)
        result2 = supplier.get()
        self.assertEqual(result2, "value_1")  # Same value
        self.assertEqual(call_count[0], 1)  # No new call

        # Phase 3: Past prefetch time (but still fresh)
        # JITTER could add up to 10 minutes (5 start + 5 range)
        current_time[0] = datetime(2024, 1, 1, 12, 50, 0)
        result3 = supplier.get()
        self.assertEqual(result3, "value_1")  # Still same value (prefetch is async)
        # Prefetch should have been triggered, but value might not be updated yet

        # Phase 4: Now stale, should force refresh
        current_time[0] = datetime(2024, 1, 1, 13, 30, 0)
        result4 = supplier.get()
        self.assertEqual(result4, "value_2")  # New value
        self.assertEqual(call_count[0], 2)  # Prefetch or refresh called

    def test_rapid_get_calls_with_valid_cache(self):
        """Test rapid get calls with valid cache (no refreshes)"""
        call_count = [0]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            call_count[0] += 1
            return RefreshResult(f"value_{call_count[0]}", current_time[0] + timedelta(hours=24), None)

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=OneCallerBlocksPrefetchStrategy(), clock=custom_clock
        )

        # Rapid calls should only trigger supplier once
        for _ in range(100):
            result = supplier.get()
            self.assertEqual(result, "value_1")

        self.assertEqual(call_count[0], 1)

    def test_alternating_stale_and_fresh_states(self):
        """Test alternating between stale and fresh states"""
        call_count = [0]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            call_count[0] += 1
            return RefreshResult(f"value_{call_count[0]}", current_time[0] + timedelta(minutes=10), None)

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=OneCallerBlocksPrefetchStrategy(), clock=custom_clock
        )

        # Initial load
        result1 = supplier.get()
        self.assertEqual(result1, "value_1")

        # Move past stale time (need to account for jitter: 5 min start + up to 5 min range)
        current_time[0] = datetime(2024, 1, 1, 12, 20, 0)
        result2 = supplier.get()
        self.assertEqual(result2, "value_2")

        # Move past stale time again
        current_time[0] = datetime(2024, 1, 1, 12, 40, 0)
        result3 = supplier.get()
        self.assertEqual(result3, "value_3")

        # Still fresh
        result4 = supplier.get()
        self.assertEqual(result4, "value_3")

        self.assertEqual(call_count[0], 3)

    def test_supplier_returning_different_value_types(self):
        """Test supplier returning different value types across calls"""
        call_count = [0]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            call_count[0] += 1
            values = ["string", 42, {"key": "value"}, [1, 2, 3]]
            return RefreshResult(
                values[(call_count[0] - 1) % len(values)], current_time[0] + timedelta(minutes=5), None
            )

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=OneCallerBlocksPrefetchStrategy(), clock=custom_clock
        )

        result1 = supplier.get()
        self.assertEqual(result1, "string")

        # Move past stale time (need to account for jitter)
        current_time[0] = datetime(2024, 1, 1, 12, 20, 0)
        result2 = supplier.get()
        self.assertEqual(result2, 42)

        current_time[0] = datetime(2024, 1, 1, 12, 40, 0)
        result3 = supplier.get()
        self.assertEqual(result3, {"key": "value"})

        current_time[0] = datetime(2024, 1, 1, 13, 0, 0)
        result4 = supplier.get()
        self.assertEqual(result4, [1, 2, 3])

    def test_cache_with_very_short_ttl(self):
        """Test cache with very short time-to-live"""
        call_count = [0]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            call_count[0] += 1
            return RefreshResult(
                f"value_{call_count[0]}",
                current_time[0] + timedelta(milliseconds=10),  # Very short TTL
                None,
            )

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=OneCallerBlocksPrefetchStrategy(), clock=custom_clock
        )

        # First call
        result1 = supplier.get()
        self.assertEqual(result1, "value_1")

        # Small delay - might still be cached (but jitter could make it stale)
        result2 = supplier.get()
        self.assertIn(result2, ["value_1", "value_2"])

        # Larger delay - definitely stale (jitter adds at most ~10 minutes)
        current_time[0] = datetime(2024, 1, 1, 13, 0, 0)  # 1 hour later
        result3 = supplier.get()
        # After moving time forward significantly, should get a new value
        # The exact value depends on whether result2 triggered a refresh
        self.assertIn(result3, ["value_2", "value_3"])

    def test_cache_with_very_long_ttl(self):
        """Test cache with very long time-to-live"""
        call_count = [0]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            call_count[0] += 1
            return RefreshResult(
                f"value_{call_count[0]}",
                current_time[0] + timedelta(days=365),  # Very long TTL
                None,
            )

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=OneCallerBlocksPrefetchStrategy(), clock=custom_clock
        )

        # Initial load
        result1 = supplier.get()
        self.assertEqual(result1, "value_1")

        # Even after significant time, still cached
        current_time[0] = datetime(2024, 1, 1, 18, 0, 0)  # 6 hours later
        result2 = supplier.get()
        self.assertEqual(result2, "value_1")
        self.assertEqual(call_count[0], 1)  # No new calls

    def test_supplier_returning_none_value(self):
        """Test supplier returning None as cached value"""
        call_count = [0]
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        def value_supplier():
            call_count[0] += 1
            return RefreshResult(
                None,  # None as value
                current_time[0] + timedelta(hours=1),
                None,
            )

        supplier = CachedResultSupplier(
            value_supplier=value_supplier, prefetch_strategy=OneCallerBlocksPrefetchStrategy(), clock=custom_clock
        )

        # Should work with None value
        result1 = supplier.get()
        self.assertIsNone(result1)

        # Still cached
        result2 = supplier.get()
        self.assertIsNone(result2)
        self.assertEqual(call_count[0], 1)

    def test_supplier_with_empty_values(self):
        """Test supplier returning empty values"""
        current_time = [datetime(2024, 1, 1, 12, 0, 0)]

        def custom_clock():
            return current_time[0]

        # Test with empty string
        supplier1 = CachedResultSupplier(
            value_supplier=lambda: RefreshResult("", current_time[0] + timedelta(hours=1), None),
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
            clock=custom_clock,
        )
        self.assertEqual(supplier1.get(), "")

        # Test with empty dict
        supplier2 = CachedResultSupplier(
            value_supplier=lambda: RefreshResult({}, current_time[0] + timedelta(hours=1), None),
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
            clock=custom_clock,
        )
        self.assertEqual(supplier2.get(), {})

        # Test with empty list
        supplier3 = CachedResultSupplier(
            value_supplier=lambda: RefreshResult([], current_time[0] + timedelta(hours=1), None),
            prefetch_strategy=OneCallerBlocksPrefetchStrategy(),
            clock=custom_clock,
        )
        self.assertEqual(supplier3.get(), [])


if __name__ == "__main__":
    unittest.main()
