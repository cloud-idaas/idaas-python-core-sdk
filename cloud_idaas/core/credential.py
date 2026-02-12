"""
IDaaS Python SDK - Credential

This module contains credential-related classes and interfaces.
"""

import time
from abc import ABC, abstractmethod
from typing import Optional


class IDaaSCredential(ABC):
    """
    Interface for IDaaS credentials.
    """

    @abstractmethod
    def get_access_token(self) -> str:
        """
        Get the access token.

        Returns:
            The access token string.
        """
        pass

    @abstractmethod
    def get_id_token(self) -> str:
        """
        Get the ID token.
        When identity type is client, id token is empty.

        Returns:
            The ID token string.
        """
        pass

    @abstractmethod
    def get_refresh_token(self) -> str:
        """
        Get the refresh token.
        When identity type is client, refresh token is empty.

        Returns:
            The refresh token string.
        """
        pass

    @abstractmethod
    def get_token_type(self) -> str:
        """
        Get the token type.

        Returns:
            The token type string (e.g., "Bearer").
        """
        pass


class IDaaSTokenResponse(IDaaSCredential):
    """
    Token response from IDaaS authentication.
    """

    def __init__(self):
        self.access_token: Optional[str] = None
        self.id_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_type: Optional[str] = None
        self.expires_in: int = 0
        self.expires_at: int = 0

    def __getattr__(self, name: str):
        """
        Support backward compatibility with private attribute access.
        Maps _access_token -> access_token, etc.
        """
        public_name = name.lstrip("_")
        if public_name in ("access_token", "id_token", "refresh_token", "token_type", "expires_in", "expires_at"):
            return object.__getattribute__(self, public_name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value):
        """
        Support backward compatibility with private attribute access.
        Maps _access_token -> access_token, etc.
        """
        public_name = name.lstrip("_")
        if public_name in ("access_token", "id_token", "refresh_token", "token_type", "expires_in", "expires_at"):
            object.__setattr__(self, public_name, value)
        else:
            object.__setattr__(self, name, value)

    def get_access_token(self) -> str:
        """Get the access token."""
        return self.access_token

    def get_id_token(self) -> str:
        """Get the ID token."""
        return self.id_token

    def get_refresh_token(self) -> str:
        """Get the refresh token."""
        return self.refresh_token

    def get_token_type(self) -> str:
        """Get the token type."""
        return self.token_type

    def will_soon_expire(self) -> bool:
        """
        Check if the token will soon expire.

        Returns:
            True if the token will soon expire, False otherwise.
        """
        now = int(time.time())
        expire_fact = 0.15
        return self.expires_in * expire_fact > (self.expires_at - now)

    def to_dict(self) -> dict:
        """
        Convert the token response to a dictionary.

        Returns:
            A dictionary representation of the token response.
        """
        return {
            "access_token": self.access_token,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "expires_at": self.expires_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "IDaaSTokenResponse":
        """
        Create a token response from a dictionary.

        Args:
            data: The dictionary containing token data.

        Returns:
            A new IDaaSTokenResponse instance.
        """
        token = cls()
        token.access_token = data.get("access_token")
        token.id_token = data.get("id_token")
        token.refresh_token = data.get("refresh_token")
        token.token_type = data.get("token_type")
        token.expires_in = data.get("expires_in", 0)
        token.expires_at = data.get("expires_at", 0)
        return token

    def __repr__(self) -> str:
        """
        Return a string representation of the token response.

        Returns:
            String representation of the token response.
        """
        return (
            f"IDaaSTokenResponse(access_token={self.access_token!r}, "
            f"id_token={self.id_token!r}, refresh_token={self.refresh_token!r}, "
            f"token_type={self.token_type!r}, expires_in={self.expires_in}, "
            f"expires_at={self.expires_at})"
        )

    def __eq__(self, other) -> bool:
        """
        Check if two IDaaSTokenResponse objects are equal.

        Args:
            other: Another object to compare with.

        Returns:
            True if equal, False otherwise.
        """
        if not isinstance(other, IDaaSTokenResponse):
            return NotImplemented
        return (
            self.access_token == other.access_token
            and self.id_token == other.id_token
            and self.refresh_token == other.refresh_token
            and self.token_type == other.token_type
            and self.expires_in == other.expires_in
            and self.expires_at == other.expires_at
        )

    def __hash__(self) -> int:
        """
        Return a hash value for the IDaaSTokenResponse object.

        Returns:
            Hash value.
        """
        return hash(
            (self.access_token, self.id_token, self.refresh_token, self.token_type, self.expires_in, self.expires_at)
        )
