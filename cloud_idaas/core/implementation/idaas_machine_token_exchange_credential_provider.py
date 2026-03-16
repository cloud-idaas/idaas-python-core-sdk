import logging
import os
from typing import Callable, Optional

from cloud_idaas.core.constants import ErrorCode, OAuth2Constants, TokenAuthnMethod
from cloud_idaas.core.credential import IDaaSCredential, IDaaSTokenResponse
from cloud_idaas.core.exceptions import CredentialException
from cloud_idaas.core.http.oauth2_token_util import OAuth2TokenUtil
from cloud_idaas.core.provider import IDaaSTokenExchangeCredentialProvider
from cloud_idaas.core.provider.jwt_client_assertion_provider import JwtClientAssertionProvider
from cloud_idaas.core.provider.oidc_token_provider import OidcTokenProvider
from cloud_idaas.core.provider.pkcs7_attested_document_provider import Pkcs7AttestedDocumentProvider
from cloud_idaas.core.util.string_util import StringUtil

logger = logging.getLogger(__name__)


class IDaaSMachineTokenExchangeCredentialProvider(IDaaSTokenExchangeCredentialProvider):
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
    ):
        if StringUtil.is_blank(client_id):
            raise ValueError("clientId is blank")
        if StringUtil.is_blank(scope):
            raise ValueError("scope is blank")
        if StringUtil.is_blank(token_endpoint):
            raise ValueError("tokenEndpoint is blank")

        self.client_id = client_id
        self.scope = scope
        self.token_endpoint = token_endpoint
        self.authn_method = authn_method
        self.client_secret_supplier = client_secret_supplier
        self.client_assertion_provider = client_assertion_provider
        self.application_federated_credential_name = application_federated_credential_name
        self.attested_document_provider = attested_document_provider
        self.oidc_token_provider = oidc_token_provider
        self.client_x509_certificate = client_x509_certificate
        self.x509_cert_chains = x509_cert_chains

    def get_credential(
        self,
        subject_token: str,
        subject_token_type: str,
        requested_token_type: Optional[str] = None,
    ) -> IDaaSCredential:
        if StringUtil.is_blank(subject_token):
            raise ValueError("subject_token is blank")
        if StringUtil.is_blank(subject_token_type):
            raise ValueError("subject_token_type is blank")

        # Use default values per RFC 8693
        if requested_token_type is None:
            requested_token_type = OAuth2Constants.ACCESS_TOKEN_TYPE_VALUE

        return self._get_token_by_token_exchange(
            subject_token=subject_token,
            subject_token_type=subject_token_type,
            requested_token_type=requested_token_type,
        )

    def _get_token_by_token_exchange(
        self,
        subject_token: str,
        subject_token_type: str,
        requested_token_type: str,
    ) -> IDaaSTokenResponse:
        if self.authn_method == TokenAuthnMethod.CLIENT_SECRET_BASIC:
            client_secret = self._get_client_secret()
            return OAuth2TokenUtil.token_exchange_with_client_secret_basic(
                client_id=self.client_id,
                client_secret=client_secret,
                token_endpoint=self.token_endpoint,
                subject_token=subject_token,
                subject_token_type=subject_token_type,
                scope=self.scope,
                requested_token_type=requested_token_type,
            )

        elif self.authn_method == TokenAuthnMethod.CLIENT_SECRET_POST:
            client_secret = self._get_client_secret()
            return OAuth2TokenUtil.token_exchange_with_client_secret_post(
                client_id=self.client_id,
                client_secret=client_secret,
                token_endpoint=self.token_endpoint,
                subject_token=subject_token,
                subject_token_type=subject_token_type,
                scope=self.scope,
                requested_token_type=requested_token_type,
            )

        elif self.authn_method in (TokenAuthnMethod.CLIENT_SECRET_JWT, TokenAuthnMethod.PRIVATE_KEY_JWT):
            if self.client_assertion_provider is None:
                raise ValueError("clientAssertionProvider is null")
            return OAuth2TokenUtil.token_exchange_with_client_assertion(
                client_id=self.client_id,
                client_assertion=self.client_assertion_provider.get_client_assertion(),
                token_endpoint=self.token_endpoint,
                subject_token=subject_token,
                subject_token_type=subject_token_type,
                scope=self.scope,
                requested_token_type=requested_token_type,
            )

        elif self.authn_method == TokenAuthnMethod.PKCS7:
            if StringUtil.is_blank(self.application_federated_credential_name):
                raise ValueError("applicationFederatedCredentialName is blank")
            if self.attested_document_provider is None:
                raise ValueError("attestedDocumentProvider is null")
            pkcs7_attested_document = self.attested_document_provider.get_attested_document()
            return OAuth2TokenUtil.token_exchange_with_pkcs7(
                client_id=self.client_id,
                application_federated_credential_name=self.application_federated_credential_name,
                pkcs7_attested_document=pkcs7_attested_document,
                token_endpoint=self.token_endpoint,
                subject_token=subject_token,
                subject_token_type=subject_token_type,
                scope=self.scope,
                requested_token_type=requested_token_type,
            )

        elif self.authn_method == TokenAuthnMethod.OIDC:
            if StringUtil.is_blank(self.application_federated_credential_name):
                raise ValueError("applicationFederatedCredentialName is blank")
            if self.oidc_token_provider is None:
                raise ValueError("oidcTokenProvider is null")
            oidc_token = self.oidc_token_provider.get_oidc_token()
            return OAuth2TokenUtil.token_exchange_with_oidc(
                client_id=self.client_id,
                application_federated_credential_name=self.application_federated_credential_name,
                oidc_token=oidc_token,
                token_endpoint=self.token_endpoint,
                subject_token=subject_token,
                subject_token_type=subject_token_type,
                scope=self.scope,
                requested_token_type=requested_token_type,
            )

        elif self.authn_method == TokenAuthnMethod.PCA:
            if StringUtil.is_blank(self.application_federated_credential_name):
                raise ValueError("applicationFederatedCredentialName is blank")
            if StringUtil.is_blank(self.client_x509_certificate):
                raise ValueError("clientX509Certificate is blank")
            if StringUtil.is_blank(self.x509_cert_chains):
                raise ValueError("x509CertChains is blank")
            if self.client_assertion_provider is None:
                raise ValueError("clientAssertionProvider is null")
            return OAuth2TokenUtil.token_exchange_with_pca(
                client_id=self.client_id,
                application_federated_credential_name=self.application_federated_credential_name,
                client_x509_certificate=self.client_x509_certificate,
                x509_cert_chains=self.x509_cert_chains,
                client_assertion=self.client_assertion_provider.get_client_assertion(),
                token_endpoint=self.token_endpoint,
                subject_token=subject_token,
                subject_token_type=subject_token_type,
                scope=self.scope,
                requested_token_type=requested_token_type,
            )

        raise CredentialException(
            ErrorCode.UNSUPPORTED_AUTHENTICATION_METHOD,
            f"Unsupported authentication method: {self.authn_method}",
        )

    def _get_client_secret(self) -> str:
        if self.client_secret_supplier is not None:
            return self.client_secret_supplier()

        client_secret = os.getenv("ALIBABA_CLOUD_EIAM_APP_CLIENT_SECRET")
        if StringUtil.is_blank(client_secret):
            raise ValueError("clientSecret is blank")
        return client_secret


class IDaaSMachineTokenExchangeCredentialProviderBuilder:
    def __init__(self):
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

    def client_id(self, value: str) -> "IDaaSMachineTokenExchangeCredentialProviderBuilder":
        self._client_id = value
        return self

    def scope(self, value: str) -> "IDaaSMachineTokenExchangeCredentialProviderBuilder":
        self._scope = value
        return self

    def token_endpoint(self, value: str) -> "IDaaSMachineTokenExchangeCredentialProviderBuilder":
        self._token_endpoint = value
        return self

    def authn_method(self, value: TokenAuthnMethod) -> "IDaaSMachineTokenExchangeCredentialProviderBuilder":
        self._authn_method = value
        return self

    def client_secret_supplier(self, value: Callable[[], str]) -> "IDaaSMachineTokenExchangeCredentialProviderBuilder":
        self._client_secret_supplier = value
        return self

    def client_assertion_provider(
        self, value: JwtClientAssertionProvider
    ) -> "IDaaSMachineTokenExchangeCredentialProviderBuilder":
        self._client_assertion_provider = value
        return self

    def application_federated_credential_name(self, value: str) -> "IDaaSMachineTokenExchangeCredentialProviderBuilder":
        self._application_federated_credential_name = value
        return self

    def attested_document_provider(
        self, value: Pkcs7AttestedDocumentProvider
    ) -> "IDaaSMachineTokenExchangeCredentialProviderBuilder":
        self._attested_document_provider = value
        return self

    def oidc_token_provider(self, value: OidcTokenProvider) -> "IDaaSMachineTokenExchangeCredentialProviderBuilder":
        self._oidc_token_provider = value
        return self

    def client_x509_certificate(self, value: str) -> "IDaaSMachineTokenExchangeCredentialProviderBuilder":
        self._client_x509_certificate = value
        return self

    def x509_cert_chains(self, value: str) -> "IDaaSMachineTokenExchangeCredentialProviderBuilder":
        self._x509_cert_chains = value
        return self

    def build(self) -> IDaaSMachineTokenExchangeCredentialProvider:
        return IDaaSMachineTokenExchangeCredentialProvider(
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
        )
