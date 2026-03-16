"""
Unit tests for IDaaSMachineTokenExchangeCredentialProvider
"""

from unittest.mock import Mock, patch

import pytest

from cloud_idaas.core.constants import TokenAuthnMethod
from cloud_idaas.core.credential import IDaaSTokenResponse
from cloud_idaas.core.exceptions import CredentialException
from cloud_idaas.core.implementation import (
    IDaaSMachineTokenExchangeCredentialProvider,
    IDaaSMachineTokenExchangeCredentialProviderBuilder,
)


class TestIDaaSMachineTokenExchangeCredentialProvider:
    """Test cases for IDaaSMachineTokenExchangeCredentialProvider."""

    def test_init_with_valid_parameters(self):
        """Test initialization with valid parameters."""
        provider = IDaaSMachineTokenExchangeCredentialProvider(
            client_id="test-client",
            scope="api://test|read",
            token_endpoint="https://example.com/token",
            authn_method=TokenAuthnMethod.CLIENT_SECRET_POST,
        )
        assert provider.client_id == "test-client"
        assert provider.scope == "api://test|read"
        assert provider.token_endpoint == "https://example.com/token"
        assert provider.authn_method == TokenAuthnMethod.CLIENT_SECRET_POST

    def test_init_with_blank_client_id_raises_error(self):
        """Test that blank client_id raises ValueError."""
        with pytest.raises(ValueError, match="clientId is blank"):
            IDaaSMachineTokenExchangeCredentialProvider(
                client_id="",
                scope="api://test|read",
                token_endpoint="https://example.com/token",
            )

    def test_init_with_blank_token_endpoint_raises_error(self):
        """Test that blank token_endpoint raises ValueError."""
        with pytest.raises(ValueError, match="tokenEndpoint is blank"):
            IDaaSMachineTokenExchangeCredentialProvider(
                client_id="test-client",
                scope="api://test|read",
                token_endpoint="",
            )

    def test_get_credential_with_blank_subject_token_raises_error(self):
        """Test that blank subject_token raises ValueError."""
        provider = IDaaSMachineTokenExchangeCredentialProvider(
            client_id="test-client",
            scope="api://test|read",
            token_endpoint="https://example.com/token",
        )
        with pytest.raises(ValueError, match="subject_token is blank"):
            provider.get_credential(subject_token="", subject_token_type="type")

    def test_get_credential_with_blank_subject_token_type_raises_error(self):
        """Test that blank subject_token_type raises ValueError."""
        provider = IDaaSMachineTokenExchangeCredentialProvider(
            client_id="test-client",
            scope="api://test|read",
            token_endpoint="https://example.com/token",
        )
        with pytest.raises(ValueError, match="subject_token_type is blank"):
            provider.get_credential(subject_token="token", subject_token_type="")

    @patch("cloud_idaas.core.implementation.idaas_machine_token_exchange_credential_provider.OAuth2TokenUtil")
    def test_get_credential_with_client_secret_basic(self, mock_oauth2_util):
        """Test get_credential with CLIENT_SECRET_BASIC authn method."""
        mock_response = Mock(spec=IDaaSTokenResponse)
        mock_oauth2_util.token_exchange_with_client_secret_basic.return_value = mock_response

        provider = IDaaSMachineTokenExchangeCredentialProvider(
            client_id="test-client",
            scope="api://test|read",
            token_endpoint="https://example.com/token",
            authn_method=TokenAuthnMethod.CLIENT_SECRET_BASIC,
            client_secret_supplier=lambda: "secret",
        )

        result = provider.get_credential(
            subject_token="subject_token",
            subject_token_type="urn:ietf:params:oauth:token-type:access_token",
        )

        assert result == mock_response
        mock_oauth2_util.token_exchange_with_client_secret_basic.assert_called_once()

    @patch("cloud_idaas.core.implementation.idaas_machine_token_exchange_credential_provider.OAuth2TokenUtil")
    def test_get_credential_with_client_secret_post(self, mock_oauth2_util):
        """Test get_credential with CLIENT_SECRET_POST authn method."""
        mock_response = Mock(spec=IDaaSTokenResponse)
        mock_oauth2_util.token_exchange_with_client_secret_post.return_value = mock_response

        provider = IDaaSMachineTokenExchangeCredentialProvider(
            client_id="test-client",
            scope="api://test|read",
            token_endpoint="https://example.com/token",
            authn_method=TokenAuthnMethod.CLIENT_SECRET_POST,
            client_secret_supplier=lambda: "secret",
        )

        result = provider.get_credential(
            subject_token="subject_token",
            subject_token_type="urn:ietf:params:oauth:token-type:access_token",
        )

        assert result == mock_response
        mock_oauth2_util.token_exchange_with_client_secret_post.assert_called_once()

    def test_get_credential_with_jwt_without_assertion_provider_raises_error(self):
        """Test that JWT authn without assertion provider raises ValueError."""
        provider = IDaaSMachineTokenExchangeCredentialProvider(
            client_id="test-client",
            scope="api://test|read",
            token_endpoint="https://example.com/token",
            authn_method=TokenAuthnMethod.PRIVATE_KEY_JWT,
        )

        with pytest.raises(ValueError, match="clientAssertionProvider is null"):
            provider.get_credential(
                subject_token="subject_token",
                subject_token_type="urn:ietf:params:oauth:token-type:access_token",
            )

    def test_get_credential_with_pkcs7_without_required_fields_raises_error(self):
        """Test that PKCS7 authn without required fields raises ValueError."""
        provider = IDaaSMachineTokenExchangeCredentialProvider(
            client_id="test-client",
            scope="api://test|read",
            token_endpoint="https://example.com/token",
            authn_method=TokenAuthnMethod.PKCS7,
        )

        with pytest.raises(ValueError, match="applicationFederatedCredentialName is blank"):
            provider.get_credential(
                subject_token="subject_token",
                subject_token_type="urn:ietf:params:oauth:token-type:access_token",
            )

    def test_get_credential_with_oidc_without_required_fields_raises_error(self):
        """Test that OIDC authn without required fields raises ValueError."""
        provider = IDaaSMachineTokenExchangeCredentialProvider(
            client_id="test-client",
            scope="api://test|read",
            token_endpoint="https://example.com/token",
            authn_method=TokenAuthnMethod.OIDC,
        )

        with pytest.raises(ValueError, match="applicationFederatedCredentialName is blank"):
            provider.get_credential(
                subject_token="subject_token",
                subject_token_type="urn:ietf:params:oauth:token-type:access_token",
            )

    def test_get_credential_with_pca_without_required_fields_raises_error(self):
        """Test that PCA authn without required fields raises ValueError."""
        provider = IDaaSMachineTokenExchangeCredentialProvider(
            client_id="test-client",
            scope="api://test|read",
            token_endpoint="https://example.com/token",
            authn_method=TokenAuthnMethod.PCA,
        )

        with pytest.raises(ValueError, match="applicationFederatedCredentialName is blank"):
            provider.get_credential(
                subject_token="subject_token",
                subject_token_type="urn:ietf:params:oauth:token-type:access_token",
            )

    def test_get_credential_with_unsupported_authn_raises_error(self):
        """Test that unsupported authn method raises CredentialException."""
        provider = IDaaSMachineTokenExchangeCredentialProvider(
            client_id="test-client",
            scope="api://test|read",
            token_endpoint="https://example.com/token",
            authn_method="UNSUPPORTED_METHOD",
        )

        with pytest.raises(CredentialException):
            provider.get_credential(
                subject_token="subject_token",
                subject_token_type="urn:ietf:params:oauth:token-type:access_token",
            )


class TestIDaaSMachineTokenExchangeCredentialProviderBuilder:
    """Test cases for IDaaSMachineTokenExchangeCredentialProviderBuilder."""

    def test_builder_with_all_parameters(self):
        """Test builder with all parameters."""
        provider = (
            IDaaSMachineTokenExchangeCredentialProviderBuilder()
            .client_id("test-client")
            .scope("api://test|read")
            .token_endpoint("https://example.com/token")
            .authn_method(TokenAuthnMethod.CLIENT_SECRET_POST)
            .client_secret_supplier(lambda: "secret")
            .build()
        )

        assert provider.client_id == "test-client"
        assert provider.scope == "api://test|read"
        assert provider.token_endpoint == "https://example.com/token"
        assert provider.authn_method == TokenAuthnMethod.CLIENT_SECRET_POST

    def test_builder_chaining(self):
        """Test that builder methods return self for chaining."""
        builder = IDaaSMachineTokenExchangeCredentialProviderBuilder()
        assert builder.client_id("test") is builder
        assert builder.scope("api://test|read") is builder
        assert builder.token_endpoint("https://example.com") is builder
        assert builder.authn_method(TokenAuthnMethod.CLIENT_SECRET_POST) is builder

    def test_builder_default_authn_method(self):
        """Test that default authn_method is CLIENT_SECRET_POST."""
        builder = IDaaSMachineTokenExchangeCredentialProviderBuilder()
        assert builder._authn_method == TokenAuthnMethod.CLIENT_SECRET_POST

    def test_build_creates_new_instance(self):
        """Test that build creates a new instance each time."""
        builder = (
            IDaaSMachineTokenExchangeCredentialProviderBuilder()
            .client_id("test-client")
            .scope("api://test|read")
            .token_endpoint("https://example.com/token")
        )

        provider1 = builder.build()
        provider2 = builder.build()

        assert provider1 is not provider2
        assert provider1.client_id == provider2.client_id
