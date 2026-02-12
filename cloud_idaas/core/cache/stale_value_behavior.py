"""
IDaaS Python SDK - Stale Value Behavior

This module provides an enum for stale value behavior strategy.
"""

from enum import Enum


class _StrEnum(Enum):
    """
    Base enum class that returns the value when converted to string.
    """

    def __str__(self) -> str:
        return self.value


class StaleValueBehavior(_StrEnum):
    """
    Enum for stale value behavior strategy.
    Defines how to handle stale values when cache refresh fails.
    """

    """
    Strict mode: throws exception if refresh fails.
    """
    STRICT = "STRICT"

    """
    Lenient mode: allows returning stale value and retries within a certain time.
    """
    ALLOW = "ALLOW"
