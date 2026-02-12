"""
IDaaS Python SDK

Python SDK for IDaaS (Identity as a Service) M2M product.
Based on standard OAuth and OIDC protocols.

This SDK provides functionality to obtain AccessTokens using OAuth2 client_credentials mode.
"""
from importlib import metadata

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)

__author__ = "Alibaba IDaaS Team"

# Core module exports
from cloud_idaas.core import (
    AuthenticationConstants,
    AuthenticationIdentityEnum,
    CacheException,
    ClientAssertionType,
    ClientDeployEnvironmentEnum,
    ClientException,
    ConcurrentOperationException,
    ConfigException,
    ConfigPathConstants,
    CredentialException,
    DeviceCodeResponse,
    EncodingException,
    ErrorCode,
    ErrResponse,
    HttpConstants,
    HttpException,
    IDaaSCredential,
    IDaaSException,
    IDaaSTokenResponse,
    OAuth2Constants,
    ServerException,
    TokenAuthnMethod,
)

# Cache module exports
from cloud_idaas.core.cache.refresh_result import RefreshResult
from cloud_idaas.core.cache.stale_value_behavior import StaleValueBehavior

# Config module exports
from cloud_idaas.core.config.http_configuration import HttpConfiguration
from cloud_idaas.core.config.idaas_client_config import IDaaSClientConfig
from cloud_idaas.core.config.identity_authentication_configuration import IdentityAuthenticationConfiguration
from cloud_idaas.core.config.user_agent_config import UserAgentConfig

# HTTP module exports
from cloud_idaas.core.http.content_type import ContentType
from cloud_idaas.core.http.http_client import HttpClient
from cloud_idaas.core.http.http_method import HttpMethod
from cloud_idaas.core.http.http_request import Builder, HttpRequest
from cloud_idaas.core.http.http_response import HttpResponse
from cloud_idaas.core.http.oauth2_token_util import OAuth2TokenUtil

# Implementation module exports
from cloud_idaas.core.implementation.abstract_refreshed_credential_provider import AbstractRefreshedCredentialProvider

# Authentication implementation exports
from cloud_idaas.core.implementation.authentication.jwt.static_client_secret_assertion_provider import (
    StaticClientSecretAssertionProvider,
)
from cloud_idaas.core.implementation.authentication.jwt.static_private_key_assertion_provider import (
    StaticPrivateKeyAssertionProvider,
)
from cloud_idaas.core.implementation.authentication.oidc.file_oidc_token_provider import FileOidcTokenProvider
from cloud_idaas.core.implementation.authentication.oidc.static_oidc_token_provider import StaticOidcTokenProvider
from cloud_idaas.core.implementation.authentication.pkcs7.alibaba_cloud_ecs_attested_document_provider import (
    AlibabaCloudEcsAttestedDocumentProvider,
    AlibabaCloudEcsAttestedDocumentProviderBuilder,
)
from cloud_idaas.core.implementation.authentication.pkcs7.aws_ec2_pkcs7_attested_document_provider import (
    AwsEc2Pkcs7AttestedDocumentProvider,
)
from cloud_idaas.core.implementation.authentication.pkcs7.static_pkcs7_attested_document_provider import (
    StaticPkcs7AttestedDocumentProvider,
)
from cloud_idaas.core.implementation.idaas_machine_credential_provider import (
    IDaaSMachineCredentialProvider,
    IDaaSMachineCredentialProviderBuilder,
)

# Provider module exports
from cloud_idaas.core.provider.idaas_credential_provider import IDaaSCredentialProvider
from cloud_idaas.core.provider.jwt_client_assertion_provider import JwtClientAssertionProvider
from cloud_idaas.core.provider.oidc_token_provider import OidcTokenProvider
from cloud_idaas.core.provider.pkcs7_attested_document_provider import Pkcs7AttestedDocumentProvider
from cloud_idaas.core.provider.refresh_credential_provider import RefreshCredentialProvider

# Util module exports
from cloud_idaas.core.util.browser_util import BrowserUtil
from cloud_idaas.core.util.file_util import FileUtil
from cloud_idaas.core.util.json_util import JSONUtil
from cloud_idaas.core.util.pki_util import PkiUtil
from cloud_idaas.core.util.request_util import RequestUtil
from cloud_idaas.core.util.string_util import StringUtil

__all__ = [
    "__version__",
    "__author__",
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
    # HTTP
    "HttpMethod",
    "HttpRequest",
    "Builder",
    "HttpResponse",
    "ContentType",
    "HttpClient",
    "OAuth2TokenUtil",
    # Config
    "HttpConfiguration",
    "IDaaSClientConfig",
    "IdentityAuthenticationConfiguration",
    "UserAgentConfig",
    # Provider
    "IDaaSCredentialProvider",
    "JwtClientAssertionProvider",
    "OidcTokenProvider",
    "Pkcs7AttestedDocumentProvider",
    "RefreshCredentialProvider",
    "RefreshResult",
    # Util
    "StringUtil",
    "JSONUtil",
    "FileUtil",
    "RequestUtil",
    "PkiUtil",
    "BrowserUtil",
    # Cache
    "StaleValueBehavior",
    # Implementation
    "AbstractRefreshedCredentialProvider",
    "IDaaSMachineCredentialProvider",
    "IDaaSMachineCredentialProviderBuilder",
    "StaticClientSecretAssertionProvider",
    "StaticPrivateKeyAssertionProvider",
    "StaticOidcTokenProvider",
    "FileOidcTokenProvider",
    "StaticPkcs7AttestedDocumentProvider",
    "AlibabaCloudEcsAttestedDocumentProvider",
    "AlibabaCloudEcsAttestedDocumentProviderBuilder",
    "AwsEc2Pkcs7AttestedDocumentProvider",
]
