"""
IDaaS Python SDK - Static Client Secret Assertion Provider

This module provides a JWT client assertion provider that uses
client secret for signing.
"""

import uuid
from typing import Callable, Optional

from cloud_idaas.core.exceptions import CredentialException
from cloud_idaas.core.provider.jwt_client_assertion_provider import JwtClientAssertionProvider


class StaticClientSecretAssertionProvider(JwtClientAssertionProvider):
    """
    JWT client assertion provider that uses client secret for signing.

    This provider creates JWT assertions signed with HMAC-SHA256 using
    a client secret.
    """

    def __init__(self, client_secret_supplier: Callable[[], str]):
        """
        Initialize the static client secret assertion provider.

        Args:
            client_secret_supplier: Function that returns the client secret.
        """
        self._client_secret_supplier = client_secret_supplier
        self._client_id: Optional[str] = None
        self._token_endpoint: Optional[str] = None
        self._scope: Optional[str] = None

    @property
    def client_id(self) -> Optional[str]:
        """Get the client ID."""
        return self._client_id

    @client_id.setter
    def client_id(self, value: str) -> None:
        """Set the client ID."""
        self._client_id = value

    @property
    def token_endpoint(self) -> Optional[str]:
        """Get the token endpoint."""
        return self._token_endpoint

    @token_endpoint.setter
    def token_endpoint(self, value: str) -> None:
        """Set the token endpoint."""
        self._token_endpoint = value

    @property
    def scope(self) -> Optional[str]:
        """Get the OAuth scope."""
        return self._scope

    @scope.setter
    def scope(self, value: str) -> None:
        """Set the OAuth scope."""
        self._scope = value

    def get_client_assertion(self) -> str:
        """
        Generate a JWT client assertion signed with the client secret.

        Returns:
            The JWT assertion string.

        Raises:
            CredentialException: If assertion generation fails or required fields are missing.
        """
        # Validate required fields
        if not self._client_id or not self._token_endpoint:
            raise CredentialException("client_id and token_endpoint are required for generating client assertion")

        try:
            from datetime import datetime, timedelta, timezone

            import jwt  # PyJWT library

            # Build JWT claims
            now = datetime.now(timezone.utc)
            claims = {
                "aud": self._token_endpoint,
                "sub": self._client_id,
                "iss": self._client_id,
                "jti": str(uuid.uuid4()),
                "iat": int(now.timestamp()),
                "exp": int((now + timedelta(minutes=10)).timestamp()),
            }

            # Sign with client secret using HMAC-SHA256
            client_secret = self._client_secret_supplier()
            return jwt.encode(claims, client_secret, algorithm="HS256")

        except ImportError:
            raise CredentialException("PyJWT library is required. Install it with: pip install pyjwt")
        except Exception as e:
            raise CredentialException(f"Failed to generate client assertion: {e}", e)
