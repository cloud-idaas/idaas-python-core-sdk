"""
Tests for HttpClient interface
"""

import unittest

from cloud_idaas import HttpClient, HttpRequest, HttpResponse


class TestHttpClient(unittest.TestCase):
    """Test cases for HttpClient interface"""

    def test_http_client_is_abstract(self):
        """Test that HttpClient is an abstract class"""
        with self.assertRaises(TypeError):
            HttpClient()

    def test_send_is_abstract(self):
        """Test that send method is abstract"""

        class MockHttpClient(HttpClient):
            def send(self, request: HttpRequest) -> HttpResponse:
                return HttpResponse(200, "OK")

        mock_client = MockHttpClient()
        response = mock_client.send(HttpRequest())
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
