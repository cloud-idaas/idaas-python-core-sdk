"""
IDaaS Python SDK - Refresh Credential Provider
"""

from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class RefreshCredentialProvider(ABC):
    """
    Interface for refresh credential provider.
    """

    @abstractmethod
    def refresh_credential(self) -> "RefreshResult":
        """
        Refresh the credential.

        Returns:
            RefreshResult containing the refreshed credential.
        """
        pass


class RefreshResult:
    """
    Result of a credential refresh operation.
    """

    def __init__(self, value: T, is_refreshed: bool):
        self._value = value
        self._is_refreshed = is_refreshed

    @property
    def value(self) -> T:
        return self._value

    @property
    def is_refreshed(self) -> bool:
        return self._is_refreshed
