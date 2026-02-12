"""
IDaaS Python SDK - Alibaba Cloud ECS Attested Document Provider

This module provides a PKCS7 attested document provider for Alibaba Cloud ECS.
"""

import logging
import time
from datetime import datetime
from typing import Optional

from cloud_idaas.core.cache.refresh_result import RefreshResult
from cloud_idaas.core.cache.stale_value_behavior import StaleValueBehavior
from cloud_idaas.core.constants import HttpConstants
from cloud_idaas.core.exceptions import EncodingException
from cloud_idaas.core.http.default_http_client import DefaultHttpClient
from cloud_idaas.core.http.http_method import HttpMethod
from cloud_idaas.core.http.http_request import HttpRequest
from cloud_idaas.core.implementation.abstract_refreshed_credential_provider import AbstractRefreshedCredentialProvider
from cloud_idaas.core.provider.pkcs7_attested_document_provider import Pkcs7AttestedDocumentProvider
from cloud_idaas.core.util.json_util import JSONUtil
from cloud_idaas.core.util.string_util import StringUtil

logger = logging.getLogger(__name__)

# Default ECS metadata service URLs
ECS_META_SERVER_PKCS7_TOKEN_URL = "http://100.100.100.200/latest/api/token"
ECS_META_SERVER_PKCS7_URL_TEMPLATE = "http://100.100.100.200/latest/dynamic/instance-identity/pkcs7?audience=%s"

# Default HTTP client
_HTTP_CLIENT = DefaultHttpClient()


class AlibabaCloudEcsAttestedDocumentProvider(AbstractRefreshedCredentialProvider[str], Pkcs7AttestedDocumentProvider):
    """
    PKCS7 attested document provider for Alibaba Cloud ECS.

    This provider retrieves PKCS7 attested documents from the Alibaba Cloud ECS
    metadata service.
    """

    def __init__(
        self,
        idaas_instance_id: str,
        meta_server_pkcs7_url_template: Optional[str] = None,
        default_document_effective_seconds: int = 3600,
        async_credential_update_enabled: bool = False,
        stale_value_behavior: StaleValueBehavior = StaleValueBehavior.STRICT,
    ):
        """
        Initialize the Alibaba Cloud ECS attested document provider.

        Args:
            idaas_instance_id: The IDaaS instance ID.
            meta_server_pkcs7_url_template: The metadata server URL template.
            default_document_effective_seconds: Default document effective time in seconds.
            async_credential_update_enabled: Whether to enable async credential update.
            stale_value_behavior: Behavior when cached value is stale.
        """
        if StringUtil.is_empty(idaas_instance_id):
            raise ValueError("idaasInstanceId cannot be empty")

        if meta_server_pkcs7_url_template is not None and StringUtil.is_empty(meta_server_pkcs7_url_template):
            raise ValueError("metaServerUrl cannot be empty")

        if default_document_effective_seconds <= 1200 or default_document_effective_seconds > 1314000:
            raise ValueError("defaultDocumentEffectiveSeconds must be greater than 1200 and less than 1314000")

        super().__init__(async_credential_update_enabled, stale_value_behavior)

        self._meta_server_url_template = meta_server_pkcs7_url_template or ECS_META_SERVER_PKCS7_URL_TEMPLATE
        self._idaas_instance_id = idaas_instance_id
        self._default_document_effective_seconds = default_document_effective_seconds
        self._signing_time = self._get_now()

    @property
    def meta_server_url_template(self) -> str:
        """Get the metadata server URL template."""
        return self._meta_server_url_template

    @property
    def idaas_instance_id(self) -> str:
        """Get the IDaaS instance ID."""
        return self._idaas_instance_id

    @idaas_instance_id.setter
    def idaas_instance_id(self, value: str) -> None:
        """Set the IDaaS instance ID."""
        self._idaas_instance_id = value

    @property
    def signing_time(self) -> int:
        """Get the signing time."""
        return self._signing_time

    @signing_time.setter
    def signing_time(self, value: int) -> None:
        """Set the signing time."""
        self._signing_time = value

    @property
    def default_document_effective_seconds(self) -> int:
        """Get the default document effective seconds."""
        return self._default_document_effective_seconds

    @default_document_effective_seconds.setter
    def default_document_effective_seconds(self, value: int) -> None:
        """Set the default document effective seconds."""
        self._default_document_effective_seconds = value

    def get_attested_document(self) -> str:
        """
        Get the attested document.

        Returns:
            The attested document string.
        """
        return self.get_cached_result_supplier().get()

    @staticmethod
    def _get_now() -> int:
        """
        Get the current time as a Unix timestamp in seconds.

        Returns:
            The current time as a Unix timestamp.
        """
        return int(time.time())

    def _refresh_credential(self) -> RefreshResult[str]:
        """
        Refresh the attested document.

        Returns:
            RefreshResult containing the new attested document and timing information.

        Raises:
            EncodingException: If URL encoding fails.
        """
        # Build audience parameter
        audience_value = {"aud": self._idaas_instance_id, "signingTime": self._signing_time}

        self._signing_time = self._get_now()
        audience_value["signingTime"] = self._signing_time

        # URL encode the audience parameter
        try:
            from urllib.parse import quote

            audience_parameter = quote(JSONUtil.to_json_string(audience_value), safe="")
        except Exception as e:
            raise EncodingException(f"Failed to URL encode audience parameter: {e}", e)

        # Get token from metadata service
        token_headers = {
            HttpConstants.X_ALIYUN_ECS_METADATA_TOKEN_TTL_SECONDS: str(self._default_document_effective_seconds)
        }
        token_request = (
            HttpRequest.builder()
            .url(ECS_META_SERVER_PKCS7_TOKEN_URL)
            .http_method(HttpMethod.PUT)
            .headers(token_headers)
            .build()
        )

        token_response = _HTTP_CLIENT.send(token_request)
        token = token_response.body

        # Get attested document from metadata service
        doc_headers = {HttpConstants.X_ALIYUN_ECS_METADATA_TOKEN: token}
        doc_request = (
            HttpRequest.builder()
            .url(self._meta_server_url_template % audience_parameter)
            .http_method(HttpMethod.GET)
            .headers(doc_headers)
            .build()
        )

        doc_response = _HTTP_CLIENT.send(doc_request)

        # Calculate timing
        from datetime import timezone

        stale_time = datetime.fromtimestamp(
            self._signing_time + self._default_document_effective_seconds, tz=timezone.utc
        )
        prefetch_time = datetime.fromtimestamp(
            self._signing_time + self._default_document_effective_seconds // 2, tz=timezone.utc
        )

        return RefreshResult.builder(doc_response.body).stale_time(stale_time).prefetch_time(prefetch_time).build()

    @staticmethod
    def builder() -> "AlibabaCloudEcsAttestedDocumentProviderBuilder":
        """Create a new builder instance."""
        return AlibabaCloudEcsAttestedDocumentProviderBuilder()


class AlibabaCloudEcsAttestedDocumentProviderBuilder:
    """Builder class for AlibabaCloudEcsAttestedDocumentProvider."""

    def __init__(self):
        """Initialize the builder."""
        self._meta_server_pkcs7_url_template: Optional[str] = None
        self._idaas_instance_id: Optional[str] = None
        self._default_document_effective_seconds = 3600
        self._async_credential_update_enabled = False
        self._stale_value_behavior = StaleValueBehavior.STRICT

    def meta_server_pkcs7_url_template(self, value: str) -> "AlibabaCloudEcsAttestedDocumentProviderBuilder":
        """Set the metadata server PKCS7 URL template."""
        if StringUtil.is_empty(value):
            raise ValueError("metaServerUrl cannot be empty")
        self._meta_server_pkcs7_url_template = value
        return self

    def idaas_instance_id(self, value: str) -> "AlibabaCloudEcsAttestedDocumentProviderBuilder":
        """Set the IDaaS instance ID."""
        if StringUtil.is_empty(value):
            raise ValueError("idaasInstanceId cannot be empty")
        self._idaas_instance_id = value
        return self

    def default_document_effective_seconds(self, value: int) -> "AlibabaCloudEcsAttestedDocumentProviderBuilder":
        """Set the default document effective seconds."""
        if value <= 1200 or value > 1314000:
            raise ValueError("defaultDocumentEffectiveSeconds must be greater than 1200 and less than 1314000")
        self._default_document_effective_seconds = value
        return self

    def async_credential_update_enabled(self, value: bool) -> "AlibabaCloudEcsAttestedDocumentProviderBuilder":
        """Set whether async credential update is enabled."""
        self._async_credential_update_enabled = value
        return self

    def stale_value_behavior(self, value: StaleValueBehavior) -> "AlibabaCloudEcsAttestedDocumentProviderBuilder":
        """Set the stale value behavior."""
        self._stale_value_behavior = value
        return self

    def build(self) -> AlibabaCloudEcsAttestedDocumentProvider:
        """
        Build the Alibaba Cloud ECS attested document provider.

        Returns:
            The configured AlibabaCloudEcsAttestedDocumentProvider instance.
        """
        return AlibabaCloudEcsAttestedDocumentProvider(
            idaas_instance_id=self._idaas_instance_id,
            meta_server_pkcs7_url_template=self._meta_server_pkcs7_url_template,
            default_document_effective_seconds=self._default_document_effective_seconds,
            async_credential_update_enabled=self._async_credential_update_enabled,
            stale_value_behavior=self._stale_value_behavior,
        )
