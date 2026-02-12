"""
IDaaS Python SDK - Prefetch Strategy

This module provides an interface for prefetch strategies.
"""

from typing import Callable


class PrefetchStrategy:
    """
    Prefetch strategy interface, defining the behavior when the prefetch time is reached.
    """

    def prefetch(self, value_updater: Callable[[], None]) -> None:
        """
        Prefetch operation executed when the prefetch time is reached.

        Args:
            value_updater: Value updater, responsible for executing the specific
                          value refresh operation.
        """
        raise NotImplementedError("Subclasses must implement prefetch method")

    def close(self) -> None:
        """Close any resources used by this prefetch strategy."""
        pass

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
