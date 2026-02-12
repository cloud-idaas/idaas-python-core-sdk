"""
Unit tests for AwsEc2Pkcs7AttestedDocumentProvider
"""

import pytest

from cloud_idaas import (
    AwsEc2Pkcs7AttestedDocumentProvider,
    CredentialException,
)


class TestAwsEc2Pkcs7AttestedDocumentProvider:
    """Test cases for AwsEc2Pkcs7AttestedDocumentProvider."""

    def test_get_attested_document_raises_not_implemented_exception(self):
        """Test that get_attested_document raises CredentialException."""
        provider = AwsEc2Pkcs7AttestedDocumentProvider()

        with pytest.raises(CredentialException, match="AWS EC2 PKCS7 attested document provider is not implemented"):
            provider.get_attested_document()
