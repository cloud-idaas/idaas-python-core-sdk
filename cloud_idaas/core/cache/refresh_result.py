"""
IDaaS Python SDK - Refresh Result

This module provides a result class encapsulating the cache value
and related expiration time and prefetch time information.
"""

from datetime import datetime
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class RefreshResult(Generic[T]):
    """
    Result class encapsulating the cache value and related expiration time
    and prefetch time information.

    Type Parameters:
        T: Type of the cached value
    """

    def __init__(self, value: T, stale_time: Optional[datetime] = None, prefetch_time: Optional[datetime] = None):
        """
        Constructs a new RefreshResult instance.

        Args:
            value: The actual cached value.
            stale_time: Expiration time, after which all threads will block waiting for update.
            prefetch_time: Prefetch time, after which prefetch operation will be triggered.
        """
        self._value = value
        self._stale_time = stale_time
        self._prefetch_time = prefetch_time

    @property
    def value(self) -> T:
        """Gets the actual cached value."""
        return self._value

    @property
    def stale_time(self) -> Optional[datetime]:
        """Gets the expiration time."""
        return self._stale_time

    @property
    def prefetch_time(self) -> Optional[datetime]:
        """Gets the prefetch time."""
        return self._prefetch_time

    def __eq__(self, other) -> bool:
        """Check equality with another RefreshResult."""
        if not isinstance(other, RefreshResult):
            return False
        return (
            self._value == other._value
            and self._stale_time == other._stale_time
            and self._prefetch_time == other._prefetch_time
        )

    def __hash__(self) -> int:
        """Get hash of this RefreshResult."""
        return hash((self._value, self._stale_time, self._prefetch_time))

    def __repr__(self) -> str:
        """String representation of this RefreshResult."""
        return f"RefreshResult[value={self._value}, stale_time={self._stale_time}, prefetch_time={self._prefetch_time}]"

    @staticmethod
    def builder(value: T) -> "RefreshResultBuilder[T]":
        """
        Create a builder for RefreshResult.

        Args:
            value: The cached value.

        Returns:
            A RefreshResultBuilder instance.
        """
        return RefreshResultBuilder(value)


class RefreshResultBuilder(Generic[T]):
    """Builder class for constructing RefreshResult instances."""

    def __init__(self, value: T):
        """
        Initialize the builder with a value.

        Args:
            value: The cached value.
        """
        self._value = value
        self._stale_time: Optional[datetime] = None
        self._prefetch_time: Optional[datetime] = None

    def stale_time(self, stale_time: datetime) -> "RefreshResultBuilder[T]":
        """
        Set the stale time.

        Args:
            stale_time: The expiration time.

        Returns:
            This builder instance for method chaining.
        """
        self._stale_time = stale_time
        return self

    def prefetch_time(self, prefetch_time: datetime) -> "RefreshResultBuilder[T]":
        """
        Set the prefetch time.

        Args:
            prefetch_time: The prefetch time.

        Returns:
            This builder instance for method chaining.
        """
        self._prefetch_time = prefetch_time
        return self

    def build(self) -> RefreshResult[T]:
        """
        Build the RefreshResult instance.

        Returns:
            A RefreshResult instance with the configured values.
        """
        return RefreshResult(self._value, self._stale_time, self._prefetch_time)
