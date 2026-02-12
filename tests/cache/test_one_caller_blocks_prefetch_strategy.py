"""
Tests for OneCallerBlocksPrefetchStrategy class
"""

import threading
import time
import unittest
from unittest.mock import MagicMock

from cloud_idaas.core.cache.strategy.one_caller_blocks_prefetch_strategy import OneCallerBlocksPrefetchStrategy


class TestOneCallerBlocksPrefetchStrategy(unittest.TestCase):
    """Test cases for OneCallerBlocksPrefetchStrategy class"""

    def setUp(self):
        """Set up test fixtures"""
        self.strategy = OneCallerBlocksPrefetchStrategy()

    def tearDown(self):
        """Clean up test fixtures"""
        self.strategy.close()

    def test_prefetch_single_call(self):
        """Test prefetch with single call"""
        value_updater = MagicMock()
        self.strategy.prefetch(value_updater)

        value_updater.assert_called_once()

    def test_prefetch_concurrent_calls(self):
        """Test prefetch with concurrent calls (one should execute, one should be skipped)"""
        value_updater = MagicMock()
        value_updater.side_effect = lambda: time.sleep(0.1)  # Simulate slow operation

        # Start first prefetch in a thread
        thread1 = threading.Thread(target=self.strategy.prefetch, args=(value_updater,))
        thread1.start()

        # Start second prefetch immediately (should be skipped since first is running)
        time.sleep(0.01)  # Small delay to ensure first thread starts
        self.strategy.prefetch(value_updater)

        # Wait for first thread to complete
        thread1.join()

        # Should have been called exactly once (first call executed, second was skipped)
        self.assertEqual(value_updater.call_count, 1)

    def test_prefetch_sequential_calls(self):
        """Test sequential prefetch calls (both should execute)"""
        value_updater = MagicMock()

        # First call
        self.strategy.prefetch(value_updater)
        self.assertEqual(value_updater.call_count, 1)

        # Wait a bit to ensure completion
        time.sleep(0.1)

        # Second call should execute after first completes
        self.strategy.prefetch(value_updater)
        self.assertEqual(value_updater.call_count, 2)

    def test_close(self):
        """Test close method"""
        value_updater = MagicMock()
        self.strategy.prefetch(value_updater)

        self.strategy.close()

        # After close, new prefetch should work
        value_updater2 = MagicMock()
        self.strategy.prefetch(value_updater2)
        value_updater2.assert_called_once()

    def test_exception_handling(self):
        """Test that flag is cleared even when value_updater raises exception"""

        def failing_updater():
            raise ValueError("Test exception")

        # Flag should not be set initially
        self.assertFalse(self.strategy._currently_refreshing.is_set())

        # Prefetch with failing updater
        with self.assertRaises(ValueError):
            self.strategy.prefetch(failing_updater)

        # Flag should be cleared after exception (due to finally block)
        self.assertFalse(self.strategy._currently_refreshing.is_set())

    def test_multiple_concurrent_threads(self):
        """Test prefetch with multiple concurrent threads (only one should execute)"""
        call_count = [0]
        event = threading.Event()

        def slow_updater():
            call_count[0] += 1
            time.sleep(0.2)
            event.set()

        threads = []
        for _ in range(5):
            thread = threading.Thread(target=self.strategy.prefetch, args=(slow_updater,))
            thread.start()
            threads.append(thread)

        # Wait for operation to complete
        event.wait(timeout=1.0)
        time.sleep(0.1)

        for thread in threads:
            thread.join(timeout=0.1)

        # Should have been called exactly once
        self.assertEqual(call_count[0], 1)

    def test_close_while_refreshing(self):
        """Test close called while a refresh is in progress"""
        call_count = [0]
        event = threading.Event()

        def slow_updater():
            call_count[0] += 1
            time.sleep(0.2)
            event.set()

        # Start prefetch in a thread
        thread = threading.Thread(target=self.strategy.prefetch, args=(slow_updater,))
        thread.start()

        # Wait for refresh to start
        time.sleep(0.01)

        # Call close while refresh is in progress
        self.strategy.close()

        # Wait for thread to complete
        event.wait(timeout=1.0)
        thread.join(timeout=0.5)

        # Updater should have completed (close just clears the flag)
        self.assertEqual(call_count[0], 1)

    def test_flag_cleared_on_completion(self):
        """Test that flag is properly cleared after prefetch completes"""
        value_updater = MagicMock()

        # Flag should not be set initially
        self.assertFalse(self.strategy._currently_refreshing.is_set())

        # Prefetch
        self.strategy.prefetch(value_updater)

        # Flag should be cleared after completion
        self.assertFalse(self.strategy._currently_refreshing.is_set())

    def test_flag_set_during_prefetch(self):
        """Test that flag is set during prefetch"""
        flag_during_call = [False]

        def check_flag_updater():
            flag_during_call[0] = self.strategy._currently_refreshing.is_set()

        self.strategy.prefetch(check_flag_updater)

        # Flag should have been set during the call
        self.assertTrue(flag_during_call[0])

    def test_concurrent_after_completion(self):
        """Test that concurrent calls work after previous prefetch completes"""
        call_count = [0]

        def counting_updater():
            call_count[0] += 1

        # First prefetch
        self.strategy.prefetch(counting_updater)
        self.assertEqual(call_count[0], 1)

        # Small delay to ensure completion
        time.sleep(0.05)

        # Second prefetch should execute
        self.strategy.prefetch(counting_updater)
        self.assertEqual(call_count[0], 2)

    def test_immediate_repeated_calls(self):
        """Test that repeated immediate calls are skipped"""
        call_count = [0]

        def slow_updater():
            call_count[0] += 1
            time.sleep(0.1)

        # Start first prefetch
        thread = threading.Thread(target=self.strategy.prefetch, args=(slow_updater,))
        thread.start()

        # Immediately try multiple more prefetches
        for _ in range(5):
            self.strategy.prefetch(slow_updater)

        thread.join()

        # Should have been called only once
        self.assertEqual(call_count[0], 1)


if __name__ == "__main__":
    unittest.main()
