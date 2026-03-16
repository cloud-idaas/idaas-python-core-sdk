"""
IDaaS Python SDK - IDaaS Credential Provider
"""

from abc import abstractmethod
from typing import Optional

from cloud_idaas.core.credential import IDaaSCredential
from cloud_idaas.core.provider.oidc_token_provider import OidcTokenProvider


class IDaaSCredentialProvider(OidcTokenProvider):
    """
    Interface for IDaaS credential provider.
    """

    @abstractmethod
    def get_credential(self) -> Optional[IDaaSCredential]:
        """
        Get the IDaaS credential.

        Returns:
            The IDaaS credential, or None if not available.
        """
        pass

    def get_bearer_token(self) -> Optional[str]:
        """
        Get the bearer token (access token).

        Returns:
            The bearer token string, or None if not available.
        """
        credential = self.get_credential()
        if credential is None:
            return None
        return credential.get_access_token()

    def get_oidc_token(self) -> Optional[str]:
        """
        Get the OIDC token.

        Returns:
            The OIDC token string (same as bearer token), or None if not available.
        """
        return self.get_bearer_token()
