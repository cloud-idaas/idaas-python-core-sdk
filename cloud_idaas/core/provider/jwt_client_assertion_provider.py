"""
IDaaS Python SDK - JWT Client Assertion Provider
"""

from abc import ABC, abstractmethod


class JwtClientAssertionProvider(ABC):
    """
    Interface for JWT client assertion provider.
    """

    @abstractmethod
    def get_client_assertion(self) -> str:
        """
        Get the client assertion (JWT).

        Returns:
            The client assertion string.
        """
        pass
