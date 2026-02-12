"""
IDaaS Python SDK - Authentication Constants

This module contains constant definitions used for authentication.
"""

from enum import Enum
from typing import Optional


class _StrEnum(Enum):
    """
    Base enum class that returns the value when converted to string.
    """

    def __str__(self) -> str:
        return self.value


class AuthenticationConstants:
    """
    Constants for authentication-related configurations.
    """

    # Kubernetes service account token path
    # Reference: https://kubernetes.io/docs/concepts/security/service-accounts/#get-a-token
    KUBERNETES_SERVICE_ACCOUNT_TOKEN_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/token"

    # Alibaba Cloud ECS metadata service URL
    ALIBABA_CLOUD_ECS_METADATA_SERVICE_URL = "http://100.100.100.200/latest/meta-data/"

    # Environment variable name for Alibaba Cloud ACK OIDC token file
    # Reference: https://help.aliyun.com/zh/ack/ack-managed-and-ack-dedicated/user-guide/use-rrsa-to-authorize-pods-to-access-different-cloud-services
    ALIBABA_CLOUD_ACK_OIDC_TOKEN_PATH_ENV = "ALIBABA_CLOUD_OIDC_TOKEN_FILE"

    # Default client ID environment variable name
    DEFAULT_CLIENT_ID_ENVIRONMENT_VARIABLE_NAME = "CLOUD_IDAAS_CLIENT_ID"

    # Default client secret environment variable name
    DEFAULT_CLIENT_SECRET_ENVIRONMENT_VARIABLE_NAME = "CLOUD_IDAAS_CLIENT_SECRET"


class ConfigPathConstants:
    """
    Constants for configuration file paths.
    """

    # Environment variable name for config file path
    ENV_CONFIG_PATH_KEY = "CLOUD_IDAAS_CONFIG_PATH"

    # Default config file path
    DEFAULT_CONFIG_PATH = "~/.cloud_idaas/client-config.json"

    # Environment variable name for human credential cache file path
    ENV_HUMAN_CREDENTIAL_CACHE_PATH_KEY = "CLOUD_IDAAS_HUMAN_CREDENTIAL_CACHE_PATH"

    # Default human credential cache file path template
    DEFAULT_HUMAN_CREDENTIAL_CACHE_PATH_TEMPLATE = "~/.cloud_idaas/human_credential_{}_{}.json"


class OAuth2Constants:
    """
    Constants for OAuth2 protocol parameters.
    """

    CLIENT_ID = "client_id"
    CLIENT_SECRET = "client_secret"
    SCOPE = "scope"
    DEVICE_CODE = "device_code"
    GRANT_TYPE = "grant_type"
    CLIENT_CREDENTIALS_GRANT_TYPE_VALUE = "client_credentials"
    TOKEN_EXCHANGE_GRANT_TYPE_VALUE = "urn:ietf:params:oauth:grant-type:token-exchange"
    DEVICE_CODE_GRANT_TYPE_VALUE = "urn:ietf:params:oauth:grant-type:device_code"
    REFRESH_TOKEN_GRANT_TYPE_VALUE = "refresh_token"
    CLIENT_ASSERTION_TYPE = "client_assertion_type"
    CLIENT_ASSERTION = "client_assertion"
    APPLICATION_FEDERATED_CREDENTIAL_NAME = "application_federated_credential_name"
    REFRESH_TOKEN_PARAMETER = "refresh_token"
    CLIENT_X509_CERTIFICATE = "client_x509"
    X509_CERT_CHAINS = "client_x509_chain"
    SUBJECT_TOKEN = "subject_token"
    SUBJECT_TOKEN_TYPE = "subject_token_type"
    SUBJECT_TOKEN_TYPE_VALUE = "urn:ietf:params:oauth:token-type:jwt"
    REQUESTED_TOKEN_TYPE = "requested_token_type"
    REQUESTED_TOKEN_TYPE_VALUE = "urn:ietf:params:oauth:token-type:access_token"
    AUDIENCE = "audience"


class HttpConstants:
    """
    Constants for HTTP protocol.
    """

    HTTPS = "https"
    AUTHORIZATION_HEADER = "Authorization"
    CONTENT_TYPE_HEADER = "Content-Type"
    BEARER = "Bearer"
    BASIC = "Basic"
    USER_AGENT = "User-Agent"
    LOCATION = "Location"
    REDIRECT_TO = "Redirect to: "
    X_ALIYUN_ECS_METADATA_TOKEN_TTL_SECONDS = "X-aliyun-ecs-metadata-token-ttl-seconds"
    X_ALIYUN_ECS_METADATA_TOKEN = "X-aliyun-ecs-metadata-token"
    COLON = ":"
    SPACE = " "


class ClientAssertionType:
    """
    Constants for client assertion types.
    """

    # RFC specification
    OAUTH_JWT_BEARER = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"

    # PCA (Private Certificate Authority)
    PRIVATE_CA_JWT_BEARER = "urn:cloud:idaas:params:oauth:client-assertion-type:x509-jwt-bearer"

    # PKCS7
    PKCS7_BEARER = "urn:cloud:idaas:params:oauth:client-assertion-type:pkcs7-bearer"

    # OIDC
    OIDC_BEARER = "urn:cloud:idaas:params:oauth:client-assertion-type:id-token-bearer"


class AuthenticationIdentityEnum(_StrEnum):
    """
    Enum for authentication identity types.
    """

    HUMAN = "HUMAN"
    CLIENT = "CLIENT"


class ClientDeployEnvironmentEnum(_StrEnum):
    """
    Enum for client deployment environments.
    """

    # When deploying to a common environment, only supported environment variables client assertion provider
    COMMON = "COMMON"
    COMPUTER = "COMPUTER"
    KUBERNETES = "KUBERNETES"
    ALIBABA_CLOUD_ECS = "ALIBABA_CLOUD_ECS"
    ALIBABA_CLOUD_ECI = "ALIBABA_CLOUD_ECI"
    ALIBABA_CLOUD_ACK = "ALIBABA_CLOUD_ACK"
    AWS_EC2 = "AWS_EC2"
    AWS_ESK = "AWS_ESK"
    GOOGLE_VM = "GOOGLE_VM"
    HUAWEI_CLOUD_ECS = "HUAWEI_CLOUD_ECS"

    # When deploying to a custom environment, customer need manual specified the authentication provider
    CUSTOM = "CUSTOM"


class ErrorCode:
    """
    Enum for error codes.
    """

    IDAAS_INSTANCE_ID_NOT_FOUND = "IDaaSInstanceIdNotFound"
    CLIENT_ID_NOT_FOUND = "ClientIdNotFound"
    ISSUER_ENDPOINT_NOT_FOUND = "IssuerEndpointNotFound"
    TOKEN_ENDPOINT_NOT_FOUND = "TokenEndpointNotFound"
    HUMAN_AUTHENTICATE_CLIENT_ID_NOT_FOUND = "HumanAuthenticateClientIdNotFound"
    HUMAN_AUTHENTICATE_SCOPE_NOT_FOUND = "HumanAuthenticateScopeNotFound"
    DEVICE_AUTHORIZATION_ENDPOINT_NOT_FOUND = "DeviceAuthorizationEndpointNotFound"
    AUTHN_CONFIGURATION_NOT_FOUND = "AuthnConfigurationNotFound"
    CLIENT_SECRET_ENV_VAR_NAME_NOT_FOUND = "ClientSecretEnvVarNameNotFound"
    PRIVATE_KEY_ENV_VAR_NAME_NOT_FOUND = "PrivateKeyEnvVarNameNotFound"
    APPLICATION_FEDERATED_CREDENTIAL_NAME_NOT_FOUND = "ApplicationFederatedCredentialNameNotFound"
    CLIENT_DEPLOY_ENVIRONMENT_NOT_FOUND = "ClientDeployEnvironmentNotFound"
    CLIENT_X509_CERTIFICATE_NOT_FOUND = "ClientX509CertificateNotFound"
    X509_CERT_CHAINS_NOT_FOUND = "X509CertChainsNotFound"
    UNSUPPORTED_CLIENT_DEPLOY_ENVIRONMENT = "UnsupportedClientDeployEnvironment"
    UNSUPPORTED_AUTHENTICATION_METHOD = "UnsupportedAuthenticationMethod"
    CONNECT_TIMEOUT_NOT_VALID = "ConnectTimeoutNotValid"
    READ_TIMEOUT_NOT_VALID = "ReadTimeoutNotValid"
    IDAAS_CREDENTIAL_PROVIDER_FACTORY_NOT_INIT = "IDaaSCredentialProviderFactoryNotInit"
    NOT_SUPPORTED_WEB_KEY = "NotSupportedWebKey"
    REFRESH_TOKEN_EMPTY = "RefreshTokenEmpty"
    DEVELOPER_API_ENDPOINT_NOT_FOUND = "DeveloperApiEndpointNotFound"
    LOAD_CONFIG_FILE_FAILED = "LoadConfigFileFailed"
    INVALID_REQUEST = "InvalidRequest"
    CONNECT_TIME_OUT = "ConnectTimeOut"
    READ_TIME_OUT = "ReadTimeOut"
    CLIENT_ERROR = "ClientError"
    SERVER_ERROR = "ServerError"
    INVALID_TOKEN_TYPE = "InvalidTokenType"
    ACCESS_TOKEN_NOT_FOUND = "AccessTokenNotFound"
    ID_TOKEN_NOT_FOUND = "IdTokenNotFound"
    REFRESH_TOKEN_NOT_FOUND = "RefreshTokenNotFound"


class TokenAuthnMethod(_StrEnum):
    """
    Enum for token authentication methods.
    """

    NONE = "NONE"
    CLIENT_SECRET_POST = "CLIENT_SECRET_POST"
    CLIENT_SECRET_BASIC = "CLIENT_SECRET_BASIC"
    CLIENT_SECRET_JWT = "CLIENT_SECRET_JWT"
    PRIVATE_KEY_JWT = "PRIVATE_KEY_JWT"
    # IDaaS custom defined authentication method
    PKCS7 = "PKCS7"
    PCA = "PCA"
    OIDC = "OIDC"

    @staticmethod
    def equals(method1: Optional[str], method2: Optional[str]) -> bool:
        """
        Compare two authentication method strings.

        Args:
            method1: First method string to compare.
            method2: Second method string to compare.

        Returns:
            True if both are None or equal, False otherwise.
        """
        if method1 is None and method2 is None:
            return True
        if method1 is None or method2 is None:
            return False
        return method1 == method2
