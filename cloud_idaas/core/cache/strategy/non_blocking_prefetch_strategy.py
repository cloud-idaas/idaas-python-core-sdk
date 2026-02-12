"""
IDaaS Python SDK - Non Blocking Prefetch Strategy

This module provides the NonBlocking strategy implementation.
Non-blocking strategy: Uses a background thread pool to asynchronously update the cache.
"""

import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from cloud_idaas.core.cache.prefetch_strategy import PrefetchStrategy

MAX_CONCURRENT_REFRESHES = 100
THREAD_POOL_KEEP_ALIVE_SECONDS = 60

_logger = logging.getLogger(__name__)


class NonBlockingPrefetchStrategy(PrefetchStrategy):
    """
    NonBlocking strategy implementation.
    Non-blocking strategy: Uses a background thread pool to asynchronously update the cache.
    """

    # Global executor service for all NonBlocking instances
    _executor: ThreadPoolExecutor = ThreadPoolExecutor(
        max_workers=1,
        thread_name_prefix="idaas-python-core-sdk-non-blocking-refresh",
    )

    # Semaphore for concurrent refresh leases
    _concurrent_refresh_lease = threading.Semaphore(MAX_CONCURRENT_REFRESHES)

    def __init__(self):
        """Initialize the NonBlockingPrefetchStrategy."""
        self._currently_prefetching = threading.Event()

    def prefetch(self, value_updater: Callable[[], None]) -> None:
        """
        Prefetch operation executed when the prefetch time is reached.

        Args:
            value_updater: Value updater, responsible for executing the specific
                          value refresh operation.
        """
        if not self._concurrent_refresh_lease.acquire(blocking=False):
            _logger.warning("Only %d concurrent refreshes are allowed", MAX_CONCURRENT_REFRESHES)
            return

        if not self._currently_prefetching.is_set():
            self._currently_prefetching.set()
            try:
                self._executor.submit(self._run_with_cleanup, value_updater)
            except Exception:
                self._currently_prefetching.clear()
                self._concurrent_refresh_lease.release()
        else:
            self._concurrent_refresh_lease.release()

    def _run_with_cleanup(self, value_updater: Callable[[], None]) -> None:
        """
        Run the value updater with cleanup.

        Args:
            value_updater: Value updater.
        """
        try:
            value_updater()
        finally:
            self._currently_prefetching.clear()
            self._concurrent_refresh_lease.release()

    @classmethod
    def shutdown_executor(cls) -> None:
        """Shutdown the global executor service."""
        cls._executor.shutdown(wait=True)

    def close(self) -> None:
        """Clear the prefetching flag."""
        self._currently_prefetching.clear()
