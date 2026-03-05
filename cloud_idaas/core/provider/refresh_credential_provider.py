"""
IDaaS Python SDK - Refresh Credential Provider
"""

from abc import ABC, abstractmethod
from typing import TypeVar

from cloud_idaas.core.cache.refresh_result import RefreshResult

T = TypeVar("T")


class RefreshCredentialProvider(ABC):
    """
    Interface for refresh credential provider.
    """

    @abstractmethod
    def refresh_credential(self) -> RefreshResult:
        """
        Refresh the credential.

        Returns:
            RefreshResult containing the refreshed credential.
        """
        pass
