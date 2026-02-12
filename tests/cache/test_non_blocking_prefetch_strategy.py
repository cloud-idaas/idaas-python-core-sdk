"""
Tests for NonBlockingPrefetchStrategy class
"""

import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import MagicMock, patch

from cloud_idaas.core.cache.strategy.non_blocking_prefetch_strategy import (
    MAX_CONCURRENT_REFRESHES,
    NonBlockingPrefetchStrategy,
)


class TestNonBlockingPrefetchStrategy(unittest.TestCase):
    """Test cases for NonBlockingPrefetchStrategy class"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a fresh executor for each test to avoid interference
        self.original_executor = NonBlockingPrefetchStrategy._executor
        NonBlockingPrefetchStrategy._executor = ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="test-non-blocking-refresh",
        )
        self.strategy = NonBlockingPrefetchStrategy()

    def tearDown(self):
        """Clean up test fixtures"""
        self.strategy.close()
        # Restore original executor
        NonBlockingPrefetchStrategy._executor.shutdown(wait=True)
        NonBlockingPrefetchStrategy._executor = self.original_executor

    def test_prefetch_single_call(self):
        """Test prefetch with single call"""
        value_updater = MagicMock()
        self.strategy.prefetch(value_updater)

        # Give some time for async execution
        time.sleep(0.1)

        value_updater.assert_called_once()

    def test_prefetch_concurrent_calls_one_instance(self):
        """Test concurrent prefetch calls on same instance (only one should execute)"""
        call_count = [0]
        event = threading.Event()

        def value_updater():
            call_count[0] += 1
            time.sleep(0.2)  # Simulate slow operation
            event.set()

        # Start multiple prefetch calls in threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=self.strategy.prefetch, args=(value_updater,))
            thread.start()
            threads.append(thread)

        # Wait for the operation to complete
        event.wait(timeout=1.0)

        # Give some time for all threads to complete
        time.sleep(0.3)

        for thread in threads:
            thread.join(timeout=0.1)

        # Should have been called exactly once
        self.assertEqual(call_count[0], 1)

    def test_prefetch_sequential_calls(self):
        """Test sequential prefetch calls (both should execute)"""
        value_updater = MagicMock()
        call_count = [0]

        def mock_updater():
            call_count[0] += 1

        value_updater.side_effect = mock_updater

        # First call
        self.strategy.prefetch(value_updater)
        time.sleep(0.1)

        # Second call should execute after first completes
        self.strategy.prefetch(value_updater)
        time.sleep(0.1)

        self.assertEqual(call_count[0], 2)

    def test_multiple_instances_concurrent(self):
        """Test concurrent prefetch with multiple strategy instances"""
        call_count = [0]
        event = threading.Event()

        def value_updater():
            call_count[0] += 1
            time.sleep(0.1)
            if call_count[0] >= 3:
                event.set()

        strategies = [NonBlockingPrefetchStrategy() for _ in range(3)]

        # Start prefetch on all instances
        for strategy in strategies:
            strategy.prefetch(value_updater)

        # Wait for all to complete
        event.wait(timeout=1.0)
        time.sleep(0.2)

        # Each instance should have triggered one update
        self.assertEqual(call_count[0], 3)

        # Clean up
        for strategy in strategies:
            strategy.close()

    def test_max_concurrent_refreshes_limit(self):
        """Test that max concurrent refreshes is respected"""
        active_count = [0]
        max_active = [0]
        start_event = threading.Event()
        continue_event = threading.Event()

        def blocking_updater():
            active_count[0] += 1
            max_active[0] = max(max_active[0], active_count[0])
            start_event.set()
            continue_event.wait(timeout=2.0)
            active_count[0] -= 1

        strategies = []

        # Start more prefetches than MAX_CONCURRENT_REFRESHES
        for i in range(MAX_CONCURRENT_REFRESHES + 5):
            strategy = NonBlockingPrefetchStrategy()
            strategies.append(strategy)
            strategy.prefetch(blocking_updater)

        # Wait for at least one to start
        start_event.wait(timeout=1.0)
        time.sleep(0.1)

        # Max active should not exceed MAX_CONCURRENT_REFRESHES
        self.assertLessEqual(max_active[0], MAX_CONCURRENT_REFRESHES + 1)  # +1 for timing

        # Continue and clean up
        continue_event.set()
        for strategy in strategies:
            strategy.close()

    def test_executor_submit_failure_handling(self):
        """Test handling when executor.submit fails"""
        value_updater = MagicMock()

        # Mock executor.submit to raise exception
        with patch.object(NonBlockingPrefetchStrategy._executor, "submit") as mock_submit:
            mock_submit.side_effect = RuntimeError("Executor failed")

            self.strategy.prefetch(value_updater)

            # After failure, the prefetching flag should be cleared immediately
            # (synchronously in the except block)
            self.assertFalse(self.strategy._currently_prefetching.is_set())

            # Lease should be released
            self.assertEqual(self.strategy._concurrent_refresh_lease._value, MAX_CONCURRENT_REFRESHES)

    def test_updater_exception_handling(self):
        """Test exception handling within value_updater"""

        def failing_updater():
            raise ValueError("Updater failed")

        self.strategy.prefetch(failing_updater)

        # Give time for execution and cleanup
        time.sleep(0.2)

        # Flag should be cleared even after exception
        self.assertFalse(self.strategy._currently_prefetching.is_set())

        # Lease should be released
        self.assertEqual(self.strategy._concurrent_refresh_lease._value, MAX_CONCURRENT_REFRESHES)

    def test_close(self):
        """Test close method"""
        self.strategy._currently_prefetching.set()
        self.strategy.close()

        # After close, flag should be cleared
        self.assertFalse(self.strategy._currently_prefetching.is_set())

    def test_concurrent_refresh_lease_exhausted(self):
        """Test behavior when concurrent refresh lease is exhausted"""
        # Acquire all leases
        leases = []
        for _ in range(MAX_CONCURRENT_REFRESHES):
            self.assertTrue(self.strategy._concurrent_refresh_lease.acquire(blocking=False))
            leases.append(self.strategy._concurrent_refresh_lease)

        value_updater = MagicMock()

        # This prefetch should be skipped due to lease exhaustion
        self.strategy.prefetch(value_updater)

        time.sleep(0.1)

        # Updater should not have been called
        value_updater.assert_not_called()

        # Clean up
        for _ in range(MAX_CONCURRENT_REFRESHES):
            self.strategy._concurrent_refresh_lease.release()

    def test_shutdown_executor(self):
        """Test class method shutdown_executor"""
        # This is a class-level method that affects all instances
        # Just verify it can be called without error
        NonBlockingPrefetchStrategy.shutdown_executor()


class TestNonBlockingPrefetchStrategyContextManager(unittest.TestCase):
    """Test cases for NonBlockingPrefetchStrategy context manager"""

    def test_context_manager(self):
        """Test using NonBlockingPrefetchStrategy as context manager"""
        with NonBlockingPrefetchStrategy() as strategy:
            value_updater = MagicMock()
            strategy.prefetch(value_updater)
            # Wait for the executor to process the task
            time.sleep(0.5)
            value_updater.assert_called_once()

        # After exiting context, close should have been called
        self.assertFalse(strategy._currently_prefetching.is_set())

    def test_context_manager_with_exception(self):
        """Test context manager behavior with exception"""
        with NonBlockingPrefetchStrategy() as strategy:
            value_updater = MagicMock()
            strategy.prefetch(value_updater)
            time.sleep(0.1)
            try:
                raise ValueError("Test exception")
            except ValueError:
                pass  # Expected exception

        # Close should still be called even with exception
        self.assertFalse(strategy._currently_prefetching.is_set())

    def test_context_manager_returns_self_on_enter(self):
        """Test that context manager __enter__ returns self"""
        with NonBlockingPrefetchStrategy() as strategy:
            self.assertIsInstance(strategy, NonBlockingPrefetchStrategy)


class TestNonBlockingPrefetchStrategyEdgeCases(unittest.TestCase):
    """Test edge cases for NonBlockingPrefetchStrategy"""

    def setUp(self):
        """Set up test fixtures"""
        self.original_executor = NonBlockingPrefetchStrategy._executor
        NonBlockingPrefetchStrategy._executor = ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="test-non-blocking-refresh-edge",
        )
        self.strategy = NonBlockingPrefetchStrategy()

    def tearDown(self):
        """Clean up test fixtures"""
        self.strategy.close()
        NonBlockingPrefetchStrategy._executor.shutdown(wait=True)
        NonBlockingPrefetchStrategy._executor = self.original_executor

    def test_multiple_prefetch_after_completion(self):
        """Test that prefetch can be called multiple times after completion"""
        call_count = [0]

        def value_updater():
            call_count[0] += 1

        # First prefetch
        self.strategy.prefetch(value_updater)
        time.sleep(0.1)
        self.assertEqual(call_count[0], 1)

        # Second prefetch should also execute
        self.strategy.prefetch(value_updater)
        time.sleep(0.1)
        self.assertEqual(call_count[0], 2)

        # Third prefetch
        self.strategy.prefetch(value_updater)
        time.sleep(0.1)
        self.assertEqual(call_count[0], 3)

    def test_lease_released_on_normal_completion(self):
        """Test that lease is properly released when prefetch completes normally"""
        event = threading.Event()

        def value_updater():
            event.set()

        # Get initial lease count
        initial_lease = self.strategy._concurrent_refresh_lease._value

        self.strategy.prefetch(value_updater)
        event.wait(timeout=1.0)
        time.sleep(0.1)

        # Lease should be released back to original count
        self.assertEqual(self.strategy._concurrent_refresh_lease._value, initial_lease)

    def test_lease_acquired_and_released(self):
        """Test that lease is acquired before prefetch and released after"""
        event = threading.Event()

        def value_updater():
            event.set()

        # Before prefetch, lease should be at max
        self.assertEqual(self.strategy._concurrent_refresh_lease._value, MAX_CONCURRENT_REFRESHES)

        self.strategy.prefetch(value_updater)

        # During prefetch, lease should be reduced (but this is async so hard to test)
        # After completion, it should be restored
        event.wait(timeout=1.0)
        time.sleep(0.1)

        self.assertEqual(self.strategy._concurrent_refresh_lease._value, MAX_CONCURRENT_REFRESHES)

    def test_flag_cleared_after_successful_prefetch(self):
        """Test that _currently_prefetching flag is cleared after successful prefetch"""
        event = threading.Event()

        def value_updater():
            event.set()

        self.strategy.prefetch(value_updater)
        event.wait(timeout=1.0)
        time.sleep(0.1)

        self.assertFalse(self.strategy._currently_prefetching.is_set())

    def test_very_slow_updater(self):
        """Test with very slow value_updater"""
        event = threading.Event()

        def slow_updater():
            time.sleep(0.3)
            event.set()

        self.strategy.prefetch(slow_updater)
        event.wait(timeout=1.0)

        self.assertTrue(event.is_set())
        self.assertFalse(self.strategy._currently_prefetching.is_set())

    def test_rapid_sequential_calls(self):
        """Test very rapid sequential prefetch calls"""
        call_count = [0]
        event = threading.Event()

        def value_updater():
            call_count[0] += 1
            time.sleep(0.2)  # Simulate slow operation
            event.set()

        # Rapidly call prefetch multiple times
        # Due to _currently_prefetching flag, only the first will execute
        # Subsequent calls will be skipped until the flag is cleared
        for _ in range(10):
            self.strategy.prefetch(value_updater)

        # Wait for the first one to complete
        event.wait(timeout=1.0)

        # With a single-threaded executor and _currently_prefetching flag,
        # only one prefetch should execute when called rapidly
        # The flag is set immediately and prevents subsequent calls
        self.assertEqual(call_count[0], 1)

    def test_flag_set_during_prefetch(self):
        """Test that _currently_prefetching flag is set during prefetch"""
        flag_during = [None]
        event = threading.Event()

        def value_updater():
            flag_during[0] = self.strategy._currently_prefetching.is_set()
            event.set()

        self.strategy.prefetch(value_updater)
        event.wait(timeout=1.0)

        # Flag should have been set during prefetch
        self.assertTrue(flag_during[0])

    def test_multiple_instances_share_executor(self):
        """Test that multiple instances share the same executor"""
        # All instances should use the class-level executor
        strategy1 = NonBlockingPrefetchStrategy()
        strategy2 = NonBlockingPrefetchStrategy()

        self.assertIs(strategy1._executor, strategy2._executor)
        self.assertIs(strategy1._executor, NonBlockingPrefetchStrategy._executor)

        strategy1.close()
        strategy2.close()


if __name__ == "__main__":
    unittest.main()
