"""
IDaaS Python SDK - PKCS7 Authentication Implementation Module

This module contains PKCS7 authentication implementation classes.
"""

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
    "StaticPkcs7AttestedDocumentProvider",
    "AlibabaCloudEcsAttestedDocumentProvider",
    "AlibabaCloudEcsAttestedDocumentProviderBuilder",
    "AwsEc2Pkcs7AttestedDocumentProvider",
]
