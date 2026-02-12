"""
IDaaS Python SDK - Abstract Refreshed Credential Provider

This module provides an abstract base class for credential providers
that support automatic credential refresh.
"""

from typing import Generic, TypeVar

from cloud_idaas.core.cache.cached_result_supplier import CachedResultSupplier
from cloud_idaas.core.cache.refresh_result import RefreshResult
from cloud_idaas.core.cache.stale_value_behavior import StaleValueBehavior
from cloud_idaas.core.cache.strategy.non_blocking_prefetch_strategy import NonBlockingPrefetchStrategy
from cloud_idaas.core.cache.strategy.one_caller_blocks_prefetch_strategy import OneCallerBlocksPrefetchStrategy

T = TypeVar("T")


class AbstractRefreshedCredentialProvider(Generic[T]):
    """
    Abstract base class for credential providers that support automatic
    credential refresh with caching.

    Type Parameters:
        T: The type of the credential
    """

    def __init__(
        self,
        async_credential_update_enabled: bool = False,
        stale_value_behavior: StaleValueBehavior = StaleValueBehavior.STRICT,
    ):
        """
        Initialize the abstract refreshed credential provider.

        Args:
            async_credential_update_enabled: Whether to enable async credential update.
            stale_value_behavior: Behavior when cached value is stale.
        """
        self._async_credential_update_enabled = async_credential_update_enabled
        self._stale_value_behavior = stale_value_behavior

        # Choose prefetch strategy based on async setting
        if async_credential_update_enabled:
            prefetch_strategy = NonBlockingPrefetchStrategy()
        else:
            prefetch_strategy = OneCallerBlocksPrefetchStrategy()

        # Create cached result supplier
        self._cached_result_supplier = CachedResultSupplier(
            value_supplier=self._refresh_credential,
            prefetch_strategy=prefetch_strategy,
            stale_value_behavior=stale_value_behavior,
        )

    def is_async_credential_update_enabled(self) -> bool:
        """Check if async credential update is enabled."""
        return self._async_credential_update_enabled

    def get_cached_result_supplier(self) -> CachedResultSupplier[T]:
        """Get the cached result supplier."""
        return self._cached_result_supplier

    def _refresh_credential(self) -> RefreshResult[T]:
        """
        Refresh the credential. Subclasses must implement this method.

        Returns:
            RefreshResult containing the new credential and timing information.

        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError("Subclasses must implement _refresh_credential method")

    def close(self) -> None:
        """Close any resources used by this provider."""
        if self._cached_result_supplier:
            self._cached_result_supplier._prefetch_strategy.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
