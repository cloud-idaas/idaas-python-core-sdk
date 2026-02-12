"""
IDaaS Python SDK - Validator Utility

This module provides validation utilities.
"""

from typing import Optional, TypeVar

from cloud_idaas.core.config.http_configuration import HttpConfiguration
from cloud_idaas.core.config.idaas_client_config import IDaaSClientConfig
from cloud_idaas.core.constants import ErrorCode, HttpConstants, TokenAuthnMethod
from cloud_idaas.core.credential import IDaaSTokenResponse
from cloud_idaas.core.exceptions import CacheException, ConfigException

T = TypeVar("T")


class ValidatorUtil:
    """
    Utility class for validation operations.
    """

    @staticmethod
    def validate_config_not_none(o: Optional[T], error_code: str, error_message: str) -> None:
        """
        Validate that a configuration value is not None.

        Args:
            o: Value to validate.
            error_code: Error code to use if validation fails.
            error_message: Error message to use if validation fails.

        Raises:
            ConfigException: If the value is None.
        """
        if o is None:
            raise ConfigException(error_code, error_message)

    @staticmethod
    def validate_token_not_none(o: Optional[T], error_code: str, error_message: str) -> None:
        """
        Validate that a token value is not None.

        Args:
            o: Value to validate.
            error_code: Error code to use if validation fails.
            error_message: Error message to use if validation fails.

        Raises:
            CacheException: If the value is None.
        """
        if o is None:
            raise CacheException(error_code, error_message)

    @staticmethod
    def validate_base_config(idaas_client_config: IDaaSClientConfig) -> None:
        """
        Validate base IDaaS client configuration.

        Args:
            idaas_client_config: The configuration to validate.

        Raises:
            ConfigException: If validation fails.
        """
        ValidatorUtil.validate_config_not_none(
            idaas_client_config.idaas_instance_id, ErrorCode.IDAAS_INSTANCE_ID_NOT_FOUND, "IDaaS Instance ID not found."
        )
        ValidatorUtil.validate_config_not_none(
            idaas_client_config.client_id, ErrorCode.CLIENT_ID_NOT_FOUND, "Client ID not found."
        )
        ValidatorUtil.validate_config_not_none(
            idaas_client_config.issuer, ErrorCode.ISSUER_ENDPOINT_NOT_FOUND, "Issuer Endpoint not found"
        )
        ValidatorUtil.validate_config_not_none(
            idaas_client_config.token_endpoint, ErrorCode.TOKEN_ENDPOINT_NOT_FOUND, "Token Endpoint not found."
        )
        ValidatorUtil.validate_config_not_none(
            idaas_client_config.developer_api_endpoint,
            ErrorCode.DEVELOPER_API_ENDPOINT_NOT_FOUND,
            "Developer Api Endpoint not found.",
        )

    @staticmethod
    def validate_human_config(idaas_client_config: IDaaSClientConfig) -> None:
        """
        Validate human authentication configuration.

        Args:
            idaas_client_config: The configuration to validate.

        Raises:
            ConfigException: If validation fails.
        """
        ValidatorUtil.validate_config_not_none(
            idaas_client_config.authn_configuration.human_authenticate_client_id,
            ErrorCode.HUMAN_AUTHENTICATE_CLIENT_ID_NOT_FOUND,
            "Human Authenticate Client ID not found.",
        )
        ValidatorUtil.validate_config_not_none(
            idaas_client_config.device_authorization_endpoint,
            ErrorCode.DEVICE_AUTHORIZATION_ENDPOINT_NOT_FOUND,
            "Device Authorization Endpoint not found.",
        )

    @staticmethod
    def validate_client_config(idaas_client_config: IDaaSClientConfig) -> None:
        """
        Validate client authentication configuration.

        Args:
            idaas_client_config: The configuration to validate.

        Raises:
            ConfigException: If validation fails.
        """
        authn_configuration = idaas_client_config.authn_configuration
        if authn_configuration is None:
            raise ConfigException(ErrorCode.AUTHN_CONFIGURATION_NOT_FOUND, "Authn Configuration not found.")

        authn_method = authn_configuration.authn_method

        if authn_method in (
            TokenAuthnMethod.CLIENT_SECRET_BASIC,
            TokenAuthnMethod.CLIENT_SECRET_POST,
            TokenAuthnMethod.CLIENT_SECRET_JWT,
        ):
            ValidatorUtil.validate_config_not_none(
                authn_configuration.client_secret_env_var_name,
                ErrorCode.CLIENT_SECRET_ENV_VAR_NAME_NOT_FOUND,
                "Client Secret Env Var Name not found.",
            )
        elif authn_method == TokenAuthnMethod.PRIVATE_KEY_JWT:
            ValidatorUtil.validate_config_not_none(
                authn_configuration.private_key_env_var_name,
                ErrorCode.PRIVATE_KEY_ENV_VAR_NAME_NOT_FOUND,
                "Private Key Env Var Name not found.",
            )
        elif authn_method in (TokenAuthnMethod.PKCS7, TokenAuthnMethod.OIDC):
            ValidatorUtil.validate_config_not_none(
                authn_configuration.application_federated_credential_name,
                ErrorCode.APPLICATION_FEDERATED_CREDENTIAL_NAME_NOT_FOUND,
                "Application Federated Credential Name not found.",
            )
            ValidatorUtil.validate_config_not_none(
                authn_configuration.client_deploy_environment,
                ErrorCode.CLIENT_DEPLOY_ENVIRONMENT_NOT_FOUND,
                "Client Deploy Environment not found.",
            )
        elif authn_method == TokenAuthnMethod.PCA:
            ValidatorUtil.validate_config_not_none(
                authn_configuration.application_federated_credential_name,
                ErrorCode.APPLICATION_FEDERATED_CREDENTIAL_NAME_NOT_FOUND,
                "Application Federated Credential Name not found.",
            )
            ValidatorUtil.validate_config_not_none(
                authn_configuration.client_x509_certificate,
                ErrorCode.CLIENT_X509_CERTIFICATE_NOT_FOUND,
                "Client X509 Certificate not found.",
            )
            ValidatorUtil.validate_config_not_none(
                authn_configuration.x509_cert_chains,
                ErrorCode.X509_CERT_CHAINS_NOT_FOUND,
                "X509 Cert Chains not found.",
            )
            ValidatorUtil.validate_config_not_none(
                authn_configuration.private_key_env_var_name,
                ErrorCode.PRIVATE_KEY_ENV_VAR_NAME_NOT_FOUND,
                "Private Key Env Var Name not found.",
            )

    @staticmethod
    def validate_http_config(http_configuration: HttpConfiguration) -> None:
        """
        Validate HTTP configuration.

        Args:
            http_configuration: The HTTP configuration to validate.

        Raises:
            ConfigException: If validation fails.
        """
        if http_configuration is not None:
            if http_configuration.connect_timeout < 2000 or http_configuration.connect_timeout > 60000:
                raise ConfigException(ErrorCode.CONNECT_TIMEOUT_NOT_VALID, "Connect Timeout not valid.")
            if http_configuration.read_timeout < 2000 or http_configuration.read_timeout > 60000:
                raise ConfigException(ErrorCode.READ_TIMEOUT_NOT_VALID, "Read Timeout not valid.")

    @staticmethod
    def validate_local_token(local_token: IDaaSTokenResponse) -> None:
        """
        Validate local token.

        Args:
            local_token: The token to validate.

        Raises:
            CacheException: If validation fails.
        """
        if not TokenAuthnMethod.equals(local_token.token_type, HttpConstants.BEARER):
            raise CacheException(ErrorCode.INVALID_TOKEN_TYPE, f"Invalid local token type: {local_token.token_type}.")
        ValidatorUtil.validate_token_not_none(
            local_token.access_token, ErrorCode.ACCESS_TOKEN_NOT_FOUND, "Access Token not found."
        )
        ValidatorUtil.validate_token_not_none(local_token.id_token, ErrorCode.ID_TOKEN_NOT_FOUND, "ID Token not found.")
        ValidatorUtil.validate_token_not_none(
            local_token.refresh_token, ErrorCode.REFRESH_TOKEN_NOT_FOUND, "Refresh Token not found."
        )
