"""
Unit tests for IDaaSCredentialProvider
"""

from unittest.mock import Mock

import pytest

from cloud_idaas import IDaaSCredential
from cloud_idaas.core.provider import IDaaSCredentialProvider


class MockIDaaSCredentialProvider(IDaaSCredentialProvider):
    """Mock implementation of IDaaSCredentialProvider for testing."""

    def __init__(self, credential=None):
        self._credential = credential

    def get_credential(self):
        return self._credential


class TestIDaaSCredentialProvider:
    """Test cases for IDaaSCredentialProvider."""

    def test_get_credential_returns_none_when_not_implemented(self):
        """Test that get_credential returns None by default."""
        # Create a mock that doesn't set credential
        provider = MockIDaaSCredentialProvider()
        assert provider.get_credential() is None

    def test_get_credential_returns_credential(self):
        """Test that get_credential returns the credential."""
        mock_credential = Mock(spec=IDaaSCredential)
        provider = MockIDaaSCredentialProvider(mock_credential)
        assert provider.get_credential() == mock_credential

    def test_get_bearer_token_with_credential(self):
        """Test get_bearer_token with valid credential."""
        mock_credential = Mock(spec=IDaaSCredential)
        mock_credential.get_access_token.return_value = "test_token"
        provider = MockIDaaSCredentialProvider(mock_credential)

        token = provider.get_bearer_token()
        assert token == "test_token"

    def test_get_bearer_token_without_credential(self):
        """Test get_bearer_token without credential returns None."""
        provider = MockIDaaSCredentialProvider()
        token = provider.get_bearer_token()
        assert token is None

    def test_get_oidc_token_with_credential(self):
        """Test get_oidc_token with valid credential."""
        mock_credential = Mock(spec=IDaaSCredential)
        mock_credential.get_access_token.return_value = "test_oidc_token"
        provider = MockIDaaSCredentialProvider(mock_credential)

        token = provider.get_oidc_token()
        assert token == "test_oidc_token"

    def test_get_oidc_token_without_credential(self):
        """Test get_oidc_token without credential returns None."""
        provider = MockIDaaSCredentialProvider()
        token = provider.get_oidc_token()
        assert token is None

    def test_get_oidc_token_same_as_bearer_token(self):
        """Test that get_oidc_token returns same as get_bearer_token."""
        mock_credential = Mock(spec=IDaaSCredential)
        mock_credential.get_access_token.return_value = "same_token"
        provider = MockIDaaSCredentialProvider(mock_credential)

        assert provider.get_oidc_token() == provider.get_bearer_token()

    def test_set_client_secret_supplier_raises_not_implemented(self):
        """Test that set_client_secret_supplier raises NotImplementedError."""
        provider = MockIDaaSCredentialProvider()
        with pytest.raises(NotImplementedError, match="set_client_secret_supplier not implemented"):
            provider.set_client_secret_supplier(lambda: "secret")

    def test_set_client_assertion_provider_raises_not_implemented(self):
        """Test that set_client_assertion_provider raises NotImplementedError."""
        provider = MockIDaaSCredentialProvider()
        with pytest.raises(NotImplementedError, match="set_client_assertion_provider not implemented"):
            provider.set_client_assertion_provider(Mock())

    def test_set_oidc_token_provider_raises_not_implemented(self):
        """Test that set_oidc_token_provider raises NotImplementedError."""
        provider = MockIDaaSCredentialProvider()
        with pytest.raises(NotImplementedError, match="set_oidc_token_provider not implemented"):
            provider.set_oidc_token_provider(Mock())

    def test_set_attested_document_provider_raises_not_implemented(self):
        """Test that set_attested_document_provider raises NotImplementedError."""
        provider = MockIDaaSCredentialProvider()
        with pytest.raises(NotImplementedError, match="set_attested_document_provider not implemented"):
            provider.set_attested_document_provider(Mock())

    def test_set_application_federated_credential_name_raises_not_implemented(self):
        """Test that set_application_federated_credential_name raises NotImplementedError."""
        provider = MockIDaaSCredentialProvider()
        with pytest.raises(NotImplementedError, match="set_application_federated_credential_name not implemented"):
            provider.set_application_federated_credential_name("test_name")

    def test_set_client_x509_certificate_raises_not_implemented(self):
        """Test that set_client_x509_certificate raises NotImplementedError."""
        provider = MockIDaaSCredentialProvider()
        with pytest.raises(NotImplementedError, match="set_client_x509_certificate not implemented"):
            provider.set_client_x509_certificate("test_cert")

    def test_set_x509_cert_chains_raises_not_implemented(self):
        """Test that set_x509_cert_chains raises NotImplementedError."""
        provider = MockIDaaSCredentialProvider()
        with pytest.raises(NotImplementedError, match="set_x509_cert_chains not implemented"):
            provider.set_x509_cert_chains("test_chains")
