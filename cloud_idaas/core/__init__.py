"""
IDaaS Python SDK - Core Module

This is the core module of the IDaaS Python SDK.
"""

# Cache
from cloud_idaas.core.cache import (
    CachedResultSupplier,
    NonBlockingPrefetchStrategy,
    OneCallerBlocksPrefetchStrategy,
    PrefetchStrategy,
    RefreshResult,
    RefreshResultBuilder,
    StaleValueBehavior,
)

# Config
from cloud_idaas.core.config import (
    HttpConfiguration,
    IDaaSClientConfig,
    IdentityAuthenticationConfiguration,
    UserAgentConfig,
)

# Constants
from cloud_idaas.core.constants import (
    AuthenticationConstants,
    AuthenticationIdentityEnum,
    ClientAssertionType,
    ClientDeployEnvironmentEnum,
    ConfigPathConstants,
    ErrorCode,
    HttpConstants,
    OAuth2Constants,
    PluginConstants,
    TokenAuthnMethod,
)

# Credential
from cloud_idaas.core.credential import (
    IDaaSCredential,
    IDaaSTokenResponse,
)

# Domain
from cloud_idaas.core.domain import (
    DeviceCodeResponse,
    ErrResponse,
)

# Exceptions
from cloud_idaas.core.exceptions import (
    CacheException,
    ClientException,
    ConcurrentOperationException,
    ConfigException,
    CredentialException,
    EncodingException,
    HttpException,
    IDaaSException,
    ServerException,
)

# Factory
from cloud_idaas.core.factory import IDaaSCredentialProviderFactory

# HTTP
from cloud_idaas.core.http import (
    Builder,
    ContentType,
    DefaultHttpClient,
    HttpClient,
    HttpMethod,
    HttpRequest,
    HttpResponse,
    OAuth2TokenUtil,
)

# Implementation
from cloud_idaas.core.implementation import (
    AbstractRefreshedCredentialProvider,
    IDaaSMachineCredentialProvider,
    IDaaSMachineCredentialProviderBuilder,
    IDaaSMachineTokenExchangeCredentialProvider,
    IDaaSMachineTokenExchangeCredentialProviderBuilder,
)
from cloud_idaas.core.implementation.authentication import (
    AlibabaCloudEcsAttestedDocumentProvider,
    AlibabaCloudEcsAttestedDocumentProviderBuilder,
    AwsEc2Pkcs7AttestedDocumentProvider,
    FileOidcTokenProvider,
    StaticClientSecretAssertionProvider,
    StaticOidcTokenProvider,
    StaticPkcs7AttestedDocumentProvider,
    StaticPrivateKeyAssertionProvider,
)

# Provider
from cloud_idaas.core.provider import (
    IDaaSCredentialProvider,
    IDaaSTokenExchangeCredentialProvider,
    JwtClientAssertionProvider,
    OidcTokenProvider,
    Pkcs7AttestedDocumentProvider,
    PluginCredentialProvider,
    RefreshCredentialProvider,
)

# Util
from cloud_idaas.core.util import (
    BrowserUtil,
    ConfigReader,
    ExceptionAnalyzer,
    FileUtil,
    JSONUtil,
    PkiUtil,
    PluginCredentialProviderUtil,
    RequestUtil,
    ScopeUtil,
    StringUtil,
    ValidatorUtil,
)

# Version management - keep at the end, skip import sorting
from importlib import metadata  # isort: skip

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # avoids polluting the results of dir(__package__)

__author__ = "AlibabaCloud IDaaS Team"

__all__ = [
    # Constants
    "AuthenticationConstants",
    "ConfigPathConstants",
    "OAuth2Constants",
    "HttpConstants",
    "ClientAssertionType",
    "AuthenticationIdentityEnum",
    "ClientDeployEnvironmentEnum",
    "ErrorCode",
    "TokenAuthnMethod",
    "PluginConstants",
    # Exceptions
    "IDaaSException",
    "ClientException",
    "ServerException",
    "ConfigException",
    "CacheException",
    "ConcurrentOperationException",
    "CredentialException",
    "EncodingException",
    "HttpException",
    # Credential
    "IDaaSCredential",
    "IDaaSTokenResponse",
    # Domain
    "ErrResponse",
    "DeviceCodeResponse",
    # Cache
    "CachedResultSupplier",
    "PrefetchStrategy",
    "RefreshResult",
    "RefreshResultBuilder",
    "StaleValueBehavior",
    "NonBlockingPrefetchStrategy",
    "OneCallerBlocksPrefetchStrategy",
    # Config
    "HttpConfiguration",
    "IDaaSClientConfig",
    "IdentityAuthenticationConfiguration",
    "UserAgentConfig",
    # HTTP
    "HttpMethod",
    "HttpRequest",
    "Builder",
    "HttpResponse",
    "ContentType",
    "HttpClient",
    "DefaultHttpClient",
    "OAuth2TokenUtil",
    # Provider
    "IDaaSCredentialProvider",
    "IDaaSTokenExchangeCredentialProvider",
    "JwtClientAssertionProvider",
    "OidcTokenProvider",
    "Pkcs7AttestedDocumentProvider",
    "RefreshCredentialProvider",
    "PluginCredentialProvider",
    # Factory
    "IDaaSCredentialProviderFactory",
    # Implementation
    "AbstractRefreshedCredentialProvider",
    "IDaaSMachineCredentialProvider",
    "IDaaSMachineCredentialProviderBuilder",
    "IDaaSMachineTokenExchangeCredentialProvider",
    "IDaaSMachineTokenExchangeCredentialProviderBuilder",
    # Implementation - Authentication
    "StaticClientSecretAssertionProvider",
    "StaticPrivateKeyAssertionProvider",
    "FileOidcTokenProvider",
    "StaticOidcTokenProvider",
    "StaticPkcs7AttestedDocumentProvider",
    "AlibabaCloudEcsAttestedDocumentProvider",
    "AlibabaCloudEcsAttestedDocumentProviderBuilder",
    "AwsEc2Pkcs7AttestedDocumentProvider",
    # Util
    "BrowserUtil",
    "ConfigReader",
    "ExceptionAnalyzer",
    "FileUtil",
    "JSONUtil",
    "PkiUtil",
    "RequestUtil",
    "StringUtil",
    "ValidatorUtil",
    "ScopeUtil",
    "PluginCredentialProviderUtil",
]
