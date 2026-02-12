"""
IDaaS Python SDK - IDaaS Credential Provider Factory
"""

import logging
import os
from typing import Optional

from cloud_idaas.core.config import HttpConfiguration, IDaaSClientConfig
from cloud_idaas.core.constants import (
    AuthenticationIdentityEnum,
    ClientDeployEnvironmentEnum,
    ErrorCode,
)
from cloud_idaas.core.exceptions import ConfigException
from cloud_idaas.core.provider import IDaaSCredentialProvider, OidcTokenProvider
from cloud_idaas.core.util import JSONUtil, TokenAuthnMethod, ValidatorUtil
from cloud_idaas.core.util.config_reader import ConfigReader


class IDaaSCredentialProviderFactory:
    """
    Factory for creating IDaaS credential providers.
    """

    _idaas_client_config: IDaaSClientConfig = IDaaSClientConfig()
    _initialized: bool = False
    _human_federate_credential_oidc_token_provider: Optional[OidcTokenProvider] = None
    _credential_providers: dict = {}

    _logger = logging.getLogger(__name__)

    @classmethod
    def init(cls, config_path: str = None) -> None:
        """
        Initialize the factory with configuration from config file.

        Args:
            config_path: Optional. Custom config file path.
                        If not provided, will use environment variable or default path.
        """
        if cls._initialized:
            cls._logger.info("IDaaS Credential Provider Factory has been initialized.")
            return

        try:
            config_content = ConfigReader.get_config_as_string(config_path)
            config_data = JSONUtil.parse_object(config_content, IDaaSClientConfig)
            cls._idaas_client_config.assign(config_data)
            cls._validate_client_config(cls._idaas_client_config)
            cls._validate_http_config(cls._idaas_client_config.http_configuration)
            cls._initialized = True
        except Exception:
            cls._logger.error("IDaaS Credential Provider Factory init failed.", exc_info=True)
            raise ConfigException(
                ErrorCode.IDAAS_CREDENTIAL_PROVIDER_FACTORY_NOT_INIT, "IDaaS Credential Provider Factory init failed."
            )

        cls._init_credential_provider()

    @classmethod
    def init_with_config(cls, authentication_config: IDaaSClientConfig) -> None:
        """
        Initialize the factory with provided configuration.

        Args:
            authentication_config: The authentication configuration.
        """
        if cls._initialized:
            cls._logger.info("IDaaS Credential Provider Factory has been initialized.")
            return

        cls._idaas_client_config.assign(authentication_config)
        cls._validate_client_config(cls._idaas_client_config)
        cls._initialized = True

    @classmethod
    def _init_credential_provider(cls) -> None:
        """Initialize credential provider based on configuration."""
        if not cls._initialized:
            return

        # If the identity type is human, trigger login in the Init method
        authentication_configuration = cls._idaas_client_config.authn_configuration
        if authentication_configuration.identity_type == AuthenticationIdentityEnum.HUMAN:
            # Note: HumanFederatedOidcTokenProvider will be implemented later
            cls._logger.info("Human identity type detected. OIDC token provider initialization will be implemented.")

        scope = cls._idaas_client_config.scope
        if scope not in cls._credential_providers:
            cls._credential_providers[scope] = cls._create_credential_provider(scope)

    @classmethod
    def _validate_client_config(cls, client_config: IDaaSClientConfig) -> None:
        """
        Validate client configuration.

        Args:
            client_config: The client configuration to validate.
        """
        ValidatorUtil.validate_base_config(client_config)
        if client_config.authn_configuration.identity_type == AuthenticationIdentityEnum.HUMAN:
            ValidatorUtil.validate_human_config(client_config)
        else:
            ValidatorUtil.validate_client_config(client_config)

    @classmethod
    def _validate_http_config(cls, http_configuration: HttpConfiguration) -> None:
        """
        Validate HTTP configuration.

        Args:
            http_configuration: The HTTP configuration to validate.
        """
        ValidatorUtil.validate_http_config(http_configuration)

    @classmethod
    def get_idaas_credential_provider(cls) -> IDaaSCredentialProvider:
        """
        Get the default IDaaS credential provider.

        Returns:
            The IDaaS credential provider.

        Raises:
            ConfigException: If factory has not been initialized.
        """
        return cls.get_idaas_credential_provider_by_scope(cls._idaas_client_config.scope)

    @classmethod
    def get_idaas_credential_provider_by_scope(cls, scope: str) -> IDaaSCredentialProvider:
        """
        Get the IDaaS credential provider for a specific scope.

        Args:
            scope: The OAuth scope.

        Returns:
            The IDaaS credential provider.

        Raises:
            ConfigException: If factory has not been initialized.
        """
        if not cls._initialized:
            raise ConfigException(
                ErrorCode.IDAAS_CREDENTIAL_PROVIDER_FACTORY_NOT_INIT,
                "IDaaS Credential Provider Factory has not been initialized.",
            )

        if scope not in cls._credential_providers:
            cls._credential_providers[scope] = cls._create_credential_provider(scope)

        return cls._credential_providers[scope]

    @classmethod
    def _create_credential_provider(cls, scope: str) -> IDaaSCredentialProvider:
        """
        Create a credential provider for the given scope.

        Args:
            scope: The OAuth scope.

        Returns:
            The created credential provider.

        Raises:
            ConfigException: If authentication method is not supported.
        """
        from cloud_idaas.core.implementation.authentication.jwt.static_client_secret_assertion_provider import (
            StaticClientSecretAssertionProvider,
        )
        from cloud_idaas.core.implementation.authentication.jwt.static_private_key_assertion_provider import (
            StaticPrivateKeyAssertionProvider,
        )
        from cloud_idaas.core.implementation.authentication.oidc.file_oidc_token_provider import FileOidcTokenProvider
        from cloud_idaas.core.implementation.authentication.oidc.static_oidc_token_provider import (
            StaticOidcTokenProvider,
        )
        from cloud_idaas.core.implementation.authentication.pkcs7.alibaba_cloud_ecs_attested_document_provider import (
            AlibabaCloudEcsAttestedDocumentProvider,
        )
        from cloud_idaas.core.implementation.authentication.pkcs7.aws_ec2_pkcs7_attested_document_provider import (
            AwsEc2Pkcs7AttestedDocumentProvider,
        )
        from cloud_idaas.core.implementation.authentication.pkcs7.static_pkcs7_attested_document_provider import (
            StaticPkcs7AttestedDocumentProvider,
        )
        from cloud_idaas.core.implementation.idaas_machine_credential_provider import (
            IDaaSMachineCredentialProviderBuilder,
        )

        config = cls._idaas_client_config
        authn_config = config.authn_configuration
        authn_method = authn_config.authn_method

        # Create builder with common configuration
        builder = IDaaSMachineCredentialProviderBuilder()
        builder.client_id(config.client_id)
        builder.scope(scope)
        builder.token_endpoint(config.token_endpoint)
        builder.authn_method(authn_method)

        # Configure based on authentication method
        if authn_method == TokenAuthnMethod.CLIENT_SECRET_BASIC or authn_method == TokenAuthnMethod.CLIENT_SECRET_POST:
            # Client secret authentication
            if authn_config.client_secret_env_var_name:

                def get_client_secret():
                    secret = os.environ.get(authn_config.client_secret_env_var_name)
                    if not secret:
                        raise ValueError(f"Environment variable {authn_config.client_secret_env_var_name} is not set")
                    return secret

                builder.client_secret_supplier(get_client_secret)

        elif authn_method == TokenAuthnMethod.CLIENT_SECRET_JWT:
            # Client secret JWT assertion
            if authn_config.client_secret_env_var_name:

                def get_client_secret():
                    secret = os.environ.get(authn_config.client_secret_env_var_name)
                    if not secret:
                        raise ValueError(f"Environment variable {authn_config.client_secret_env_var_name} is not set")
                    return secret

                assertion_provider = StaticClientSecretAssertionProvider(get_client_secret)
                assertion_provider.client_id = config.client_id
                assertion_provider.token_endpoint = config.token_endpoint
                assertion_provider.scope = scope
                builder.client_assertion_provider(assertion_provider)

        elif authn_method == TokenAuthnMethod.PRIVATE_KEY_JWT:
            # Private key JWT assertion
            if authn_config.private_key_env_var_name:
                private_key = os.environ.get(authn_config.private_key_env_var_name)
                if not private_key:
                    raise ValueError(f"Environment variable {authn_config.private_key_env_var_name} is not set")
                assertion_provider = StaticPrivateKeyAssertionProvider(private_key)
                assertion_provider.client_id = config.client_id
                assertion_provider.token_endpoint = config.token_endpoint
                assertion_provider.scope = scope
                builder.client_assertion_provider(assertion_provider)

        elif authn_method == TokenAuthnMethod.PKCS7:
            # PKCS7 attested document
            builder.application_federated_credential_name(authn_config.application_federated_credential_name)

            # Create attested document provider based on deployment environment
            if authn_config.client_deploy_environment == ClientDeployEnvironmentEnum.ALIBABA_CLOUD_ECS:
                attested_provider = AlibabaCloudEcsAttestedDocumentProvider()
            elif authn_config.client_deploy_environment == ClientDeployEnvironmentEnum.AWS_EC2:
                attested_provider = AwsEc2Pkcs7AttestedDocumentProvider()
            else:
                # Static PKCS7 attested document
                attested_provider = StaticPkcs7AttestedDocumentProvider()
            builder.attested_document_provider(attested_provider)

        elif authn_method == TokenAuthnMethod.OIDC:
            # OIDC token
            builder.application_federated_credential_name(authn_config.application_federated_credential_name)

            # Create OIDC token provider
            if authn_config.oidc_token_file_path_env_var_name:
                token_file_path = os.environ.get(authn_config.oidc_token_file_path_env_var_name)
                if token_file_path:
                    oidc_provider = FileOidcTokenProvider(token_file_path)
                else:
                    oidc_provider = StaticOidcTokenProvider()
            elif authn_config.oidc_token_file_path:
                oidc_provider = FileOidcTokenProvider(authn_config.oidc_token_file_path)
            else:
                oidc_provider = StaticOidcTokenProvider()
            builder.oidc_token_provider(oidc_provider)

        elif authn_method == TokenAuthnMethod.PCA:
            # Private Certificate Authority
            builder.application_federated_credential_name(authn_config.application_federated_credential_name)
            builder.client_x509_certificate(authn_config.client_x509_certificate)
            builder.x509_cert_chains(authn_config.x509_cert_chains)

            # Need client assertion provider for PCA
            if authn_config.private_key_env_var_name:
                private_key = os.environ.get(authn_config.private_key_env_var_name)
                if not private_key:
                    raise ValueError(f"Environment variable {authn_config.private_key_env_var_name} is not set")
                assertion_provider = StaticPrivateKeyAssertionProvider(private_key)
                assertion_provider.client_id = config.client_id
                assertion_provider.token_endpoint = config.token_endpoint
                assertion_provider.scope = scope
                builder.client_assertion_provider(assertion_provider)

        else:
            raise ConfigException(
                ErrorCode.UNSUPPORTED_AUTHENTICATION_METHOD, f"Unsupported authentication method: {authn_method}"
            )

        return builder.build()

    @classmethod
    def get_developer_api_endpoint(cls) -> str:
        """
        Get the developer API endpoint.

        Returns:
            The developer API endpoint.

        Raises:
            ConfigException: If factory has not been initialized.
        """
        if not cls._initialized:
            raise ConfigException(
                ErrorCode.IDAAS_CREDENTIAL_PROVIDER_FACTORY_NOT_INIT,
                "IDaaS Credential Provider Factory has not been initialized.",
            )
        return cls._idaas_client_config.developer_api_endpoint

    @classmethod
    def get_idaas_instance_id(cls) -> str:
        """
        Get the IDaaS instance ID.

        Returns:
            The IDaaS instance ID.

        Raises:
            ConfigException: If factory has not been initialized.
        """
        if not cls._initialized:
            raise ConfigException(
                ErrorCode.IDAAS_CREDENTIAL_PROVIDER_FACTORY_NOT_INIT,
                "IDaaS Credential Provider Factory has not been initialized.",
            )
        return cls._idaas_client_config.idaas_instance_id

    @classmethod
    def get_http_config(cls) -> HttpConfiguration:
        """
        Get the HTTP configuration.

        Returns:
            The HTTP configuration.

        Raises:
            ConfigException: If factory has not been initialized.
        """
        if not cls._initialized:
            raise ConfigException(
                ErrorCode.IDAAS_CREDENTIAL_PROVIDER_FACTORY_NOT_INIT,
                "IDaaS Credential Provider Factory has not been initialized.",
            )
        return cls._idaas_client_config.http_configuration

    @classmethod
    def reset(cls) -> None:
        """Reset the factory state (useful for testing)."""
        cls._initialized = False
        cls._idaas_client_config = IDaaSClientConfig()
        cls._human_federate_credential_oidc_token_provider = None
        cls._credential_providers.clear()
