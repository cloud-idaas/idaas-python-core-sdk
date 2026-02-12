"""
IDaaS Python SDK - Static Private Key Assertion Provider

This module provides a JWT client assertion provider that uses
private key for signing.
"""

import uuid
from typing import Optional

from cloud_idaas.core.constants import ErrorCode
from cloud_idaas.core.exceptions import CredentialException
from cloud_idaas.core.provider.jwt_client_assertion_provider import JwtClientAssertionProvider
from cloud_idaas.core.util.pki_util import PkiUtil


class StaticPrivateKeyAssertionProvider(JwtClientAssertionProvider):
    """
    JWT client assertion provider that uses private key for signing.

    This provider creates JWT assertions signed with RSA or ECDSA
    using a private key.
    """

    def __init__(self, private_key_string: str):
        """
        Initialize the static private key assertion provider.

        Args:
            private_key_string: The private key in PEM format.
        """
        self._private_key_string = private_key_string
        try:
            self._private_key = PkiUtil.parse_private_key_from_pem(private_key_string)
        except Exception as e:
            raise CredentialException(f"Failed to parse private key: {e}", e)

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
        Generate a JWT client assertion signed with the private key.

        Returns:
            The JWT assertion string.

        Raises:
            CredentialException: If assertion generation fails.
        """
        try:
            from datetime import datetime, timedelta, timezone

            import jwt  # PyJWT library
            from cryptography.hazmat.primitives.asymmetric import ec, rsa

            # Build JWT claims - use empty string for None values to allow JWT generation
            client_id = self._client_id or ""
            token_endpoint = self._token_endpoint or ""

            now = datetime.now(timezone.utc)
            claims = {
                "aud": token_endpoint,
                "sub": client_id,
                "iss": client_id,
                "jti": str(uuid.uuid4()),
                "iat": int(now.timestamp()),
                "exp": int((now + timedelta(minutes=10)).timestamp()),
            }

            # Determine algorithm based on key type
            algorithm = None
            if isinstance(self._private_key, rsa.RSAPrivateKey):
                algorithm = "RS256"
            elif isinstance(self._private_key, ec.EllipticCurvePrivateKey):
                algorithm = "ES256"
            else:
                raise CredentialException(
                    ErrorCode.NOT_SUPPORTED_WEB_KEY, f"Not supported web key: {type(self._private_key)}"
                )

            # Sign with private key
            return jwt.encode(claims, self._private_key, algorithm=algorithm)

        except ImportError:
            raise CredentialException("PyJWT library is required. Install it with: pip install pyjwt")
        except Exception as e:
            raise CredentialException(f"Failed to generate client assertion: {e}", e)
