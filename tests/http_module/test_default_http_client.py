"""
Tests for DefaultHttpClient class
"""

import unittest
from unittest.mock import MagicMock, patch

from cloud_idaas import Builder, ClientException, ContentType, ServerException
from cloud_idaas.core.http.default_http_client import DefaultHttpClient, HttpClientFactory
from cloud_idaas.core.http.http_method import HttpMethod


class TestDefaultHttpClient(unittest.TestCase):
    """Test cases for DefaultHttpClient class"""

    def setUp(self):
        """Set up test fixtures"""
        HttpClientFactory.reset()

    def test_client_initialization(self):
        """Test client initialization with default timeouts"""
        client = DefaultHttpClient()
        self.assertEqual(client._connect_timeout, 5.0)
        self.assertEqual(client._read_timeout, 10.0)

    def test_client_initialization_custom_timeouts(self):
        """Test client initialization with custom timeouts"""
        client = DefaultHttpClient(connect_timeout=3000, read_timeout=5000)
        self.assertEqual(client._connect_timeout, 3.0)
        self.assertEqual(client._read_timeout, 5.0)

    @patch("cloud_idaas.core.http.default_http_client.urllib3.PoolManager")
    def test_send_get_request(self, mock_pool_manager):
        """Test sending GET request"""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.data = b'{"result": "success"}'
        mock_pool_manager.return_value.request.return_value = mock_response

        client = DefaultHttpClient()
        request = Builder().http_method(HttpMethod.GET).url("https://example.com/api").build()

        response = client.send(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, '{"result": "success"}')

    @patch("cloud_idaas.core.http.default_http_client.urllib3.PoolManager")
    def test_send_post_request_with_json(self, mock_pool_manager):
        """Test sending POST request with JSON body"""
        mock_response = MagicMock()
        mock_response.status = 201
        mock_response.data = b'{"id": 1}'
        mock_pool_manager.return_value.request.return_value = mock_response

        client = DefaultHttpClient()
        request = (
            Builder()
            .http_method(HttpMethod.POST)
            .url("https://example.com/api")
            .body('{"name": "test"}')
            .content_type(ContentType.JSON)
            .build()
        )

        response = client.send(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.body, '{"id": 1}')

    @patch("cloud_idaas.core.http.default_http_client.urllib3.PoolManager")
    def test_send_post_request_with_form(self, mock_pool_manager):
        """Test sending POST request with form body"""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.data = b'{"result": "success"}'
        mock_pool_manager.return_value.request.return_value = mock_response

        client = DefaultHttpClient()
        form_body = {"username": ["test"], "password": ["secret"]}
        request = (
            Builder()
            .http_method(HttpMethod.POST)
            .url("https://example.com/api")
            .form_body(form_body)
            .content_type(ContentType.FORM)
            .build()
        )

        response = client.send(request)

        self.assertEqual(response.status_code, 200)

    @patch("cloud_idaas.core.http.default_http_client.urllib3.PoolManager")
    def test_4xx_error_raises_client_exception(self, mock_pool_manager):
        """Test 4xx errors raise ClientException"""
        mock_response = MagicMock()
        mock_response.status = 404
        mock_response.data = b'{"error": "not_found", "error_description": "Resource not found"}'
        mock_pool_manager.return_value.request.return_value = mock_response

        client = DefaultHttpClient()
        request = Builder().http_method(HttpMethod.GET).url("https://example.com/api").build()

        with self.assertRaises(ClientException) as context:
            client.send(request)

        self.assertEqual(context.exception.error_code, "not_found")
        self.assertEqual(context.exception.error_message, "Resource not found")

    @patch("cloud_idaas.core.http.default_http_client.urllib3.PoolManager")
    def test_5xx_error_raises_server_exception(self, mock_pool_manager):
        """Test 5xx errors raise ServerException"""
        mock_response = MagicMock()
        mock_response.status = 500
        mock_response.data = b'{"error": "internal_error", "error_description": "Server error"}'
        mock_pool_manager.return_value.request.return_value = mock_response

        client = DefaultHttpClient()
        request = Builder().http_method(HttpMethod.GET).url("https://example.com/api").build()

        with self.assertRaises(ServerException) as context:
            client.send(request)

        self.assertEqual(context.exception.error_code, "internal_error")
        self.assertEqual(context.exception.error_message, "Server error")

    @patch("cloud_idaas.core.http.default_http_client.urllib3.PoolManager")
    def test_build_headers(self, mock_pool_manager):
        """Test building request headers"""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.data = b"{}"
        mock_pool_manager.return_value.request.return_value = mock_response

        client = DefaultHttpClient()
        headers = {"Authorization": ["Bearer token"], "Accept": ["application/json"]}
        request = (
            Builder()
            .http_method(HttpMethod.GET)
            .url("https://example.com/api")
            .headers(headers)
            .content_type(ContentType.JSON)
            .build()
        )

        client.send(request)

        call_args = mock_pool_manager.return_value.request.call_args
        self.assertIn("headers", call_args.kwargs)
        self.assertEqual(call_args.kwargs["headers"]["Authorization"], "Bearer token")
        self.assertEqual(call_args.kwargs["headers"]["Accept"], "application/json")
        self.assertEqual(call_args.kwargs["headers"]["Content-Type"], "application/json")

    def test_http_client_factory_singleton(self):
        """Test HttpClientFactory returns singleton instance"""
        client1 = HttpClientFactory.get_default_http_client()
        client2 = HttpClientFactory.get_default_http_client()

        self.assertIs(client1, client2)

    def test_http_client_factory_reset(self):
        """Test HttpClientFactory reset"""
        client1 = HttpClientFactory.get_default_http_client()
        HttpClientFactory.reset()
        client2 = HttpClientFactory.get_default_http_client()

        self.assertIsNot(client1, client2)


if __name__ == "__main__":
    unittest.main()
