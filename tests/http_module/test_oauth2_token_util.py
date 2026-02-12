"""
Tests for OAuth2TokenUtil class
"""

import unittest
from unittest.mock import patch

from cloud_idaas import OAuth2TokenUtil


class TestOAuth2TokenUtil(unittest.TestCase):
    """Test cases for OAuth2TokenUtil class"""

    def setUp(self):
        """Set up test fixtures"""
        self.client_id = "test_client"
        self.client_secret = "test_secret"
        self.token_endpoint = "https://example.com/oauth/token"
        self.scope = "openid profile"

    def test_default_grant_type(self):
        """Test default grant type"""
        self.assertEqual(OAuth2TokenUtil.DEFAULT_GRANT_TYPE, "client_credentials")

    def test_authorization_pending_constant(self):
        """Test authorization pending constant"""
        self.assertEqual(OAuth2TokenUtil.AUTHORIZATION_PENDING, "authorization_pending")

    def test_slow_down_constant(self):
        """Test slow down constant"""
        self.assertEqual(OAuth2TokenUtil.SLOW_DOWN, "slow_down")

    @patch("cloud_idaas.core.http.oauth2_token_util.HttpClientFactory")
    def test_base64_encode(self, mock_factory):
        """Test base64 encode helper method"""
        result = OAuth2TokenUtil._base64_encode("test:value")
        import base64

        expected = base64.b64encode(b"test:value").decode("utf-8")
        self.assertEqual(result, expected)

    @patch("cloud_idaas.core.http.oauth2_token_util.HttpClientFactory")
    def test_base64_encode_with_special_chars(self, mock_factory):
        """Test base64 encode with special characters"""
        result = OAuth2TokenUtil._base64_encode("client-id:secret!@#")
        import base64

        expected = base64.b64encode(b"client-id:secret!@#").decode("utf-8")
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
