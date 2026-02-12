"""
IDaaS Python SDK - IDaaS Machine Credential Provider

This module provides the main machine credential provider for IDaaS.
It supports multiple authentication methods including client secret,
JWT assertion, PKCS7, OIDC, and PCA.
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Callable, Optional

from cloud_idaas.core.cache.refresh_result import RefreshResult
from cloud_idaas.core.cache.stale_value_behavior import StaleValueBehavior
from cloud_idaas.core.constants import TokenAuthnMethod
from cloud_idaas.core.credential import IDaaSCredential, IDaaSTokenResponse
from cloud_idaas.core.exceptions import CredentialException
from cloud_idaas.core.http.oauth2_token_util import OAuth2TokenUtil
from cloud_idaas.core.implementation.abstract_refreshed_credential_provider import AbstractRefreshedCredentialProvider
from cloud_idaas.core.provider.idaas_credential_provider import IDaaSCredentialProvider
from cloud_idaas.core.provider.jwt_client_assertion_provider import JwtClientAssertionProvider
from cloud_idaas.core.provider.oidc_token_provider import OidcTokenProvider
from cloud_idaas.core.provider.pkcs7_attested_document_provider import Pkcs7AttestedDocumentProvider
from cloud_idaas.core.util.string_util import StringUtil

logger = logging.getLogger(__name__)


class IDaaSMachineCredentialProvider(AbstractRefreshedCredentialProvider[IDaaSCredential], IDaaSCredentialProvider):
    """
    Machine credential provider for IDaaS.

    Supports the following authentication methods:
    - CLIENT_SECRET_BASIC: Client secret in HTTP Basic Auth
    - CLIENT_SECRET_POST: Client secret in POST body
    - CLIENT_SECRET_JWT: Client assertion using client secret
    - PRIVATE_KEY_JWT: Client assertion using private key
    - PKCS7: PKCS7 attested document
    - OIDC: OIDC token
    - PCA: Private Certificate Authority
    """

    def __init__(
        self,
        client_id: str,
        scope: str,
        token_endpoint: str,
        authn_method: TokenAuthnMethod = TokenAuthnMethod.CLIENT_SECRET_POST,
        client_secret_supplier: Optional[Callable[[], str]] = None,
        client_assertion_provider: Optional[JwtClientAssertionProvider] = None,
        application_federated_credential_name: Optional[str] = None,
        attested_document_provider: Optional[Pkcs7AttestedDocumentProvider] = None,
        oidc_token_provider: Optional[OidcTokenProvider] = None,
        client_x509_certificate: Optional[str] = None,
        x509_cert_chains: Optional[str] = None,
        async_credential_update_enabled: bool = False,
        stale_value_behavior: StaleValueBehavior = StaleValueBehavior.STRICT,
    ):
        """
        Initialize the IDaaS machine credential provider.

        Args:
            client_id: The client ID.
            scope: The OAuth scope.
            token_endpoint: The token endpoint URL.
            authn_method: The authentication method.
            client_secret_supplier: Function to get client secret.
            client_assertion_provider: JWT client assertion provider.
            application_federated_credential_name: Application federated credential name.
            attested_document_provider: PKCS7 attested document provider.
            oidc_token_provider: OIDC token provider.
            client_x509_certificate: Client X509 certificate (for PCA).
            x509_cert_chains: X509 certificate chains (for PCA).
            async_credential_update_enabled: Whether to enable async credential update.
            stale_value_behavior: Behavior when cached value is stale.
        """
        if StringUtil.is_blank(client_id):
            raise ValueError("clientId is blank")
        if StringUtil.is_blank(scope):
            raise ValueError("scope is blank")
        if StringUtil.is_blank(token_endpoint):
            raise ValueError("tokenEndpoint is blank")

        super().__init__(async_credential_update_enabled, stale_value_behavior)

        self._authn_method = authn_method
        self._client_id = client_id
        self._scope = scope
        self._token_endpoint = token_endpoint
        self._client_secret_supplier = client_secret_supplier
        self._client_assertion_provider = client_assertion_provider
        self._application_federated_credential_name = application_federated_credential_name
        self._attested_document_provider = attested_document_provider
        self._oidc_token_provider = oidc_token_provider
        self._client_x509_certificate = client_x509_certificate
        self._x509_cert_chains = x509_cert_chains

    @property
    def authn_method(self) -> TokenAuthnMethod:
        """Get the authentication method."""
        return self._authn_method

    @authn_method.setter
    def authn_method(self, value: TokenAuthnMethod) -> None:
        """Set the authentication method."""
        self._authn_method = value

    @property
    def client_id(self) -> str:
        """Get the client ID."""
        return self._client_id

    @property
    def scope(self) -> str:
        """Get the OAuth scope."""
        return self._scope

    @property
    def token_endpoint(self) -> str:
        """Get the token endpoint."""
        return self._token_endpoint

    @property
    def client_secret_supplier(self) -> Optional[Callable[[], str]]:
        """Get the client secret supplier."""
        return self._client_secret_supplier

    @client_secret_supplier.setter
    def client_secret_supplier(self, value: Callable[[], str]) -> None:
        """Set the client secret supplier."""
        self._client_secret_supplier = value

    @property
    def client_assertion_provider(self) -> Optional[JwtClientAssertionProvider]:
        """Get the client assertion provider."""
        return self._client_assertion_provider

    @client_assertion_provider.setter
    def client_assertion_provider(self, value: JwtClientAssertionProvider) -> None:
        """Set the client assertion provider."""
        self._client_assertion_provider = value

    @property
    def application_federated_credential_name(self) -> Optional[str]:
        """Get the application federated credential name."""
        return self._application_federated_credential_name

    @application_federated_credential_name.setter
    def application_federated_credential_name(self, value: str) -> None:
        """Set the application federated credential name."""
        self._application_federated_credential_name = value

    @property
    def attested_document_provider(self) -> Optional[Pkcs7AttestedDocumentProvider]:
        """Get the attested document provider."""
        return self._attested_document_provider

    @attested_document_provider.setter
    def attested_document_provider(self, value: Pkcs7AttestedDocumentProvider) -> None:
        """Set the attested document provider."""
        self._attested_document_provider = value

    @property
    def oidc_token_provider(self) -> Optional[OidcTokenProvider]:
        """Get the OIDC token provider."""
        return self._oidc_token_provider

    @oidc_token_provider.setter
    def oidc_token_provider(self, value: OidcTokenProvider) -> None:
        """Set the OIDC token provider."""
        self._oidc_token_provider = value

    @property
    def client_x509_certificate(self) -> Optional[str]:
        """Get the client X509 certificate."""
        return self._client_x509_certificate

    @client_x509_certificate.setter
    def client_x509_certificate(self, value: str) -> None:
        """Set the client X509 certificate."""
        self._client_x509_certificate = value

    @property
    def x509_cert_chains(self) -> Optional[str]:
        """Get the X509 certificate chains."""
        return self._x509_cert_chains

    @x509_cert_chains.setter
    def x509_cert_chains(self, value: str) -> None:
        """Set the X509 certificate chains."""
        self._x509_cert_chains = value

    def get_credential(self) -> IDaaSCredential:
        """
        Get the credential.

        Returns:
            The IDaaS credential.
        """
        return self.get_cached_result_supplier().get()

    def _get_token_from_idaas(self) -> IDaaSTokenResponse:
        """
        Get token from IDaaS using the configured authentication method.

        Returns:
            The token response.

        Raises:
            ValueError: If required parameters are missing.
            CredentialException: If authentication fails.
        """
        if self._authn_method == TokenAuthnMethod.CLIENT_SECRET_BASIC:
            if self._client_secret_supplier is None:
                client_secret = os.getenv("ALIBABA_CLOUD_EIAM_APP_CLIENT_SECRET")
                if StringUtil.is_blank(client_secret):
                    raise ValueError("clientSecret is blank")
                return OAuth2TokenUtil.get_token_with_client_secret_basic(
                    self._client_id, client_secret, self._token_endpoint, self._scope
                )
            return OAuth2TokenUtil.get_token_with_client_secret_basic(
                self._client_id, self._client_secret_supplier(), self._token_endpoint, self._scope
            )

        elif self._authn_method == TokenAuthnMethod.CLIENT_SECRET_POST:
            if self._client_secret_supplier is None:
                client_secret = os.getenv("ALIBABA_CLOUD_EIAM_APP_CLIENT_SECRET")
                if StringUtil.is_blank(client_secret):
                    raise ValueError("clientSecret is blank")
                return OAuth2TokenUtil.get_token_with_client_secret_post(
                    self._client_id, client_secret, self._token_endpoint, self._scope
                )
            return OAuth2TokenUtil.get_token_with_client_secret_post(
                self._client_id, self._client_secret_supplier(), self._token_endpoint, self._scope
            )

        elif self._authn_method in (TokenAuthnMethod.CLIENT_SECRET_JWT, TokenAuthnMethod.PRIVATE_KEY_JWT):
            if self._client_assertion_provider is None:
                raise ValueError("clientAssertionProvider is null")
            return OAuth2TokenUtil.get_token_with_client_assertion(
                self._client_id,
                self._client_assertion_provider.get_client_assertion(),
                self._token_endpoint,
                self._scope,
            )

        elif self._authn_method == TokenAuthnMethod.PKCS7:
            if StringUtil.is_blank(self._application_federated_credential_name):
                raise ValueError("applicationFederatedCredentialName is blank")
            if self._attested_document_provider is None:
                raise ValueError("attestedDocumentProvider is null")
            pkcs7_attested_document = self._attested_document_provider.get_attested_document()
            return OAuth2TokenUtil.get_token_with_pkcs7_attested_document(
                self._client_id,
                self._application_federated_credential_name,
                pkcs7_attested_document,
                self._token_endpoint,
                self._scope,
            )

        elif self._authn_method == TokenAuthnMethod.OIDC:
            if StringUtil.is_blank(self._application_federated_credential_name):
                raise ValueError("applicationFederatedCredentialName is blank")
            if self._oidc_token_provider is None:
                raise ValueError("oidcTokenProvider is null")
            oidc_token = self._oidc_token_provider.get_oidc_token()
            return OAuth2TokenUtil.get_token_with_oidc_federated_credential(
                self._client_id,
                self._application_federated_credential_name,
                oidc_token,
                self._token_endpoint,
                self._scope,
            )

        elif self._authn_method == TokenAuthnMethod.PCA:
            if StringUtil.is_blank(self._application_federated_credential_name):
                raise ValueError("applicationFederatedCredentialName is blank")
            if StringUtil.is_blank(self._client_x509_certificate):
                raise ValueError("clientX509Certificate is blank")
            if StringUtil.is_blank(self._x509_cert_chains):
                raise ValueError("x509CertChains is blank")
            return OAuth2TokenUtil.get_token_with_pca(
                self._client_id,
                self._application_federated_credential_name,
                self._client_x509_certificate,
                self._x509_cert_chains,
                self._client_assertion_provider.get_client_assertion(),
                self._token_endpoint,
                self._scope,
            )

        raise CredentialException(f"Unsupported authentication method: {self._authn_method}")

    def _refresh_credential(self) -> RefreshResult[IDaaSCredential]:
        """
        Refresh the credential.

        Returns:
            RefreshResult containing the new credential and timing information.
        """
        token_response = self._get_token_from_idaas()
        logger.info(f"Machine Credential refresh, time: {datetime.now()}")

        # Calculate stale time (4/5 of expires_in) and prefetch time (2/3 of expires_in)
        # Convert timestamp to timezone-aware datetime in UTC
        from datetime import timezone

        expires_at = datetime.fromtimestamp(token_response.expires_at, tz=timezone.utc)
        expires_in_seconds = token_response.expires_in
        stale_time = expires_at - timedelta(seconds=expires_in_seconds // 5)
        prefetch_time = expires_at - timedelta(seconds=expires_in_seconds // 3)

        return RefreshResult.builder(token_response).stale_time(stale_time).prefetch_time(prefetch_time).build()

    @staticmethod
    def builder() -> "IDaaSMachineCredentialProviderBuilder":
        """Create a new builder instance."""
        return IDaaSMachineCredentialProviderBuilder()


class IDaaSMachineCredentialProviderBuilder:
    """Builder class for IDaaSMachineCredentialProvider."""

    def __init__(self):
        """Initialize the builder."""
        self._client_id: Optional[str] = None
        self._scope: Optional[str] = None
        self._token_endpoint: Optional[str] = None
        self._authn_method = TokenAuthnMethod.CLIENT_SECRET_POST
        self._client_secret_supplier: Optional[Callable[[], str]] = None
        self._client_assertion_provider: Optional[JwtClientAssertionProvider] = None
        self._application_federated_credential_name: Optional[str] = None
        self._attested_document_provider: Optional[Pkcs7AttestedDocumentProvider] = None
        self._oidc_token_provider: Optional[OidcTokenProvider] = None
        self._client_x509_certificate: Optional[str] = None
        self._x509_cert_chains: Optional[str] = None
        self._async_credential_update_enabled = False
        self._stale_value_behavior = StaleValueBehavior.STRICT

    def client_id(self, value: str) -> "IDaaSMachineCredentialProviderBuilder":
        """Set the client ID."""
        self._client_id = value
        return self

    def scope(self, value: str) -> "IDaaSMachineCredentialProviderBuilder":
        """Set the OAuth scope."""
        self._scope = value
        return self

    def token_endpoint(self, value: str) -> "IDaaSMachineCredentialProviderBuilder":
        """Set the token endpoint."""
        self._token_endpoint = value
        return self

    def authn_method(self, value: TokenAuthnMethod) -> "IDaaSMachineCredentialProviderBuilder":
        """Set the authentication method."""
        self._authn_method = value
        return self

    def client_secret_supplier(self, value: Callable[[], str]) -> "IDaaSMachineCredentialProviderBuilder":
        """Set the client secret supplier."""
        self._client_secret_supplier = value
        return self

    def client_assertion_provider(self, value: JwtClientAssertionProvider) -> "IDaaSMachineCredentialProviderBuilder":
        """Set the client assertion provider."""
        self._client_assertion_provider = value
        return self

    def application_federated_credential_name(self, value: str) -> "IDaaSMachineCredentialProviderBuilder":
        """Set the application federated credential name."""
        self._application_federated_credential_name = value
        return self

    def attested_document_provider(
        self, value: Pkcs7AttestedDocumentProvider
    ) -> "IDaaSMachineCredentialProviderBuilder":
        """Set the attested document provider."""
        self._attested_document_provider = value
        return self

    def oidc_token_provider(self, value: OidcTokenProvider) -> "IDaaSMachineCredentialProviderBuilder":
        """Set the OIDC token provider."""
        self._oidc_token_provider = value
        return self

    def client_x509_certificate(self, value: str) -> "IDaaSMachineCredentialProviderBuilder":
        """Set the client X509 certificate."""
        self._client_x509_certificate = value
        return self

    def x509_cert_chains(self, value: str) -> "IDaaSMachineCredentialProviderBuilder":
        """Set the X509 certificate chains."""
        self._x509_cert_chains = value
        return self

    def async_credential_update_enabled(self, value: bool) -> "IDaaSMachineCredentialProviderBuilder":
        """Set whether async credential update is enabled."""
        self._async_credential_update_enabled = value
        return self

    def stale_value_behavior(self, value: StaleValueBehavior) -> "IDaaSMachineCredentialProviderBuilder":
        """Set the stale value behavior."""
        self._stale_value_behavior = value
        return self

    def build(self) -> IDaaSMachineCredentialProvider:
        """
        Build the IDaaS machine credential provider.

        Returns:
            The configured IDaaSMachineCredentialProvider instance.
        """
        return IDaaSMachineCredentialProvider(
            client_id=self._client_id,
            scope=self._scope,
            token_endpoint=self._token_endpoint,
            authn_method=self._authn_method,
            client_secret_supplier=self._client_secret_supplier,
            client_assertion_provider=self._client_assertion_provider,
            application_federated_credential_name=self._application_federated_credential_name,
            attested_document_provider=self._attested_document_provider,
            oidc_token_provider=self._oidc_token_provider,
            client_x509_certificate=self._client_x509_certificate,
            x509_cert_chains=self._x509_cert_chains,
            async_credential_update_enabled=self._async_credential_update_enabled,
            stale_value_behavior=self._stale_value_behavior,
        )
