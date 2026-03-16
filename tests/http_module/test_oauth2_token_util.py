"""
Tests for OAuth2TokenUtil class
"""

import json
import unittest
from unittest.mock import Mock, patch

from cloud_idaas.core import OAuth2TokenUtil
from cloud_idaas.core.credential import IDaaSTokenResponse


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


class TestOAuth2TokenUtilTokenExchange(unittest.TestCase):
    """Test cases for OAuth2TokenUtil token_exchange methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.client_id = "test_client"
        self.client_secret = "test_secret"
        self.token_endpoint = "https://example.com/oauth/token"
        self.subject_token = "subject_token_value"
        self.subject_token_type = "urn:ietf:params:oauth:token-type:access_token"
        self.scope = "api://test|read"
        self.requested_token_type = "urn:ietf:params:oauth:token-type:access_token"

    def _create_token_response(self):
        """Create a mock IDaaSTokenResponse."""
        response = IDaaSTokenResponse()
        response.access_token = "exchanged_access_token"
        response.token_type = "Bearer"
        response.expires_in = 3600
        response.issued_token_type = "urn:ietf:params:oauth:token-type:access_token"
        return response

    @patch("cloud_idaas.core.http.oauth2_token_util.OAuth2TokenUtil._post_token_endpoint")
    def test_token_exchange_with_client_secret_basic(self, mock_post):
        """Test token_exchange_with_client_secret_basic."""
        mock_post.return_value = self._create_token_response()

        # client_secret_basic uses its own HTTP client, so we need to mock it
        with patch("cloud_idaas.core.http.oauth2_token_util.HttpClientFactory") as mock_factory:
            mock_http_client = Mock()
            mock_response = Mock()
            mock_response.body = json.dumps(
                {
                    "access_token": "exchanged_access_token",
                    "token_type": "Bearer",
                    "expires_in": 3600,
                    "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
                }
            )
            mock_http_client.send.return_value = mock_response
            mock_factory.get_default_http_client.return_value = mock_http_client

            result = OAuth2TokenUtil.token_exchange_with_client_secret_basic(
                client_id=self.client_id,
                client_secret=self.client_secret,
                token_endpoint=self.token_endpoint,
                subject_token=self.subject_token,
                subject_token_type=self.subject_token_type,
                scope=self.scope,
                requested_token_type=self.requested_token_type,
            )

            self.assertIsInstance(result, IDaaSTokenResponse)
            self.assertEqual(result.access_token, "exchanged_access_token")

    @patch("cloud_idaas.core.http.oauth2_token_util.OAuth2TokenUtil._post_token_endpoint")
    def test_token_exchange_with_client_secret_post(self, mock_post):
        """Test token_exchange_with_client_secret_post."""
        mock_post.return_value = self._create_token_response()

        result = OAuth2TokenUtil.token_exchange_with_client_secret_post(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_endpoint=self.token_endpoint,
            subject_token=self.subject_token,
            subject_token_type=self.subject_token_type,
            scope=self.scope,
            requested_token_type=self.requested_token_type,
        )

        self.assertIsInstance(result, IDaaSTokenResponse)
        self.assertEqual(result.access_token, "exchanged_access_token")
        mock_post.assert_called_once()

    @patch("cloud_idaas.core.http.oauth2_token_util.OAuth2TokenUtil._post_token_endpoint")
    def test_token_exchange_with_client_assertion(self, mock_post):
        """Test token_exchange_with_client_assertion."""
        mock_post.return_value = self._create_token_response()

        result = OAuth2TokenUtil.token_exchange_with_client_assertion(
            client_id=self.client_id,
            client_assertion="mock_assertion",
            token_endpoint=self.token_endpoint,
            subject_token=self.subject_token,
            subject_token_type=self.subject_token_type,
            scope=self.scope,
            requested_token_type=self.requested_token_type,
        )

        self.assertIsInstance(result, IDaaSTokenResponse)
        self.assertEqual(result.access_token, "exchanged_access_token")
        mock_post.assert_called_once()

    @patch("cloud_idaas.core.http.oauth2_token_util.OAuth2TokenUtil._post_token_endpoint")
    def test_token_exchange_with_pkcs7(self, mock_post):
        """Test token_exchange_with_pkcs7."""
        mock_post.return_value = self._create_token_response()

        result = OAuth2TokenUtil.token_exchange_with_pkcs7(
            client_id=self.client_id,
            application_federated_credential_name="app_fed_cred",
            pkcs7_attested_document="attested_doc",
            token_endpoint=self.token_endpoint,
            subject_token=self.subject_token,
            subject_token_type=self.subject_token_type,
            scope=self.scope,
            requested_token_type=self.requested_token_type,
        )

        self.assertIsInstance(result, IDaaSTokenResponse)
        self.assertEqual(result.access_token, "exchanged_access_token")
        mock_post.assert_called_once()

    @patch("cloud_idaas.core.http.oauth2_token_util.OAuth2TokenUtil._post_token_endpoint")
    def test_token_exchange_with_oidc(self, mock_post):
        """Test token_exchange_with_oidc."""
        mock_post.return_value = self._create_token_response()

        result = OAuth2TokenUtil.token_exchange_with_oidc(
            client_id=self.client_id,
            application_federated_credential_name="app_fed_cred",
            oidc_token="oidc_token_value",
            token_endpoint=self.token_endpoint,
            subject_token=self.subject_token,
            subject_token_type=self.subject_token_type,
            scope=self.scope,
            requested_token_type=self.requested_token_type,
        )

        self.assertIsInstance(result, IDaaSTokenResponse)
        self.assertEqual(result.access_token, "exchanged_access_token")
        mock_post.assert_called_once()

    @patch("cloud_idaas.core.http.oauth2_token_util.OAuth2TokenUtil._post_token_endpoint")
    def test_token_exchange_with_pca(self, mock_post):
        """Test token_exchange_with_pca."""
        mock_post.return_value = self._create_token_response()

        result = OAuth2TokenUtil.token_exchange_with_pca(
            client_id=self.client_id,
            application_federated_credential_name="app_fed_cred",
            client_x509_certificate="x509_cert",
            x509_cert_chains="x509_chains",
            client_assertion="mock_assertion",
            token_endpoint=self.token_endpoint,
            subject_token=self.subject_token,
            subject_token_type=self.subject_token_type,
            scope=self.scope,
            requested_token_type=self.requested_token_type,
        )

        self.assertIsInstance(result, IDaaSTokenResponse)
        self.assertEqual(result.access_token, "exchanged_access_token")
        mock_post.assert_called_once()

    @patch("cloud_idaas.core.http.oauth2_token_util.OAuth2TokenUtil._post_token_endpoint")
    def test_token_exchange_with_actor_token(self, mock_post):
        """Test token_exchange with actor_token for delegation."""
        mock_post.return_value = self._create_token_response()

        # client_secret_basic uses its own HTTP client, so we need to mock it
        with patch("cloud_idaas.core.http.oauth2_token_util.HttpClientFactory") as mock_factory:
            mock_http_client = Mock()
            mock_response = Mock()
            mock_response.body = json.dumps(
                {
                    "access_token": "exchanged_access_token",
                    "token_type": "Bearer",
                    "expires_in": 3600,
                    "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
                }
            )
            mock_http_client.send.return_value = mock_response
            mock_factory.get_default_http_client.return_value = mock_http_client

            result = OAuth2TokenUtil.token_exchange_with_client_secret_basic(
                client_id=self.client_id,
                client_secret=self.client_secret,
                token_endpoint=self.token_endpoint,
                subject_token=self.subject_token,
                subject_token_type=self.subject_token_type,
                scope=self.scope,
                requested_token_type=self.requested_token_type,
                actor_token="actor_token_value",
                actor_token_type="urn:ietf:params:oauth:token-type:access_token",
            )

            self.assertIsInstance(result, IDaaSTokenResponse)


if __name__ == "__main__":
    unittest.main()
