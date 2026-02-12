"""
Tests for BrowserUtil class
"""

import unittest
from unittest.mock import patch

from cloud_idaas import BrowserUtil


class TestBrowserUtil(unittest.TestCase):
    """Test cases for BrowserUtil class"""

    @patch("cloud_idaas.core.util.browser_util.webbrowser")
    def test_open_with_string_uri(self, mock_webbrowser):
        """Test open with string URI"""
        BrowserUtil.open("https://example.com")
        mock_webbrowser.open.assert_called_once_with("https://example.com")

    @patch("cloud_idaas.core.util.browser_util.webbrowser")
    def test_open_with_object_uri(self, mock_webbrowser):
        """Test open with object that has __str__ method"""

        class MockURI:
            def __str__(self):
                return "https://example.com"

        BrowserUtil.open(MockURI())
        mock_webbrowser.open.assert_called_once_with("https://example.com")

    @patch("cloud_idaas.core.util.browser_util.webbrowser")
    @patch("cloud_idaas.core.util.browser_util.urlparse")
    def test_open_with_invalid_uri(self, mock_urlparse, mock_webbrowser):
        """Test open with invalid URI"""
        from urllib.parse import ParseResult

        mock_urlparse.return_value = ParseResult(scheme="", netloc="", path="", params="", query="", fragment="")

        with self.assertRaises(IOError):
            BrowserUtil.open("invalid-uri")

    @patch("cloud_idaas.core.util.browser_util.webbrowser")
    def test_open_with_browser_error(self, mock_webbrowser):
        """Test open when browser.open raises exception"""
        mock_webbrowser.open.side_effect = Exception("Browser error")
        with self.assertRaises(IOError):
            BrowserUtil.open("https://example.com")


if __name__ == "__main__":
    unittest.main()
