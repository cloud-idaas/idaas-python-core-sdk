"""
Tests for PrefetchStrategy base class
"""

import unittest
from unittest.mock import MagicMock

from cloud_idaas.core.cache.prefetch_strategy import PrefetchStrategy
from cloud_idaas.core.cache.strategy.non_blocking_prefetch_strategy import NonBlockingPrefetchStrategy
from cloud_idaas.core.cache.strategy.one_caller_blocks_prefetch_strategy import OneCallerBlocksPrefetchStrategy


class TestPrefetchStrategy(unittest.TestCase):
    """Test cases for PrefetchStrategy base class"""

    def test_prefetch_raises_not_implemented(self):
        """Test that prefetch raises NotImplementedError in base class"""
        strategy = PrefetchStrategy()
        value_updater = MagicMock()

        with self.assertRaises(NotImplementedError):
            strategy.prefetch(value_updater)

    def test_close_no_op(self):
        """Test that close does nothing in base class"""
        strategy = PrefetchStrategy()
        # Should not raise any exception
        strategy.close()

    def test_context_manager_exit_calls_close(self):
        """Test that context manager __exit__ calls close"""

        class TestStrategy(PrefetchStrategy):
            def __init__(self):
                super().__init__()
                self.close_called = False

            def close(self):
                self.close_called = True

        with TestStrategy() as strategy:
            self.assertFalse(strategy.close_called)

        # After exiting context, close should have been called
        self.assertTrue(strategy.close_called)

    def test_context_manager_returns_self_on_enter(self):
        """Test that context manager __enter__ returns self"""
        strategy = OneCallerBlocksPrefetchStrategy()

        with strategy as ctx:
            self.assertIs(ctx, strategy)

    def test_context_manager_with_exception(self):
        """Test context manager behavior with exception"""
        strategy = OneCallerBlocksPrefetchStrategy()
        close_called = [False]

        # Override close to track calls
        original_close = strategy.close

        def track_close():
            close_called[0] = True
            original_close()

        strategy.close = track_close

        try:
            with strategy:
                raise ValueError("Test exception")
        except ValueError:
            pass

        # Close should still be called even with exception
        self.assertTrue(close_called[0])

    def test_context_manager_enter_idempotent(self):
        """Test that multiple __enter__ calls work correctly"""
        strategy = OneCallerBlocksPrefetchStrategy()

        with strategy:
            with strategy:
                # Nested context managers should work
                pass


class TestPrefetchStrategySubclasses(unittest.TestCase):
    """Test PrefetchStrategy implementations"""

    def test_one_caller_blocks_prefetch_as_context_manager(self):
        """Test OneCallerBlocksPrefetchStrategy as context manager"""
        with OneCallerBlocksPrefetchStrategy() as strategy:
            value_updater = MagicMock()
            strategy.prefetch(value_updater)
            value_updater.assert_called_once()

    def test_non_blocking_prefetch_as_context_manager(self):
        """Test NonBlockingPrefetchStrategy as context manager"""
        import time

        with NonBlockingPrefetchStrategy() as strategy:
            value_updater = MagicMock()
            strategy.prefetch(value_updater)
            time.sleep(0.5)
            value_updater.assert_called_once()

    def test_context_manager_reusability(self):
        """Test that strategies can be reused after context exit"""
        strategy = OneCallerBlocksPrefetchStrategy()

        with strategy:
            pass

        # Can be used again after exiting
        with strategy:
            value_updater = MagicMock()
            strategy.prefetch(value_updater)
            value_updater.assert_called_once()

    def test_context_manager_explicit_close(self):
        """Test that explicit close also works"""
        strategy = OneCallerBlocksPrefetchStrategy()

        with strategy:
            value_updater = MagicMock()
            strategy.prefetch(value_updater)

        # After explicit context exit, can still call close
        strategy.close()
        # Should not raise exception


if __name__ == "__main__":
    unittest.main()
