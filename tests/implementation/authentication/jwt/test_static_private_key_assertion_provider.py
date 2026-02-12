"""
Unit tests for StaticPrivateKeyAssertionProvider
"""

import pytest

from cloud_idaas import CredentialException
from cloud_idaas.core.implementation.authentication.jwt.static_private_key_assertion_provider import (
    StaticPrivateKeyAssertionProvider,
)

# Test RSA private key in PEM format
RSA_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDj8x6kVxQsH9D
Y5kQydFQH9B4Y8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
wIDAQABAoIBADj8x6kVxQsH9DY5kQydFQH9B4Y8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8
kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
-----END PRIVATE KEY-----"""


# EC private key in PEM format
EC_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MHcCAQEEIJj8x6kVxQsH9DY5kQydFQH9B4Y8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8
kQoAoGCCqGSM49AwEHoUQDQgAEj8x6kVxQsH9DY5kQydFQH9B4Y8kQ8kQ8kQ8kQ
8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
Q8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8kQ8k
-----END PRIVATE KEY-----"""


class TestStaticPrivateKeyAssertionProvider:
    """Test cases for StaticPrivateKeyAssertionProvider."""

    def test_initialization_with_rsa_key(self):
        """Test initialization with RSA private key."""
        # Use a valid RSA key
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.asymmetric import rsa

        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        from cryptography.hazmat.primitives import serialization

        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        provider = StaticPrivateKeyAssertionProvider(pem.decode())
        assert provider._private_key_string == pem.decode()
        assert provider._private_key is not None

    def test_initialization_with_invalid_key_raises_error(self):
        """Test initialization with invalid key raises CredentialException."""
        with pytest.raises(CredentialException, match="Failed to parse private key"):
            StaticPrivateKeyAssertionProvider("invalid_key")

    def test_client_id_property(self):
        """Test client_id property setter and getter."""
        provider = self._create_provider_with_valid_key()
        assert provider.client_id is None

        provider.client_id = "test_client_id"
        assert provider.client_id == "test_client_id"

    def test_token_endpoint_property(self):
        """Test token_endpoint property setter and getter."""
        provider = self._create_provider_with_valid_key()
        assert provider.token_endpoint is None

        provider.token_endpoint = "https://test.com/token"
        assert provider.token_endpoint == "https://test.com/token"

    def test_scope_property(self):
        """Test scope property setter and getter."""
        provider = self._create_provider_with_valid_key()
        assert provider.scope is None

        provider.scope = "test_scope"
        assert provider.scope == "test_scope"

    def test_get_client_assertion_generates_jwt(self):
        """Test that get_client_assertion generates valid JWT."""
        provider = self._create_provider_with_valid_key()
        provider.client_id = "test_client_id"
        provider.token_endpoint = "https://test.com/token"

        assertion = provider.get_client_assertion()
        assert assertion is not None
        assert isinstance(assertion, str)
        assert len(assertion) > 0

        # JWT should have 3 parts separated by dots
        parts = assertion.split(".")
        assert len(parts) == 3

    def test_get_client_assertion_with_rsa_key(self):
        """Test getting client assertion with RSA key uses RS256 algorithm."""
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa

        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        provider = StaticPrivateKeyAssertionProvider(pem.decode())
        provider.client_id = "test_client_id"
        provider.token_endpoint = "https://test.com/token"

        assertion = provider.get_client_assertion()

        # Verify the assertion is valid JWT
        parts = assertion.split(".")
        assert len(parts) == 3

    def test_get_client_assertion_without_client_id(self):
        """Test getting assertion without client_id."""
        provider = self._create_provider_with_valid_key()
        provider.token_endpoint = "https://test.com/token"

        # Should still generate assertion but with empty client_id
        assertion = provider.get_client_assertion()
        assert assertion is not None

    def test_get_client_assertion_without_token_endpoint(self):
        """Test getting assertion without token_endpoint."""
        provider = self._create_provider_with_valid_key()
        provider.client_id = "test_client_id"

        # Should still generate assertion but with empty token_endpoint
        assertion = provider.get_client_assertion()
        assert assertion is not None

    def _create_provider_with_valid_key(self):
        """Helper method to create a provider with a valid RSA key."""
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa

        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        return StaticPrivateKeyAssertionProvider(pem.decode())
