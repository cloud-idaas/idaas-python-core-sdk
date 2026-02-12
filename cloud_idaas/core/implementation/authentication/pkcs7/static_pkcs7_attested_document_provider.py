"""
IDaaS Python SDK - Static PKCS7 Attested Document Provider

This module provides a static PKCS7 attested document provider.
"""

from typing import Optional

from cloud_idaas.core.provider import Pkcs7AttestedDocumentProvider


class StaticPkcs7AttestedDocumentProvider(Pkcs7AttestedDocumentProvider):
    """
    Static PKCS7 attested document provider.

    This provider returns a pre-configured PKCS7 attested document.
    """

    def __init__(self, attested_document: Optional[str] = None):
        """
        Initialize the static PKCS7 attested document provider.

        Args:
            attested_document: The attested document string.
        """
        self._attested_document = attested_document

    def get_attested_document(self) -> Optional[str]:
        """
        Get the attested document.

        Returns:
            The attested document string, or None if not set.
        """
        return self._attested_document

    def set_attested_document(self, attested_document: str) -> None:
        """
        Set the attested document.

        Args:
            attested_document: The attested document string.
        """
        self._attested_document = attested_document
