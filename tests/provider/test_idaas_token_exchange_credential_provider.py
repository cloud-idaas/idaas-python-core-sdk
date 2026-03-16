"""
Unit tests for IDaaSTokenExchangeCredentialProvider
"""

from unittest.mock import Mock

import pytest

from cloud_idaas.core import IDaaSCredential
from cloud_idaas.core.provider import IDaaSTokenExchangeCredentialProvider


class MockIDaaSTokenExchangeCredentialProvider(IDaaSTokenExchangeCredentialProvider):
    """Mock implementation of IDaaSTokenExchangeCredentialProvider for testing."""

    def __init__(self, credential=None):
        self._credential = credential

    def get_credential(
        self,
        subject_token: str,
        subject_token_type: str,
        requested_token_type=None,
    ):
        return self._credential


class TestIDaaSTokenExchangeCredentialProvider:
    """Test cases for IDaaSTokenExchangeCredentialProvider."""

    def test_get_credential_returns_none_when_not_set(self):
        """Test that get_credential returns None when not set."""
        provider = MockIDaaSTokenExchangeCredentialProvider()
        assert provider.get_credential("token", "type") is None

    def test_get_credential_returns_credential(self):
        """Test that get_credential returns the credential."""
        mock_credential = Mock(spec=IDaaSCredential)
        provider = MockIDaaSTokenExchangeCredentialProvider(mock_credential)
        assert provider.get_credential("token", "type") == mock_credential

    def test_get_issued_token_with_credential(self):
        """Test get_issued_token with valid credential."""
        mock_credential = Mock(spec=IDaaSCredential)
        mock_credential.get_access_token.return_value = "test_token"
        provider = MockIDaaSTokenExchangeCredentialProvider(mock_credential)

        token = provider.get_issued_token("subject_token", "urn:ietf:params:oauth:token-type:access_token")
        assert token == "test_token"

    def test_get_issued_token_without_credential(self):
        """Test get_issued_token without credential returns None."""
        provider = MockIDaaSTokenExchangeCredentialProvider()
        with pytest.raises(AttributeError):
            provider.get_issued_token("subject_token", "urn:ietf:params:oauth:token-type:access_token")

    def test_get_issued_token_with_requested_token_type(self):
        """Test get_issued_token with requested_token_type parameter."""
        mock_credential = Mock(spec=IDaaSCredential)
        mock_credential.get_access_token.return_value = "exchanged_token"
        provider = MockIDaaSTokenExchangeCredentialProvider(mock_credential)

        token = provider.get_issued_token(
            subject_token="subject_token",
            subject_token_type="urn:ietf:params:oauth:token-type:access_token",
            requested_token_type="urn:ietf:params:oauth:token-type:access_token",
        )
        assert token == "exchanged_token"

    def test_is_abstract_class(self):
        """Test that IDaaSTokenExchangeCredentialProvider is abstract."""
        with pytest.raises(TypeError):
            IDaaSTokenExchangeCredentialProvider()
