"""
IDaaS Python SDK - IDaaS Credential Provider
"""

from abc import abstractmethod
from typing import Callable, Optional

from cloud_idaas.core.credential import IDaaSCredential
from cloud_idaas.core.provider.jwt_client_assertion_provider import JwtClientAssertionProvider
from cloud_idaas.core.provider.oidc_token_provider import OidcTokenProvider
from cloud_idaas.core.provider.pkcs7_attested_document_provider import Pkcs7AttestedDocumentProvider


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

    def set_client_secret_supplier(self, supplier: "Callable[[], str]") -> None:
        """
        Set the client secret supplier.

        Args:
            supplier: A callable that returns the client secret.
        """
        raise NotImplementedError("set_client_secret_supplier not implemented")

    def set_client_assertion_provider(self, provider: "JwtClientAssertionProvider") -> None:
        """
        Set the client assertion provider.

        Args:
            provider: The JWT client assertion provider.
        """
        raise NotImplementedError("set_client_assertion_provider not implemented")

    def set_oidc_token_provider(self, provider: "OidcTokenProvider") -> None:
        """
        Set the OIDC token provider.

        Args:
            provider: The OIDC token provider.
        """
        raise NotImplementedError("set_oidc_token_provider not implemented")

    def set_attested_document_provider(self, provider: "Pkcs7AttestedDocumentProvider") -> None:
        """
        Set the attested document provider.

        Args:
            provider: The PKCS7 attested document provider.
        """
        raise NotImplementedError("set_attested_document_provider not implemented")

    def set_application_federated_credential_name(self, name: str) -> None:
        """
        Set the application federated credential name.

        Args:
            name: The application federated credential name.
        """
        raise NotImplementedError("set_application_federated_credential_name not implemented")

    def set_client_x509_certificate(self, certificate: str) -> None:
        """
        Set the client X509 certificate.

        Args:
            certificate: The client X509 certificate.
        """
        raise NotImplementedError("set_client_x509_certificate not implemented")

    def set_x509_cert_chains(self, chains: str) -> None:
        """
        Set the X509 certificate chains.

        Args:
            chains: The X509 certificate chains.
        """
        raise NotImplementedError("set_x509_cert_chains not implemented")
