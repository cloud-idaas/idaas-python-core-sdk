"""
IDaaS Python SDK - One Caller Blocks Prefetch Strategy

This module provides the OneCallerBlocks strategy implementation.
The simplest strategy: only one caller will be blocked and execute the update operation,
other callers return immediately.
"""

import threading
from typing import Callable

from cloud_idaas.core.cache.prefetch_strategy import PrefetchStrategy


class OneCallerBlocksPrefetchStrategy(PrefetchStrategy):
    """
    OneCallerBlocks strategy implementation.
    The simplest strategy: only one caller will be blocked and execute the update operation,
    other callers return immediately.
    """

    def __init__(self):
        """Initialize the OneCallerBlocksPrefetchStrategy."""
        self._currently_refreshing = threading.Event()

    def prefetch(self, value_updater: Callable[[], None]) -> None:
        """
        Prefetch operation executed when the prefetch time is reached.

        Args:
            value_updater: Value updater, responsible for executing the specific
                          value refresh operation.
        """
        if not self._currently_refreshing.is_set():
            self._currently_refreshing.set()
            try:
                value_updater()
            finally:
                self._currently_refreshing.clear()

    def close(self) -> None:
        """Clear the refresh flag."""
        self._currently_refreshing.clear()
