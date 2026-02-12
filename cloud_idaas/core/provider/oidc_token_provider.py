"""
IDaaS Python SDK - OIDC Token Provider
"""

from abc import ABC, abstractmethod


class OidcTokenProvider(ABC):
    """
    Interface for OIDC token provider.
    """

    @abstractmethod
    def get_oidc_token(self) -> str:
        """
        Get the OIDC token.

        Returns:
            The OIDC token string.
        """
        pass
