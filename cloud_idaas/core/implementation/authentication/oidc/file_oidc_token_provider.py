"""
IDaaS Python SDK - File OIDC Token Provider

This module provides an OIDC token provider that reads tokens from a file.
"""

import logging
from datetime import datetime, timezone
from typing import Optional

from cloud_idaas.core.exceptions import CredentialException
from cloud_idaas.core.provider.oidc_token_provider import OidcTokenProvider
from cloud_idaas.core.util.file_util import FileUtil

logger = logging.getLogger(__name__)


class FileOidcTokenProvider(OidcTokenProvider):
    """
    OIDC token provider that reads tokens from a file.

    This provider reads an OIDC token from a file and caches it.
    The token is refreshed when it's about to expire (within 10 minutes).
    """

    def __init__(self, oidc_token_file_path: str):
        """
        Initialize the file OIDC token provider.

        Args:
            oidc_token_file_path: Path to the OIDC token file.
        """
        self._oidc_token_file_path = oidc_token_file_path
        self._expires_time: Optional[int] = None
        self._oidc_token: Optional[str] = None

    def get_oidc_token_file_path(self) -> str:
        """Get the OIDC token file path."""
        return self._oidc_token_file_path

    def get_oidc_token(self) -> str:
        """
        Get the OIDC token.

        Returns:
            The OIDC token string.

        Raises:
            CredentialException: If token cannot be read or parsed.
        """
        if self._oidc_token is not None and not self._will_soon_expire():
            return self._oidc_token
        else:
            try:
                self._oidc_token = FileUtil.read_file(self._oidc_token_file_path)
                self._expires_time = self._parse_expiration_time(self._oidc_token)
            except Exception as e:
                raise CredentialException(f"Failed to read or parse OIDC token: {e}", e)
        return self._oidc_token

    def _parse_expiration_time(self, token: str) -> Optional[int]:
        """
        Parse the expiration time from the OIDC token.

        Args:
            token: The OIDC token string.

        Returns:
            The expiration time as a Unix timestamp, or None if not found.
        """
        try:
            import jwt

            # Decode without verification to get the claims
            claims = jwt.decode(token, options={"verify_signature": False})
            return claims.get("exp")
        except Exception as e:
            logger.warning(f"Failed to parse expiration time from token: {e}")
            return None

    def _will_soon_expire(self) -> bool:
        """
        Check if the cached token will expire soon.

        Returns:
            True if the token will expire within 10 minutes, False otherwise.
        """
        if self._expires_time is None:
            return True

        now = int(datetime.now(timezone.utc).timestamp())
        seconds_until_expiry = self._expires_time - now
        return seconds_until_expiry < 600  # 10 minutes in seconds
