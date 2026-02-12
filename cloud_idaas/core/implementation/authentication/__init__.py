"""
IDaaS Python SDK - Authentication Implementation Module

This module contains authentication implementation classes.
"""

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

__all__ = [
    "StaticClientSecretAssertionProvider",
    "StaticPrivateKeyAssertionProvider",
    "StaticPkcs7AttestedDocumentProvider",
    "AlibabaCloudEcsAttestedDocumentProvider",
    "AlibabaCloudEcsAttestedDocumentProviderBuilder",
    "AwsEc2Pkcs7AttestedDocumentProvider",
    "StaticOidcTokenProvider",
    "FileOidcTokenProvider",
]
