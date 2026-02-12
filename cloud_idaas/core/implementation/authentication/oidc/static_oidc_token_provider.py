"""
IDaaS Python SDK - Static OIDC Token Provider

This module provides a static OIDC token provider.
"""

from typing import Optional

from cloud_idaas.core.provider import OidcTokenProvider


class StaticOidcTokenProvider(OidcTokenProvider):
    """
    Static OIDC token provider.

    This provider returns a pre-configured OIDC token.
    """

    def __init__(self, oidc_token: Optional[str] = None):
        """
        Initialize the static OIDC token provider.

        Args:
            oidc_token: The OIDC token string.
        """
        self._oidc_token = oidc_token

    def get_oidc_token(self) -> Optional[str]:
        """
        Get the OIDC token.

        Returns:
            The OIDC token string, or None if not set.
        """
        return self._oidc_token

    def set_oidc_token(self, oidc_token: str) -> None:
        """
        Set the OIDC token.

        Args:
            oidc_token: The OIDC token string.
        """
        self._oidc_token = oidc_token
