"""
Unit tests for StaticOidcTokenProvider
"""

from cloud_idaas import (
    StaticOidcTokenProvider,
)


class TestStaticOidcTokenProvider:
    """Test cases for StaticOidcTokenProvider."""

    def test_initialization_with_token(self):
        """Test initialization with OIDC token."""
        provider = StaticOidcTokenProvider("test_oidc_token")
        assert provider._oidc_token == "test_oidc_token"

    def test_initialization_without_token(self):
        """Test initialization without OIDC token."""
        provider = StaticOidcTokenProvider()
        assert provider._oidc_token is None

    def test_get_oidc_token(self):
        """Test getting OIDC token."""
        provider = StaticOidcTokenProvider("test_oidc_token")
        token = provider.get_oidc_token()
        assert token == "test_oidc_token"

    def test_get_oidc_token_returns_none_when_not_set(self):
        """Test that get_oidc_token returns None when token is not set."""
        provider = StaticOidcTokenProvider()
        token = provider.get_oidc_token()
        assert token is None

    def test_set_oidc_token(self):
        """Test setting OIDC token."""
        provider = StaticOidcTokenProvider()
        provider.set_oidc_token("new_oidc_token")
        assert provider.get_oidc_token() == "new_oidc_token"

    def test_set_oidc_token_overwrites_existing(self):
        """Test that setting OIDC token overwrites existing value."""
        provider = StaticOidcTokenProvider("old_token")
        provider.set_oidc_token("new_oidc_token")
        assert provider.get_oidc_token() == "new_oidc_token"

    def test_multiple_get_oidc_token_calls(self):
        """Test that multiple get_oidc_token calls return the same value."""
        provider = StaticOidcTokenProvider("test_oidc_token")
        token1 = provider.get_oidc_token()
        token2 = provider.get_oidc_token()
        assert token1 == token2 == "test_oidc_token"
