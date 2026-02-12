"""
IDaaS Python SDK - PKCS7 Attested Document Provider
"""

from abc import ABC, abstractmethod


class Pkcs7AttestedDocumentProvider(ABC):
    """
    Interface for PKCS7 attested document provider.
    """

    @abstractmethod
    def get_attested_document(self) -> str:
        """
        Get the attested document.

        Returns:
            The attested document string.
        """
        pass
