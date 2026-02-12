"""
IDaaS Python SDK - Core Module

This is the core module of the IDaaS Python SDK.
"""

from cloud_idaas.core.constants import (
    AuthenticationConstants,
    AuthenticationIdentityEnum,
    ClientAssertionType,
    ClientDeployEnvironmentEnum,
    ConfigPathConstants,
    ErrorCode,
    HttpConstants,
    OAuth2Constants,
    TokenAuthnMethod,
)
from cloud_idaas.core.credential import (
    IDaaSCredential,
    IDaaSTokenResponse,
)
from cloud_idaas.core.domain import (
    DeviceCodeResponse,
    ErrResponse,
)
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
]
