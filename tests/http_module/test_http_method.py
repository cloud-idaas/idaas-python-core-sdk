"""
Tests for HttpMethod enum
"""

import unittest

from cloud_idaas.core.http.http_method import HttpMethod


class TestHttpMethod(unittest.TestCase):
    """Test cases for HttpMethod enum"""

    def test_get_method(self):
        """Test GET method"""
        self.assertEqual(HttpMethod.GET.value, "GET")

    def test_post_method(self):
        """Test POST method"""
        self.assertEqual(HttpMethod.POST.value, "POST")

    def test_put_method(self):
        """Test PUT method"""
        self.assertEqual(HttpMethod.PUT.value, "PUT")


if __name__ == "__main__":
    unittest.main()
