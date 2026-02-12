"""
Unit tests for AbstractRefreshedCredentialProvider
"""

import pytest

from cloud_idaas import AbstractRefreshedCredentialProvider, RefreshResult, StaleValueBehavior


class MockRefreshedCredentialProvider(AbstractRefreshedCredentialProvider[str]):
    """Mock implementation of AbstractRefreshedCredentialProvider for testing."""

    def __init__(self, async_enabled=False, stale_behavior=StaleValueBehavior.STRICT, refresh_result=None):
        super().__init__(async_enabled, stale_behavior)
        self._refresh_result = refresh_result

    def _refresh_credential(self) -> RefreshResult[str]:
        if self._refresh_result:
            return self._refresh_result
        return RefreshResult.builder("test_value").build()


class TestAbstractRefreshedCredentialProvider:
    """Test cases for AbstractRefreshedCredentialProvider."""

    def test_initialization_with_defaults(self):
        """Test initialization with default parameters."""
        provider = MockRefreshedCredentialProvider()
        assert not provider.is_async_credential_update_enabled()
        assert provider.get_cached_result_supplier() is not None

    def test_initialization_with_async_enabled(self):
        """Test initialization with async credential update enabled."""
        provider = MockRefreshedCredentialProvider(async_enabled=True)
        assert provider.is_async_credential_update_enabled()

    def test_initialization_with_allow_stale_behavior(self):
        """Test initialization with ALLOW stale value behavior."""
        provider = MockRefreshedCredentialProvider(stale_behavior=StaleValueBehavior.ALLOW)
        assert provider.get_cached_result_supplier() is not None

    def test_get_cached_result_supplier(self):
        """Test getting the cached result supplier."""
        provider = MockRefreshedCredentialProvider()
        supplier = provider.get_cached_result_supplier()
        assert supplier is not None

    def test_close(self):
        """Test closing the provider."""
        provider = MockRefreshedCredentialProvider()
        provider.close()
        # Should not raise an exception

    def test_context_manager(self):
        """Test using provider as context manager."""
        with MockRefreshedCredentialProvider() as provider:
            assert provider is not None
            assert provider.get_cached_result_supplier() is not None

    def test_context_manager_with_exception(self):
        """Test context manager handles exceptions properly."""
        with pytest.raises(ValueError):
            with MockRefreshedCredentialProvider() as provider:
                raise ValueError("Test exception")

    def test_refresh_credential_not_implemented(self):
        """Test that _refresh_credential raises NotImplementedError in abstract class."""

        # Create a minimal mock that doesn't implement _refresh_credential
        class MinimalMock(AbstractRefreshedCredentialProvider[str]):
            pass

        provider = MinimalMock()
        with pytest.raises(NotImplementedError, match="Subclasses must implement _refresh_credential"):
            provider._refresh_credential()

    def test_get_value_from_supplier(self):
        """Test getting value from the cached result supplier."""
        from datetime import datetime, timedelta, timezone

        now = datetime.now(timezone.utc)
        stale_time = now + timedelta(hours=1)
        prefetch_time = now + timedelta(minutes=30)

        refresh_result = RefreshResult.builder("test_value").stale_time(stale_time).prefetch_time(prefetch_time).build()
        provider = MockRefreshedCredentialProvider(refresh_result=refresh_result)

        value = provider.get_cached_result_supplier().get()
        assert value == "test_value"
