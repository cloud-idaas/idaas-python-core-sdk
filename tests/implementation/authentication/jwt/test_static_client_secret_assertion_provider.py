"""
Unit tests for StaticClientSecretAssertionProvider
"""

import pytest

from cloud_idaas import (
    CredentialException,
    StaticClientSecretAssertionProvider,
)


class TestStaticClientSecretAssertionProvider:
    """Test cases for StaticClientSecretAssertionProvider."""

    def test_initialization(self):
        """Test initialization with client secret supplier."""
        supplier = lambda: "test_secret"
        provider = StaticClientSecretAssertionProvider(supplier)
        assert provider._client_secret_supplier == supplier

    def test_client_id_property(self):
        """Test client_id property setter and getter."""
        provider = StaticClientSecretAssertionProvider(lambda: "test_secret")
        assert provider.client_id is None

        provider.client_id = "test_client_id"
        assert provider.client_id == "test_client_id"

    def test_token_endpoint_property(self):
        """Test token_endpoint property setter and getter."""
        provider = StaticClientSecretAssertionProvider(lambda: "test_secret")
        assert provider.token_endpoint is None

        provider.token_endpoint = "https://test.com/token"
        assert provider.token_endpoint == "https://test.com/token"

    def test_scope_property(self):
        """Test scope property setter and getter."""
        provider = StaticClientSecretAssertionProvider(lambda: "test_secret")
        assert provider.scope is None

        provider.scope = "test_scope"
        assert provider.scope == "test_scope"

    def test_get_client_assertion(self):
        """Test getting client assertion."""
        provider = StaticClientSecretAssertionProvider(lambda: "test_secret")
        provider.client_id = "test_client_id"
        provider.token_endpoint = "https://test.com/token"

        assertion = provider.get_client_assertion()
        assert assertion is not None
        assert isinstance(assertion, str)
        assert len(assertion) > 0

    def test_get_client_assertion_generates_valid_jwt(self):
        """Test that client assertion generates valid JWT structure."""
        provider = StaticClientSecretAssertionProvider(lambda: "test_secret")
        provider.client_id = "test_client_id"
        provider.token_endpoint = "https://test.com/token"

        assertion = provider.get_client_assertion()

        # JWT should have 3 parts separated by dots
        parts = assertion.split(".")
        assert len(parts) == 3

    def test_get_client_assertion_with_different_secrets(self):
        """Test that different secrets produce different assertions."""
        provider1 = StaticClientSecretAssertionProvider(lambda: "secret1")
        provider1.client_id = "test_client_id"
        provider1.token_endpoint = "https://test.com/token"

        provider2 = StaticClientSecretAssertionProvider(lambda: "secret2")
        provider2.client_id = "test_client_id"
        provider2.token_endpoint = "https://test.com/token"

        assertion1 = provider1.get_client_assertion()
        assertion2 = provider2.get_client_assertion()

        # Different secrets should produce different assertions
        assert assertion1 != assertion2

    def test_get_client_assertion_without_client_id_raises_error(self):
        """Test that getting assertion without client_id raises CredentialException."""
        provider = StaticClientSecretAssertionProvider(lambda: "test_secret")
        provider.token_endpoint = "https://test.com/token"

        with pytest.raises(CredentialException):
            provider.get_client_assertion()

    def test_get_client_assertion_without_token_endpoint_raises_error(self):
        """Test that getting assertion without token_endpoint raises CredentialException."""
        provider = StaticClientSecretAssertionProvider(lambda: "test_secret")
        provider.client_id = "test_client_id"

        with pytest.raises(CredentialException):
            provider.get_client_assertion()
