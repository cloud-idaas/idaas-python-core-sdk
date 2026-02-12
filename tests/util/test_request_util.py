"""
Tests for RequestUtil class
"""

import unittest
from datetime import datetime, timezone

from cloud_idaas import CredentialException, RequestUtil


class TestRequestUtil(unittest.TestCase):
    """Test cases for RequestUtil class"""

    def test_get_iso8601_time(self):
        """Test get_iso8601_time"""
        dt = datetime(2023, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        result = RequestUtil.get_iso8601_time(dt)
        self.assertEqual(result, "2023-01-01T12:30:45Z")

    def test_get_utc_date(self):
        """Test get_utc_date"""
        date_str = "2023-01-01T12:30:45Z"
        result = RequestUtil.get_utc_date(date_str)
        self.assertEqual(result.year, 2023)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 1)
        self.assertEqual(result.hour, 12)
        self.assertEqual(result.minute, 30)
        self.assertEqual(result.second, 45)

    def test_get_utc_date_invalid_format(self):
        """Test get_utc_date with invalid format"""
        with self.assertRaises(CredentialException):
            RequestUtil.get_utc_date("invalid-date")

    def test_get_unique_nonce(self):
        """Test get_unique_nonce"""
        nonce1 = RequestUtil.get_unique_nonce()
        nonce2 = RequestUtil.get_unique_nonce()
        # Verify nonces are unique (different)
        self.assertNotEqual(nonce1, nonce2)
        # Verify format (should be 32 char hex string from MD5)
        self.assertEqual(len(nonce1), 32)

    def test_compose_url_with_path(self):
        """Test compose_url with path"""
        queries = {"key1": "value1", "key2": "value2"}
        result = RequestUtil.compose_url("example.com", "/api", queries, "https")
        self.assertIn("https://example.com/api", result)
        self.assertIn("key1=value1", result)
        self.assertIn("key2=value2", result)

    def test_compose_url_without_path(self):
        """Test compose_url without path"""
        queries = {"key": "value"}
        result = RequestUtil.compose_url("example.com", None, queries, "http")
        self.assertIn("http://example.com?", result)
        self.assertIn("key=value", result)

    def test_compose_url_with_special_chars(self):
        """Test compose_url with special characters"""
        queries = {"key": "value with spaces"}
        result = RequestUtil.compose_url("example.com", None, queries, "https")
        self.assertIn("value%20with%20spaces", result)

    def test_compose_url_with_none_value(self):
        """Test compose_url with None value in queries"""
        queries = {"key1": "value1", "key2": None}
        result = RequestUtil.compose_url("example.com", None, queries, "https")
        self.assertIn("key1=value1", result)
        self.assertNotIn("key2", result)


if __name__ == "__main__":
    unittest.main()
