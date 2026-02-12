"""
IDaaS Python SDK - Provider Module

This module contains provider interfaces for credentials and tokens.
"""

from cloud_idaas.core.provider.idaas_credential_provider import IDaaSCredentialProvider
from cloud_idaas.core.provider.jwt_client_assertion_provider import JwtClientAssertionProvider
from cloud_idaas.core.provider.oidc_token_provider import OidcTokenProvider
from cloud_idaas.core.provider.pkcs7_attested_document_provider import Pkcs7AttestedDocumentProvider
from cloud_idaas.core.provider.refresh_credential_provider import RefreshCredentialProvider, RefreshResult

__all__ = [
    "IDaaSCredentialProvider",
    "JwtClientAssertionProvider",
    "OidcTokenProvider",
    "Pkcs7AttestedDocumentProvider",
    "RefreshCredentialProvider",
    "RefreshResult",
]
