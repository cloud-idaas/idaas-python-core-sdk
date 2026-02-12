"""
IDaaS Python SDK - AWS EC2 PKCS7 Attested Document Provider

This module provides a PKCS7 attested document provider for AWS EC2.
"""

from cloud_idaas.core.exceptions import CredentialException
from cloud_idaas.core.provider.pkcs7_attested_document_provider import Pkcs7AttestedDocumentProvider


class AwsEc2Pkcs7AttestedDocumentProvider(Pkcs7AttestedDocumentProvider):
    """
    PKCS7 attested document provider for AWS EC2.

    Note: This provider is not yet implemented.
    """

    def get_attested_document(self) -> str:
        """
        Get the attested document.

        Returns:
            The attested document string.

        Raises:
            CredentialException: Always raised as this provider is not implemented.
        """
        raise CredentialException("AWS EC2 PKCS7 attested document provider is not implemented")
