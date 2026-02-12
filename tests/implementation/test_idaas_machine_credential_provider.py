"""
Unit tests for IDaaSMachineCredentialProvider
"""

import os
from unittest.mock import Mock, patch

import pytest

from cloud_idaas import CredentialException, IDaaSTokenResponse, StaleValueBehavior
from cloud_idaas.core import TokenAuthnMethod
from cloud_idaas.core.implementation.idaas_machine_credential_provider import (
    IDaaSMachineCredentialProvider,
)


class TestIDaaSMachineCredentialProvider:
    """Test cases for IDaaSMachineCredentialProvider."""

    def test_initialization_with_required_params(self):
        """Test initialization with required parameters."""
        provider = IDaaSMachineCredentialProvider(
            client_id="test_client",
            scope="test_scope",
            token_endpoint="https://test.com/token",
            authn_method=TokenAuthnMethod.CLIENT_SECRET_POST,
            client_secret_supplier=lambda: "test_secret",
        )
        assert provider.client_id == "test_client"
        assert provider.scope == "test_scope"
        assert provider.token_endpoint == "https://test.com/token"
        assert provider.authn_method == TokenAuthnMethod.CLIENT_SECRET_POST

    def test_initialization_with_blank_client_id_raises_error(self):
        """Test that blank client_id raises ValueError."""
        with pytest.raises(ValueError, match="clientId is blank"):
            IDaaSMachineCredentialProvider(client_id="", scope="test_scope", token_endpoint="https://test.com/token")

    def test_initialization_with_blank_scope_raises_error(self):
        """Test that blank scope raises ValueError."""
        with pytest.raises(ValueError, match="scope is blank"):
            IDaaSMachineCredentialProvider(client_id="test_client", scope="", token_endpoint="https://test.com/token")

    def test_initialization_with_blank_token_endpoint_raises_error(self):
        """Test that blank token_endpoint raises ValueError."""
        with pytest.raises(ValueError, match="tokenEndpoint is blank"):
            IDaaSMachineCredentialProvider(client_id="test_client", scope="test_scope", token_endpoint="")

    def test_property_setters(self):
        """Test property setters."""
        provider = IDaaSMachineCredentialProvider(
            client_id="test_client", scope="test_scope", token_endpoint="https://test.com/token"
        )

        provider.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC
        assert provider.authn_method == TokenAuthnMethod.CLIENT_SECRET_BASIC

        provider.client_secret_supplier = lambda: "new_secret"
        assert provider.client_secret_supplier() == "new_secret"

        mock_assertion = Mock()
        provider.client_assertion_provider = mock_assertion
        assert provider.client_assertion_provider == mock_assertion

        provider.application_federated_credential_name = "test_fed_credential"
        assert provider.application_federated_credential_name == "test_fed_credential"

        mock_attested = Mock()
        provider.attested_document_provider = mock_attested
        assert provider.attested_document_provider == mock_attested

        mock_oidc = Mock()
        provider.oidc_token_provider = mock_oidc
        assert provider.oidc_token_provider == mock_oidc

        provider.client_x509_certificate = "test_cert"
        assert provider.client_x509_certificate == "test_cert"

        provider.x509_cert_chains = "test_chains"
        assert provider.x509_cert_chains == "test_chains"

    def test_is_async_credential_update_enabled(self):
        """Test async credential update enabled flag."""
        provider = IDaaSMachineCredentialProvider(
            client_id="test_client",
            scope="test_scope",
            token_endpoint="https://test.com/token",
            async_credential_update_enabled=True,
        )
        assert provider.is_async_credential_update_enabled()

    def test_get_cached_result_supplier(self):
        """Test getting cached result supplier."""
        provider = IDaaSMachineCredentialProvider(
            client_id="test_client", scope="test_scope", token_endpoint="https://test.com/token"
        )
        supplier = provider.get_cached_result_supplier()
        assert supplier is not None

    def test_close(self):
        """Test closing the provider."""
        provider = IDaaSMachineCredentialProvider(
            client_id="test_client", scope="test_scope", token_endpoint="https://test.com/token"
        )
        provider.close()
        # Should not raise an exception

    def test_context_manager(self):
        """Test using provider as context manager."""
        with IDaaSMachineCredentialProvider(
            client_id="test_client", scope="test_scope", token_endpoint="https://test.com/token"
        ) as provider:
            assert provider is not None

    @patch("cloud_idaas.core.implementation.idaas_machine_credential_provider.OAuth2TokenUtil")
    def test_get_token_with_client_secret_basic_from_env(self, mock_oauth_util):
        """Test getting token with client secret from environment variable."""
        import time

        mock_token_response = Mock(spec=IDaaSTokenResponse)
        mock_token_response.expires_at = int(time.time()) + 3600
        mock_token_response.expires_in = 3600
        mock_oauth_util.get_token_with_client_secret_basic.return_value = mock_token_response

        os.environ["ALIBABA_CLOUD_EIAM_APP_CLIENT_SECRET"] = "env_secret"

        provider = IDaaSMachineCredentialProvider(
            client_id="test_client",
            scope="test_scope",
            token_endpoint="https://test.com/token",
            authn_method=TokenAuthnMethod.CLIENT_SECRET_BASIC,
        )

        result = provider._get_token_from_idaas()
        assert result == mock_token_response

        del os.environ["ALIBABA_CLOUD_EIAM_APP_CLIENT_SECRET"]

    @patch("cloud_idaas.core.implementation.idaas_machine_credential_provider.OAuth2TokenUtil")
    def test_get_token_with_client_secret_basic_from_supplier(self, mock_oauth_util):
        """Test getting token with client secret from supplier."""
        mock_token_response = Mock(spec=IDaaSTokenResponse)
        mock_token_response.expires_at = 1234567890
        mock_token_response.expires_in = 3600
        mock_oauth_util.get_token_with_client_secret_basic.return_value = mock_token_response

        provider = IDaaSMachineCredentialProvider(
            client_id="test_client",
            scope="test_scope",
            token_endpoint="https://test.com/token",
            authn_method=TokenAuthnMethod.CLIENT_SECRET_BASIC,
            client_secret_supplier=lambda: "supplier_secret",
        )

        result = provider._get_token_from_idaas()
        assert result == mock_token_response

    @patch("cloud_idaas.core.implementation.idaas_machine_credential_provider.OAuth2TokenUtil")
    def test_get_token_with_client_secret_post(self, mock_oauth_util):
        """Test getting token with client secret POST method."""
        mock_token_response = Mock(spec=IDaaSTokenResponse)
        mock_token_response.expires_at = 1234567890
        mock_token_response.expires_in = 3600
        mock_oauth_util.get_token_with_client_secret_post.return_value = mock_token_response

        provider = IDaaSMachineCredentialProvider(
            client_id="test_client",
            scope="test_scope",
            token_endpoint="https://test.com/token",
            authn_method=TokenAuthnMethod.CLIENT_SECRET_POST,
            client_secret_supplier=lambda: "test_secret",
        )

        result = provider._get_token_from_idaas()
        assert result == mock_token_response

    @patch("cloud_idaas.core.implementation.idaas_machine_credential_provider.OAuth2TokenUtil")
    def test_get_token_with_client_assertion(self, mock_oauth_util):
        """Test getting token with client assertion."""
        mock_token_response = Mock(spec=IDaaSTokenResponse)
        mock_token_response.expires_at = 1234567890
        mock_token_response.expires_in = 3600
        mock_oauth_util.get_token_with_client_assertion.return_value = mock_token_response

        mock_assertion_provider = Mock()
        mock_assertion_provider.get_client_assertion.return_value = "test_assertion"

        provider = IDaaSMachineCredentialProvider(
            client_id="test_client",
            scope="test_scope",
            token_endpoint="https://test.com/token",
            authn_method=TokenAuthnMethod.CLIENT_SECRET_JWT,
            client_assertion_provider=mock_assertion_provider,
        )

        result = provider._get_token_from_idaas()
        assert result == mock_token_response

    def test_get_token_with_client_assertion_but_no_provider_raises_error(self):
        """Test that getting token without assertion provider raises ValueError."""
        provider = IDaaSMachineCredentialProvider(
            client_id="test_client",
            scope="test_scope",
            token_endpoint="https://test.com/token",
            authn_method=TokenAuthnMethod.CLIENT_SECRET_JWT,
        )

        with pytest.raises(ValueError, match="clientAssertionProvider is null"):
            provider._get_token_from_idaas()

    @patch("cloud_idaas.core.implementation.idaas_machine_credential_provider.OAuth2TokenUtil")
    def test_get_token_with_pkcs7(self, mock_oauth_util):
        """Test getting token with PKCS7 attested document."""
        mock_token_response = Mock(spec=IDaaSTokenResponse)
        mock_token_response.expires_at = 1234567890
        mock_token_response.expires_in = 3600
        mock_oauth_util.get_token_with_pkcs7_attested_document.return_value = mock_token_response

        mock_attested_provider = Mock()
        mock_attested_provider.get_attested_document.return_value = "test_pkcs7"

        provider = IDaaSMachineCredentialProvider(
            client_id="test_client",
            scope="test_scope",
            token_endpoint="https://test.com/token",
            authn_method=TokenAuthnMethod.PKCS7,
            application_federated_credential_name="test_fed_credential",
            attested_document_provider=mock_attested_provider,
        )

        result = provider._get_token_from_idaas()
        assert result == mock_token_response

    def test_get_token_with_pkcs7_missing_fed_credential_name_raises_error(self):
        """Test that PKCS7 without federated credential name raises ValueError."""
        provider = IDaaSMachineCredentialProvider(
            client_id="test_client",
            scope="test_scope",
            token_endpoint="https://test.com/token",
            authn_method=TokenAuthnMethod.PKCS7,
        )

        with pytest.raises(ValueError, match="applicationFederatedCredentialName is blank"):
            provider._get_token_from_idaas()

    @patch("cloud_idaas.core.implementation.idaas_machine_credential_provider.OAuth2TokenUtil")
    def test_get_token_with_oidc(self, mock_oauth_util):
        """Test getting token with OIDC."""
        mock_token_response = Mock(spec=IDaaSTokenResponse)
        mock_token_response.expires_at = 1234567890
        mock_token_response.expires_in = 3600
        mock_oauth_util.get_token_with_oidc_federated_credential.return_value = mock_token_response

        mock_oidc_provider = Mock()
        mock_oidc_provider.get_oidc_token.return_value = "test_oidc_token"

        provider = IDaaSMachineCredentialProvider(
            client_id="test_client",
            scope="test_scope",
            token_endpoint="https://test.com/token",
            authn_method=TokenAuthnMethod.OIDC,
            application_federated_credential_name="test_fed_credential",
            oidc_token_provider=mock_oidc_provider,
        )

        result = provider._get_token_from_idaas()
        assert result == mock_token_response

    def test_get_token_with_oidc_missing_provider_raises_error(self):
        """Test that OIDC without provider raises ValueError."""
        provider = IDaaSMachineCredentialProvider(
            client_id="test_client",
            scope="test_scope",
            token_endpoint="https://test.com/token",
            authn_method=TokenAuthnMethod.OIDC,
            application_federated_credential_name="test_fed_credential",
        )

        with pytest.raises(ValueError, match="oidcTokenProvider is null"):
            provider._get_token_from_idaas()

    @patch("cloud_idaas.core.implementation.idaas_machine_credential_provider.OAuth2TokenUtil")
    def test_get_token_with_pca(self, mock_oauth_util):
        """Test getting token with PCA."""
        mock_token_response = Mock(spec=IDaaSTokenResponse)
        mock_token_response.expires_at = 1234567890
        mock_token_response.expires_in = 3600
        mock_oauth_util.get_token_with_pca.return_value = mock_token_response

        mock_assertion_provider = Mock()
        mock_assertion_provider.get_client_assertion.return_value = "test_assertion"

        provider = IDaaSMachineCredentialProvider(
            client_id="test_client",
            scope="test_scope",
            token_endpoint="https://test.com/token",
            authn_method=TokenAuthnMethod.PCA,
            application_federated_credential_name="test_fed_credential",
            client_x509_certificate="test_cert",
            x509_cert_chains="test_chains",
            client_assertion_provider=mock_assertion_provider,
        )

        result = provider._get_token_from_idaas()
        assert result == mock_token_response

    def test_get_token_with_pca_missing_certificate_raises_error(self):
        """Test that PCA without X509 certificate raises ValueError."""
        provider = IDaaSMachineCredentialProvider(
            client_id="test_client",
            scope="test_scope",
            token_endpoint="https://test.com/token",
            authn_method=TokenAuthnMethod.PCA,
            application_federated_credential_name="test_fed_credential",
        )

        with pytest.raises(ValueError, match="clientX509Certificate is blank"):
            provider._get_token_from_idaas()

    def test_get_token_with_pca_missing_cert_chains_raises_error(self):
        """Test that PCA without cert chains raises ValueError."""
        provider = IDaaSMachineCredentialProvider(
            client_id="test_client",
            scope="test_scope",
            token_endpoint="https://test.com/token",
            authn_method=TokenAuthnMethod.PCA,
            application_federated_credential_name="test_fed_credential",
            client_x509_certificate="test_cert",
        )

        with pytest.raises(ValueError, match="x509CertChains is blank"):
            provider._get_token_from_idaas()

    def test_get_token_with_unsupported_authn_method_raises_exception(self):
        """Test that unsupported authentication method raises CredentialException."""
        provider = IDaaSMachineCredentialProvider(
            client_id="test_client", scope="test_scope", token_endpoint="https://test.com/token"
        )
        # Set to an invalid method
        provider._authn_method = "INVALID_METHOD"

        with pytest.raises(CredentialException, match="Unsupported authentication method"):
            provider._get_token_from_idaas()


class TestIDaaSMachineCredentialProviderBuilder:
    """Test cases for IDaaSMachineCredentialProviderBuilder."""

    def test_builder_creates_provider_with_defaults(self):
        """Test builder creates provider with default values."""
        provider = (
            IDaaSMachineCredentialProvider.builder()
            .client_id("test_client")
            .scope("test_scope")
            .token_endpoint("https://test.com/token")
            .build()
        )

        assert provider.client_id == "test_client"
        assert provider.scope == "test_scope"
        assert provider.token_endpoint == "https://test.com/token"
        assert provider.authn_method == TokenAuthnMethod.CLIENT_SECRET_POST
        assert not provider.is_async_credential_update_enabled()

    def test_builder_with_all_parameters(self):
        """Test builder with all parameters."""
        mock_secret_supplier = lambda: "test_secret"
        mock_assertion_provider = Mock()
        mock_attested_provider = Mock()
        mock_oidc_provider = Mock()

        provider = (
            IDaaSMachineCredentialProvider.builder()
            .client_id("test_client")
            .scope("test_scope")
            .token_endpoint("https://test.com/token")
            .authn_method(TokenAuthnMethod.CLIENT_SECRET_BASIC)
            .client_secret_supplier(mock_secret_supplier)
            .client_assertion_provider(mock_assertion_provider)
            .application_federated_credential_name("test_fed_credential")
            .attested_document_provider(mock_attested_provider)
            .oidc_token_provider(mock_oidc_provider)
            .client_x509_certificate("test_cert")
            .x509_cert_chains("test_chains")
            .async_credential_update_enabled(True)
            .stale_value_behavior(StaleValueBehavior.ALLOW)
            .build()
        )

        assert provider.client_id == "test_client"
        assert provider.scope == "test_scope"
        assert provider.token_endpoint == "https://test.com/token"
        assert provider.authn_method == TokenAuthnMethod.CLIENT_SECRET_BASIC
        assert provider.client_secret_supplier == mock_secret_supplier
        assert provider.client_assertion_provider == mock_assertion_provider
        assert provider.application_federated_credential_name == "test_fed_credential"
        assert provider.attested_document_provider == mock_attested_provider
        assert provider.oidc_token_provider == mock_oidc_provider
        assert provider.client_x509_certificate == "test_cert"
        assert provider.x509_cert_chains == "test_chains"
        assert provider.is_async_credential_update_enabled()

    def test_builder_with_missing_required_params(self):
        """Test builder with missing required parameters."""
        with pytest.raises(ValueError, match="clientId is blank"):
            IDaaSMachineCredentialProvider.builder().build()
