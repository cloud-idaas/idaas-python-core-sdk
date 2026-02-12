"""
IDaaS Python SDK - Cached Result Supplier

This module provides a time-based caching mechanism, including expiration checking,
prefetching strategy and other features.
"""

import logging
import random
import threading
from datetime import datetime, timedelta, timezone
from typing import Callable, Generic, Optional, TypeVar

from cloud_idaas.core.cache.prefetch_strategy import PrefetchStrategy
from cloud_idaas.core.cache.refresh_result import RefreshResult
from cloud_idaas.core.cache.stale_value_behavior import StaleValueBehavior
from cloud_idaas.core.exceptions import CacheException, ConcurrentOperationException

T = TypeVar("T")

# Default maximum blocking refresh wait time
BLOCKING_REFRESH_MAX_WAIT = timedelta(seconds=5)

# Jitter start time
JITTER_START = timedelta(minutes=5)

# Jitter range
JITTER_RANGE = timedelta(minutes=5)


def _get_current_time() -> datetime:
    """Get current UTC time."""
    return datetime.now(timezone.utc)


class CachedResultSupplier(Generic[T]):
    """
    CachedResultSupplier is the core class of the caching mechanism.
    It provides a time-based caching mechanism, including expiration checking,
    prefetching strategy and other features.

    Type Parameters:
        T: The type of the cached value
    """

    def __init__(
        self,
        value_supplier: Callable[[], RefreshResult[T]],
        prefetch_strategy: Optional[PrefetchStrategy] = None,
        clock: Optional[Callable[[], datetime]] = None,
        stale_value_behavior: StaleValueBehavior = StaleValueBehavior.ALLOW,
    ):
        """
        Initialize the CachedResultSupplier.

        Args:
            value_supplier: Value supplier, used to retrieve new values.
            prefetch_strategy: Prefetch strategy (defaults to OneCallerBlocksPrefetchStrategy).
            clock: Clock source, pluggable for easier testing (defaults to UTC time).
            stale_value_behavior: Stale value behavior strategy.
        """
        self._value_supplier = value_supplier
        self._prefetch_strategy = prefetch_strategy
        self._clock = clock or _get_current_time
        self._stale_value_behavior = stale_value_behavior
        self._cached_value: Optional[RefreshResult[T]] = None
        self._refresh_lock = threading.Lock()
        self._logger = logging.getLogger(__name__)

    def get(self) -> T:
        """
        Get cached value.

        Returns:
            The cached value.

        Raises:
            ConcurrentOperationException: If concurrent operation fails.
            CacheException: If cache refresh fails in strict mode.
        """
        local_cached_value = self._cached_value

        # Check if cache has expired
        if self._cache_is_stale(local_cached_value):
            self._refresh_cache()
            local_cached_value = self._cached_value

        # Confirm
        if local_cached_value is None:
            raise ConcurrentOperationException()

        # Check if prefetching is needed
        if self._should_initiate_cache_prefetch(local_cached_value):
            self._prefetch_strategy.prefetch(self._refresh_cache)

        return local_cached_value.value

    def _cache_is_stale(self, refresh_result: Optional[RefreshResult[T]]) -> bool:
        """
        Check if cache has expired.

        Args:
            refresh_result: The cache result.

        Returns:
            True if expired, otherwise False.
        """
        if refresh_result is None:
            return True
        stale_time = refresh_result.stale_time
        return stale_time is not None and self._clock() > stale_time

    def _should_initiate_cache_prefetch(self, refresh_result: Optional[RefreshResult[T]]) -> bool:
        """
        Check if cache prefetching should be initiated.

        Args:
            refresh_result: The cache result.

        Returns:
            True if prefetching should be initiated, otherwise False.
        """
        if refresh_result is None:
            return False
        prefetch_time = refresh_result.prefetch_time
        return prefetch_time is not None and self._clock() > prefetch_time

    def _refresh_cache(self) -> None:
        """Refresh cache."""
        lock_acquired = False
        try:
            # Try to acquire the lock, waiting up to specified time
            lock_acquired = self._refresh_lock.acquire(timeout=BLOCKING_REFRESH_MAX_WAIT.total_seconds())
            if not lock_acquired:
                # Failed to acquire lock due to timeout, just return current value
                self._logger.error("Failed to acquire refresh lock")
                return

            # Double-check if refresh is still needed
            if not self._cache_is_stale(self._cached_value):
                return

            # Execute the actual refresh logic
            try:
                refreshed_value = self._value_supplier()
                # Apply jitter
                self._handle_fetched_success(refreshed_value)
            except Exception as e:
                # Handle refresh failure
                self._handle_fetch_failure(e)
        finally:
            if lock_acquired:
                self._refresh_lock.release()

    def _handle_fetched_success(self, refreshed_value: RefreshResult[T]) -> None:
        """
        Handle the newly fetched value.

        Args:
            refreshed_value: The newly fetched value.
        """
        # Apply jitter to stale_time and prefetch_time
        stale_time = refreshed_value.stale_time
        prefetch_time = refreshed_value.prefetch_time

        if stale_time is not None:
            stale_time = self._jitter_time(stale_time)

        if prefetch_time is not None:
            prefetch_time = self._jitter_time(prefetch_time)

        # Update cached value
        self._cached_value = RefreshResult(refreshed_value.value, stale_time, prefetch_time)

    def _handle_fetch_failure(self, exception: Exception) -> None:
        """
        Handle failure when fetching value.

        Args:
            exception: The exception that occurred.

        Raises:
            CacheException: If stale value behavior is STRICT.
        """
        if self._stale_value_behavior == StaleValueBehavior.STRICT:
            raise CacheException(cause=exception)
        else:
            self._logger.info("Failed to refresh cache, using the old value")

    def _jitter_time(self, time: datetime) -> datetime:
        """
        Apply jitter to specified time.

        Args:
            time: Original time.

        Returns:
            Time with added jitter.
        """
        jitter_seconds = JITTER_RANGE.total_seconds()
        if jitter_seconds <= 0:
            return time

        jitter_amount = abs(random.random() * jitter_seconds)
        return time + JITTER_START + timedelta(seconds=jitter_amount)
