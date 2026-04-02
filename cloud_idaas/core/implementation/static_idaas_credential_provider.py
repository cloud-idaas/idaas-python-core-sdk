"""
IDaaS Python SDK - Static IDaaS Credential Provider

This module provides a static credential provider for testing and
scenarios where credentials are already available.
"""

from typing import Optional

from cloud_idaas.core.credential import IDaaSCredential
from cloud_idaas.core.provider.idaas_credential_provider import IDaaSCredentialProvider


class StaticIDaaSCredentialProvider(IDaaSCredentialProvider):
    """
    A credential provider that returns a static credential.

    This is useful for testing scenarios or when credentials are obtained
    through external means and need to be passed to components that expect
    an IDaaSCredentialProvider.
    """

    def __init__(self, credential: Optional[IDaaSCredential] = None):
        """
        Initialize the static credential provider.

        Args:
            credential: The static credential to return.
        """
        self._credential = credential

    def get_credential(self) -> Optional[IDaaSCredential]:
        """
        Get the static credential.

        Returns:
            The static credential, or None if not set.
        """
        return self._credential

    @classmethod
    def builder(cls) -> "StaticIDaaSCredentialProviderBuilder":
        """
        Create a builder for constructing StaticIDaaSCredentialProvider instances.

        Returns:
            A new builder instance.
        """
        return StaticIDaaSCredentialProviderBuilder()


class StaticIDaaSCredentialProviderBuilder:
    """
    Builder for constructing StaticIDaaSCredentialProvider instances.

    This builder follows the Python builder pattern for fluent API design.
    """

    def __init__(self):
        """Initialize the builder."""
        self._credential: Optional[IDaaSCredential] = None

    def credential(self, credential: IDaaSCredential) -> "StaticIDaaSCredentialProviderBuilder":
        """
        Set the credential.

        Args:
            credential: The credential to use.

        Returns:
            This builder instance for method chaining.
        """
        self._credential = credential
        return self

    def build(self) -> StaticIDaaSCredentialProvider:
        """
        Build the StaticIDaaSCredentialProvider instance.

        Returns:
            A new StaticIDaaSCredentialProvider instance.
        """
        return StaticIDaaSCredentialProvider(self._credential)
