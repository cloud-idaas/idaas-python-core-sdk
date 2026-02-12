"""
Unit tests for AlibabaCloudEcsAttestedDocumentProvider
"""

from unittest.mock import Mock, patch

import pytest

from cloud_idaas import (
    AlibabaCloudEcsAttestedDocumentProvider,
    AlibabaCloudEcsAttestedDocumentProviderBuilder,
    StaleValueBehavior,
)


class TestAlibabaCloudEcsAttestedDocumentProvider:
    """Test cases for AlibabaCloudEcsAttestedDocumentProvider."""

    def test_initialization_with_required_params(self):
        """Test initialization with required parameters."""
        provider = AlibabaCloudEcsAttestedDocumentProvider(idaas_instance_id="test_instance_id")
        assert provider.idaas_instance_id == "test_instance_id"
        assert provider.default_document_effective_seconds == 3600
        assert provider.signing_time is not None

    def test_initialization_with_custom_url_template(self):
        """Test initialization with custom URL template."""
        provider = AlibabaCloudEcsAttestedDocumentProvider(
            idaas_instance_id="test_instance_id", meta_server_pkcs7_url_template="https://custom.com/pkcs7?aud=%s"
        )
        assert provider.meta_server_url_template == "https://custom.com/pkcs7?aud=%s"

    def test_initialization_with_custom_effective_seconds(self):
        """Test initialization with custom effective seconds."""
        provider = AlibabaCloudEcsAttestedDocumentProvider(
            idaas_instance_id="test_instance_id", default_document_effective_seconds=7200
        )
        assert provider.default_document_effective_seconds == 7200

    def test_initialization_with_empty_instance_id_raises_error(self):
        """Test that empty instance_id raises ValueError."""
        with pytest.raises(ValueError, match="idaasInstanceId cannot be empty"):
            AlibabaCloudEcsAttestedDocumentProvider(idaas_instance_id="")

    def test_initialization_with_none_instance_id_raises_error(self):
        """Test that None instance_id raises ValueError."""
        with pytest.raises(ValueError, match="idaasInstanceId cannot be empty"):
            AlibabaCloudEcsAttestedDocumentProvider(idaas_instance_id=None)

    def test_initialization_with_empty_url_template_raises_error(self):
        """Test that empty URL template raises ValueError."""
        with pytest.raises(ValueError, match="metaServerUrl cannot be empty"):
            AlibabaCloudEcsAttestedDocumentProvider(
                idaas_instance_id="test_instance", meta_server_pkcs7_url_template=""
            )

    def test_initialization_with_effective_seconds_too_small_raises_error(self):
        """Test that effective seconds less than 1200 raises ValueError."""
        with pytest.raises(ValueError, match="defaultDocumentEffectiveSeconds must be greater than 1200"):
            AlibabaCloudEcsAttestedDocumentProvider(
                idaas_instance_id="test_instance", default_document_effective_seconds=1000
            )

    def test_initialization_with_effective_seconds_too_large_raises_error(self):
        """Test that effective seconds greater than 1314000 raises ValueError."""
        with pytest.raises(ValueError, match="defaultDocumentEffectiveSeconds must be greater than 1200"):
            AlibabaCloudEcsAttestedDocumentProvider(
                idaas_instance_id="test_instance", default_document_effective_seconds=2000000
            )

    def test_initialization_with_boundary_effective_seconds(self):
        """Test initialization with boundary effective seconds values."""
        # Lower boundary
        provider1 = AlibabaCloudEcsAttestedDocumentProvider(
            idaas_instance_id="test_instance", default_document_effective_seconds=1201
        )
        assert provider1.default_document_effective_seconds == 1201

        # Upper boundary
        provider2 = AlibabaCloudEcsAttestedDocumentProvider(
            idaas_instance_id="test_instance", default_document_effective_seconds=1314000
        )
        assert provider2.default_document_effective_seconds == 1314000

    def test_meta_server_url_template_property(self):
        """Test meta_server_url_template property."""
        provider = AlibabaCloudEcsAttestedDocumentProvider(
            idaas_instance_id="test_instance", meta_server_pkcs7_url_template="https://custom.com/pkcs7?aud=%s"
        )
        assert provider.meta_server_url_template == "https://custom.com/pkcs7?aud=%s"

    def test_idaas_instance_id_property(self):
        """Test idaas_instance_id property getter and setter."""
        provider = AlibabaCloudEcsAttestedDocumentProvider(idaas_instance_id="test_instance")
        assert provider.idaas_instance_id == "test_instance"

        provider.idaas_instance_id = "new_instance_id"
        assert provider.idaas_instance_id == "new_instance_id"

    def test_signing_time_property(self):
        """Test signing_time property getter and setter."""
        provider = AlibabaCloudEcsAttestedDocumentProvider(idaas_instance_id="test_instance")
        original_signing_time = provider.signing_time
        assert original_signing_time is not None

        provider.signing_time = 1234567890
        assert provider.signing_time == 1234567890

    def test_default_document_effective_seconds_property(self):
        """Test default_document_effective_seconds property getter and setter."""
        provider = AlibabaCloudEcsAttestedDocumentProvider(idaas_instance_id="test_instance")
        assert provider.default_document_effective_seconds == 3600

        provider.default_document_effective_seconds = 7200
        assert provider.default_document_effective_seconds == 7200

    def test_get_now_returns_timestamp(self):
        """Test that _get_now returns a valid timestamp."""
        provider = AlibabaCloudEcsAttestedDocumentProvider(idaas_instance_id="test_instance")
        now = provider._get_now()
        assert isinstance(now, int)
        assert now > 0

    def test_is_async_credential_update_enabled(self):
        """Test async credential update enabled flag."""
        provider = AlibabaCloudEcsAttestedDocumentProvider(
            idaas_instance_id="test_instance", async_credential_update_enabled=True
        )
        assert provider.is_async_credential_update_enabled()

    def test_get_cached_result_supplier(self):
        """Test getting cached result supplier."""
        provider = AlibabaCloudEcsAttestedDocumentProvider(idaas_instance_id="test_instance")
        supplier = provider.get_cached_result_supplier()
        assert supplier is not None

    def test_close(self):
        """Test closing the provider."""
        provider = AlibabaCloudEcsAttestedDocumentProvider(idaas_instance_id="test_instance")
        provider.close()
        # Should not raise an exception

    def test_context_manager(self):
        """Test using provider as context manager."""
        with AlibabaCloudEcsAttestedDocumentProvider(idaas_instance_id="test_instance") as provider:
            assert provider is not None

    @patch(
        "cloud_idaas.core.implementation.authentication.pkcs7.alibaba_cloud_ecs_attested_document_provider._HTTP_CLIENT"
    )
    @patch("cloud_idaas.core.implementation.authentication.pkcs7.alibaba_cloud_ecs_attested_document_provider.JSONUtil")
    @patch("urllib.parse.quote")
    def test_refresh_credential(self, mock_quote, mock_json_util, mock_http_client):
        """Test refreshing credential."""
        # Setup mocks
        mock_quote.return_value = "encoded_audience"
        mock_json_util.to_json_string.return_value = '{"aud":"test","signingTime":123}'

        mock_token_response = Mock()
        mock_token_response.body = "test_token"

        mock_doc_response = Mock()
        mock_doc_response.body = "test_pkcs7_document"

        mock_http_client.send.side_effect = [mock_token_response, mock_doc_response]

        provider = AlibabaCloudEcsAttestedDocumentProvider(idaas_instance_id="test_instance")

        result = provider._refresh_credential()
        assert result.value == "test_pkcs7_document"

    def test_get_attested_document(self):
        """Test getting attested document."""
        provider = AlibabaCloudEcsAttestedDocumentProvider(idaas_instance_id="test_instance")

        # This will try to fetch from HTTP, which we'll mock
        with patch.object(provider, "_refresh_credential") as mock_refresh:
            mock_result = Mock()
            mock_result.value = "test_document"
            mock_refresh.return_value = mock_result

            mock_supplier = provider.get_cached_result_supplier()
            with patch.object(mock_supplier, "get", return_value="test_document"):
                document = provider.get_attested_document()
                assert document == "test_document"

    def test_builder_creates_provider(self):
        """Test builder creates provider."""
        provider = AlibabaCloudEcsAttestedDocumentProvider.builder().idaas_instance_id("test_instance").build()

        assert provider.idaas_instance_id == "test_instance"

    def test_builder_with_all_parameters(self):
        """Test builder with all parameters."""
        provider = (
            AlibabaCloudEcsAttestedDocumentProvider.builder()
            .idaas_instance_id("test_instance")
            .meta_server_pkcs7_url_template("https://custom.com/pkcs7?aud=%s")
            .default_document_effective_seconds(7200)
            .async_credential_update_enabled(True)
            .stale_value_behavior(StaleValueBehavior.ALLOW)
            .build()
        )

        assert provider.idaas_instance_id == "test_instance"
        assert provider.meta_server_url_template == "https://custom.com/pkcs7?aud=%s"
        assert provider.default_document_effective_seconds == 7200
        assert provider.is_async_credential_update_enabled()

    def test_builder_with_empty_instance_id_raises_error(self):
        """Test builder with empty instance_id raises ValueError."""
        with pytest.raises(ValueError, match="idaasInstanceId cannot be empty"):
            AlibabaCloudEcsAttestedDocumentProvider.builder().idaas_instance_id("").build()

    def test_builder_with_empty_url_template_raises_error(self):
        """Test builder with empty URL template raises ValueError."""
        with pytest.raises(ValueError, match="metaServerUrl cannot be empty"):
            (
                AlibabaCloudEcsAttestedDocumentProvider.builder()
                .idaas_instance_id("test_instance")
                .meta_server_pkcs7_url_template("")
                .build()
            )

    def test_builder_with_invalid_effective_seconds_raises_error(self):
        """Test builder with invalid effective seconds raises ValueError."""
        with pytest.raises(ValueError, match="defaultDocumentEffectiveSeconds must be greater than 1200"):
            (
                AlibabaCloudEcsAttestedDocumentProvider.builder()
                .idaas_instance_id("test_instance")
                .default_document_effective_seconds(1000)
                .build()
            )


class TestAlibabaCloudEcsAttestedDocumentProviderBuilder:
    """Test cases for AlibabaCloudEcsAttestedDocumentProviderBuilder."""

    def test_builder_method_returns_builder_instance(self):
        """Test that builder() returns a builder instance."""
        builder = AlibabaCloudEcsAttestedDocumentProvider.builder()
        assert isinstance(builder, AlibabaCloudEcsAttestedDocumentProviderBuilder)

    def test_builder_fluent_interface(self):
        """Test builder fluent interface."""
        builder = (
            AlibabaCloudEcsAttestedDocumentProvider.builder()
            .idaas_instance_id("test_instance")
            .meta_server_pkcs7_url_template("https://test.com/pkcs7?aud=%s")
            .default_document_effective_seconds(7200)
            .async_credential_update_enabled(True)
            .stale_value_behavior(StaleValueBehavior.ALLOW)
        )

        assert isinstance(builder, AlibabaCloudEcsAttestedDocumentProviderBuilder)
