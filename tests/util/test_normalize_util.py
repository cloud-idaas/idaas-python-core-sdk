"""
IDaaS Python SDK - Test Normalize Utility
"""

from cloud_idaas.core.config.idaas_client_config import IDaaSClientConfig
from cloud_idaas.core.util.normalize_util import NormalizeUtil


class TestNormalizeUtil:
    """Tests for NormalizeUtil."""

    def test_normalize_endpoints_with_https(self):
        """Test that HTTPS endpoints are not changed."""
        config = IDaaSClientConfig()
        config.issuer = "https://idaas.example.com"
        config.token_endpoint = "https://idaas.example.com/oauth2/token"
        config.device_authorization_endpoint = "https://idaas.example.com/oauth2/device_authorization"
        config.developer_api_endpoint = "https://api.example.com"
        config.openapi_endpoint = "https://openapi.example.com"

        NormalizeUtil.normalize_endpoints(config)

        assert config.issuer == "https://idaas.example.com"
        assert config.token_endpoint == "https://idaas.example.com/oauth2/token"
        assert config.device_authorization_endpoint == "https://idaas.example.com/oauth2/device_authorization"
        assert config.developer_api_endpoint == "https://api.example.com"
        assert config.openapi_endpoint == "https://openapi.example.com"

    def test_normalize_endpoints_with_http(self):
        """Test that HTTP endpoints are converted to HTTPS."""
        config = IDaaSClientConfig()
        config.issuer = "http://idaas.example.com"
        config.token_endpoint = "http://idaas.example.com/oauth2/token"

        NormalizeUtil.normalize_endpoints(config)

        assert config.issuer == "https://idaas.example.com"
        assert config.token_endpoint == "https://idaas.example.com/oauth2/token"

    def test_normalize_endpoints_without_scheme(self):
        """Test that endpoints without scheme get HTTPS added."""
        config = IDaaSClientConfig()
        config.issuer = "idaas.example.com"
        config.token_endpoint = "idaas.example.com/oauth2/token"

        NormalizeUtil.normalize_endpoints(config)

        assert config.issuer == "https://idaas.example.com"
        assert config.token_endpoint == "https://idaas.example.com/oauth2/token"

    def test_normalize_endpoints_with_none(self):
        """Test that None endpoints remain None."""
        config = IDaaSClientConfig()
        config.issuer = None
        config.token_endpoint = None

        NormalizeUtil.normalize_endpoints(config)

        assert config.issuer is None
        assert config.token_endpoint is None

    def test_normalize_endpoints_with_empty_string(self):
        """Test that empty string endpoints remain empty."""
        config = IDaaSClientConfig()
        config.issuer = ""
        config.token_endpoint = ""

        NormalizeUtil.normalize_endpoints(config)

        assert config.issuer == ""
        assert config.token_endpoint == ""

    def test_normalize_endpoints_mixed(self):
        """Test mixed endpoint formats."""
        config = IDaaSClientConfig()
        config.issuer = "http://idaas.example.com"
        config.token_endpoint = "https://token.example.com"
        config.device_authorization_endpoint = "device.example.com"
        config.developer_api_endpoint = None
        config.openapi_endpoint = "http://openapi.example.com"

        NormalizeUtil.normalize_endpoints(config)

        assert config.issuer == "https://idaas.example.com"
        assert config.token_endpoint == "https://token.example.com"
        assert config.device_authorization_endpoint == "https://device.example.com"
        assert config.developer_api_endpoint is None
        assert config.openapi_endpoint == "https://openapi.example.com"

    def test_normalize_endpoints_with_port(self):
        """Test endpoints with port numbers."""
        config = IDaaSClientConfig()
        config.issuer = "http://localhost:8080"
        config.token_endpoint = "localhost:8080/token"

        NormalizeUtil.normalize_endpoints(config)

        assert config.issuer == "https://localhost:8080"
        assert config.token_endpoint == "https://localhost:8080/token"

    def test_normalize_endpoints_with_path(self):
        """Test endpoints with paths."""
        config = IDaaSClientConfig()
        config.issuer = "http://example.com/some/path"
        config.token_endpoint = "example.com/oauth2/token"

        NormalizeUtil.normalize_endpoints(config)

        assert config.issuer == "https://example.com/some/path"
        assert config.token_endpoint == "https://example.com/oauth2/token"
