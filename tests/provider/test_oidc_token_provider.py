"""
Unit tests for OidcTokenProvider
"""

import pytest

from cloud_idaas.core.provider import OidcTokenProvider


class MockOidcTokenProvider(OidcTokenProvider):
    """Mock implementation of OidcTokenProvider for testing."""

    def __init__(self, token=None):
        self._token = token

    def get_oidc_token(self):
        return self._token


class TestOidcTokenProvider:
    """Test cases for OidcTokenProvider."""

    def test_get_oidc_token_returns_value(self):
        """Test that get_oidc_token returns the configured value."""
        provider = MockOidcTokenProvider("test_oidc_token")
        assert provider.get_oidc_token() == "test_oidc_token"

    def test_get_oidc_token_returns_none(self):
        """Test that get_oidc_token returns None when not configured."""
        provider = MockOidcTokenProvider()
        assert provider.get_oidc_token() is None

    def test_is_abstract_class(self):
        """Test that OidcTokenProvider is an abstract class."""
        with pytest.raises(TypeError):
            # Cannot instantiate abstract class directly
            OidcTokenProvider()

    def test_mock_implementation_works(self):
        """Test that mock implementation works correctly."""
        provider = MockOidcTokenProvider("oidc.token.here")
        assert provider.get_oidc_token() == "oidc.token.here"

    def test_multiple_get_calls_return_same_value(self):
        """Test that multiple get_oidc_token calls return same value."""
        provider = MockOidcTokenProvider("consistent_token")
        assert provider.get_oidc_token() == provider.get_oidc_token()

    def test_get_oidc_token_with_empty_string(self):
        """Test get_oidc_token with empty string."""
        provider = MockOidcTokenProvider("")
        assert provider.get_oidc_token() == ""

    def test_get_oidc_token_with_long_token(self):
        """Test get_oidc_token with a long token string."""
        long_token = "a" * 1000
        provider = MockOidcTokenProvider(long_token)
        assert provider.get_oidc_token() == long_token
        assert len(provider.get_oidc_token()) == 1000
