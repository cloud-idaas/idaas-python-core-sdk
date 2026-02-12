"""
IDaaS Python SDK - OAuth2 Token Utility
"""

import base64
from typing import Optional

from cloud_idaas.core.constants import ClientAssertionType, HttpConstants, OAuth2Constants
from cloud_idaas.core.credential import IDaaSTokenResponse
from cloud_idaas.core.domain import DeviceCodeResponse
from cloud_idaas.core.exceptions import ClientException
from cloud_idaas.core.http.content_type import ContentType
from cloud_idaas.core.http.default_http_client import HttpClientFactory
from cloud_idaas.core.http.http_method import HttpMethod
from cloud_idaas.core.http.http_request import Builder
from cloud_idaas.core.util.json_util import JSONUtil


class OAuth2TokenUtil:
    """
    Utility class for OAuth2 token operations.
    """

    DEFAULT_GRANT_TYPE = OAuth2Constants.CLIENT_CREDENTIALS_GRANT_TYPE_VALUE
    AUTHORIZATION_PENDING = "authorization_pending"
    SLOW_DOWN = "slow_down"

    @classmethod
    def get_token_with_client_secret_basic(
        cls, client_id: str, client_secret: str, token_endpoint: str, scope: str
    ) -> IDaaSTokenResponse:
        """
        Get token using client_secret_basic authentication.

        Args:
            client_id: Client ID.
            client_secret: Client secret.
            token_endpoint: Token endpoint URL.
            scope: OAuth scope.

        Returns:
            IDaaSTokenResponse.
        """
        headers = {
            HttpConstants.CONTENT_TYPE_HEADER: [str(ContentType.FORM)],
            HttpConstants.AUTHORIZATION_HEADER: [
                f"{HttpConstants.BASIC} {cls._base64_encode(f'{client_id}:{client_secret}')}"
            ],
        }

        form_body = {
            OAuth2Constants.CLIENT_ID: [client_id],
            OAuth2Constants.GRANT_TYPE: [cls.DEFAULT_GRANT_TYPE],
            OAuth2Constants.SCOPE: [scope],
        }

        request = (
            Builder()
            .url(token_endpoint)
            .http_method(HttpMethod.POST)
            .headers(headers)
            .form_body(form_body)
            .content_type(ContentType.FORM)
            .build()
        )

        http_client = HttpClientFactory.get_default_http_client()
        response = http_client.send(request)
        return JSONUtil.parse_object(response.body, IDaaSTokenResponse)

    @classmethod
    def get_token_with_client_secret_post(
        cls, client_id: str, client_secret: str, token_endpoint: str, scope: str
    ) -> IDaaSTokenResponse:
        """
        Get token using client_secret_post authentication.

        Args:
            client_id: Client ID.
            client_secret: Client secret.
            token_endpoint: Token endpoint URL.
            scope: OAuth scope.

        Returns:
            IDaaSTokenResponse.
        """
        form_body = {
            OAuth2Constants.CLIENT_ID: [client_id],
            OAuth2Constants.CLIENT_SECRET: [client_secret],
            OAuth2Constants.GRANT_TYPE: [cls.DEFAULT_GRANT_TYPE],
            OAuth2Constants.SCOPE: [scope],
        }
        return cls._post_token_endpoint(form_body, token_endpoint)

    @classmethod
    def _post_token_endpoint(cls, form_body: dict, token_endpoint: str) -> Optional[IDaaSTokenResponse]:
        """
        Post request to token endpoint.

        Args:
            form_body: Form body parameters.
            token_endpoint: Token endpoint URL.

        Returns:
            IDaaSTokenResponse or None if authorization pending.
        """
        headers = {HttpConstants.CONTENT_TYPE_HEADER: [str(ContentType.FORM)]}

        request = (
            Builder()
            .url(token_endpoint)
            .http_method(HttpMethod.POST)
            .headers(headers)
            .form_body(form_body)
            .content_type(ContentType.FORM)
            .build()
        )

        http_client = HttpClientFactory.get_default_http_client()

        try:
            response = http_client.send(request)
        except ClientException as e:
            if e.error_code != cls.AUTHORIZATION_PENDING and e.error_code != cls.SLOW_DOWN:
                raise
            return None

        return JSONUtil.parse_object(response.body, IDaaSTokenResponse)

    @classmethod
    def get_token_with_client_assertion(
        cls, client_id: str, client_assertion: str, token_endpoint: str, scope: str
    ) -> IDaaSTokenResponse:
        """
        Get token using client assertion (JWT).

        Args:
            client_id: Client ID.
            client_assertion: Client assertion (JWT).
            token_endpoint: Token endpoint URL.
            scope: OAuth scope.

        Returns:
            IDaaSTokenResponse.
        """
        form_body = {
            OAuth2Constants.CLIENT_ID: [client_id],
            OAuth2Constants.CLIENT_ASSERTION_TYPE: [ClientAssertionType.OAUTH_JWT_BEARER],
            OAuth2Constants.CLIENT_ASSERTION: [client_assertion],
            OAuth2Constants.GRANT_TYPE: [cls.DEFAULT_GRANT_TYPE],
            OAuth2Constants.SCOPE: [scope],
        }
        return cls._post_token_endpoint(form_body, token_endpoint)

    @classmethod
    def get_token_with_pca(
        cls,
        client_id: str,
        application_federated_credential_name: str,
        client_x509_certificate: str,
        x509_cert_chains: str,
        client_assertion: str,
        token_endpoint: str,
        scope: str,
    ) -> IDaaSTokenResponse:
        """
        Get token using PCA (Private Certificate Authority) authentication.

        Args:
            client_id: Client ID.
            application_federated_credential_name: Application federated credential name.
            client_x509_certificate: Client X509 certificate.
            x509_cert_chains: X509 certificate chains.
            client_assertion: Client assertion.
            token_endpoint: Token endpoint URL.
            scope: OAuth scope.

        Returns:
            IDaaSTokenResponse.
        """
        form_body = {
            OAuth2Constants.CLIENT_ID: [client_id],
            OAuth2Constants.APPLICATION_FEDERATED_CREDENTIAL_NAME: [application_federated_credential_name],
            OAuth2Constants.CLIENT_ASSERTION_TYPE: [ClientAssertionType.PRIVATE_CA_JWT_BEARER],
            OAuth2Constants.CLIENT_ASSERTION: [client_assertion],
            OAuth2Constants.CLIENT_X509_CERTIFICATE: [client_x509_certificate],
            OAuth2Constants.X509_CERT_CHAINS: [x509_cert_chains],
            OAuth2Constants.GRANT_TYPE: [cls.DEFAULT_GRANT_TYPE],
            OAuth2Constants.SCOPE: [scope],
        }
        return cls._post_token_endpoint(form_body, token_endpoint)

    @classmethod
    def get_token_with_pkcs7_attested_document(
        cls,
        client_id: str,
        application_federated_credential_name: str,
        pkcs7_attested_document: str,
        token_endpoint: str,
        scope: str,
    ) -> IDaaSTokenResponse:
        """
        Get token using PKCS7 attested document.

        Args:
            client_id: Client ID.
            application_federated_credential_name: Application federated credential name.
            pkcs7_attested_document: PKCS7 attested document.
            token_endpoint: Token endpoint URL.
            scope: OAuth scope.

        Returns:
            IDaaSTokenResponse.
        """
        form_body = {
            OAuth2Constants.CLIENT_ID: [client_id],
            OAuth2Constants.APPLICATION_FEDERATED_CREDENTIAL_NAME: [application_federated_credential_name],
            OAuth2Constants.CLIENT_ASSERTION_TYPE: [ClientAssertionType.PKCS7_BEARER],
            OAuth2Constants.CLIENT_ASSERTION: [pkcs7_attested_document],
            OAuth2Constants.GRANT_TYPE: [cls.DEFAULT_GRANT_TYPE],
            OAuth2Constants.SCOPE: [scope],
        }
        return cls._post_token_endpoint(form_body, token_endpoint)

    @classmethod
    def get_token_with_oidc_federated_credential(
        cls,
        client_id: str,
        application_federated_credential_name: str,
        oidc_token: str,
        token_endpoint: str,
        scope: str,
    ) -> IDaaSTokenResponse:
        """
        Get token using OIDC federated credential.

        Args:
            client_id: Client ID.
            application_federated_credential_name: Application federated credential name.
            oidc_token: OIDC token.
            token_endpoint: Token endpoint URL.
            scope: OAuth scope.

        Returns:
            IDaaSTokenResponse.
        """
        form_body = {
            OAuth2Constants.CLIENT_ID: [client_id],
            OAuth2Constants.APPLICATION_FEDERATED_CREDENTIAL_NAME: [application_federated_credential_name],
            OAuth2Constants.CLIENT_ASSERTION_TYPE: [ClientAssertionType.OIDC_BEARER],
            OAuth2Constants.CLIENT_ASSERTION: [oidc_token],
            OAuth2Constants.GRANT_TYPE: [cls.DEFAULT_GRANT_TYPE],
            OAuth2Constants.SCOPE: [scope],
        }
        return cls._post_token_endpoint(form_body, token_endpoint)

    @classmethod
    def token_exchange(cls, audience: str, subject_token: str, token_endpoint: str, scope: str) -> IDaaSTokenResponse:
        """
        Perform token exchange.

        Args:
            audience: Audience for the exchanged token.
            subject_token: Subject token to exchange.
            token_endpoint: Token endpoint URL.
            scope: OAuth scope.

        Returns:
            IDaaSTokenResponse.
        """
        form_body = {
            OAuth2Constants.GRANT_TYPE: [OAuth2Constants.TOKEN_EXCHANGE_GRANT_TYPE_VALUE],
            OAuth2Constants.AUDIENCE: [audience],
            OAuth2Constants.SUBJECT_TOKEN: [subject_token],
            OAuth2Constants.SUBJECT_TOKEN_TYPE: [OAuth2Constants.SUBJECT_TOKEN_TYPE_VALUE],
            OAuth2Constants.REQUESTED_TOKEN_TYPE: [OAuth2Constants.REQUESTED_TOKEN_TYPE_VALUE],
            OAuth2Constants.SCOPE: [scope],
        }
        return cls._post_token_endpoint(form_body, token_endpoint)

    @classmethod
    def get_device_code(cls, client_id: str, scope: str, device_authorization: str) -> DeviceCodeResponse:
        """
        Get device code for device flow.

        Args:
            client_id: Client ID.
            scope: OAuth scope.
            device_authorization: Device authorization endpoint URL.

        Returns:
            DeviceCodeResponse.
        """
        headers = {HttpConstants.CONTENT_TYPE_HEADER: [str(ContentType.FORM)]}

        form_body = {OAuth2Constants.CLIENT_ID: [client_id], OAuth2Constants.SCOPE: [scope]}

        request = (
            Builder()
            .url(device_authorization)
            .http_method(HttpMethod.POST)
            .headers(headers)
            .form_body(form_body)
            .content_type(ContentType.FORM)
            .build()
        )

        http_client = HttpClientFactory.get_default_http_client()
        response = http_client.send(request)
        return JSONUtil.parse_object(response.body, DeviceCodeResponse)

    @classmethod
    def get_token_by_device_code(
        cls, client_id: str, device_code: str, token_endpoint: str
    ) -> Optional[IDaaSTokenResponse]:
        """
        Get token using device code.

        Args:
            client_id: Client ID.
            device_code: Device code.
            token_endpoint: Token endpoint URL.

        Returns:
            IDaaSTokenResponse or None if authorization pending.
        """
        form_body = {
            OAuth2Constants.GRANT_TYPE: [OAuth2Constants.DEVICE_CODE_GRANT_TYPE_VALUE],
            OAuth2Constants.CLIENT_ID: [client_id],
            OAuth2Constants.DEVICE_CODE: [device_code],
        }
        return cls._post_token_endpoint(form_body, token_endpoint)

    @classmethod
    def refresh_token(cls, client_id: str, refresh_token: str, token_endpoint: str) -> IDaaSTokenResponse:
        """
        Refresh access token using refresh token.

        Args:
            client_id: Client ID.
            refresh_token: Refresh token.
            token_endpoint: Token endpoint URL.

        Returns:
            IDaaSTokenResponse.
        """
        form_body = {
            OAuth2Constants.GRANT_TYPE: [OAuth2Constants.REFRESH_TOKEN_GRANT_TYPE_VALUE],
            OAuth2Constants.CLIENT_ID: [client_id],
            OAuth2Constants.REFRESH_TOKEN_PARAMETER: [refresh_token],
        }
        return cls._post_token_endpoint(form_body, token_endpoint)

    @staticmethod
    def _base64_encode(s: str) -> str:
        """
        Base64 encode a string.

        Args:
            s: String to encode.

        Returns:
            Base64 encoded string.
        """
        return base64.b64encode(s.encode("utf-8")).decode("utf-8")
