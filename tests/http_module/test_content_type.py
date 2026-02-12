"""
Tests for ContentType enum
"""

import unittest

from cloud_idaas import ContentType


class TestContentType(unittest.TestCase):
    """Test cases for ContentType enum"""

    def test_xml_type(self):
        """Test XML content type"""
        self.assertEqual(ContentType.XML.value, "application/xml")
        self.assertEqual(str(ContentType.XML), "application/xml")

    def test_json_type(self):
        """Test JSON content type"""
        self.assertEqual(ContentType.JSON.value, "application/json")
        self.assertEqual(str(ContentType.JSON), "application/json")

    def test_raw_type(self):
        """Test RAW content type"""
        self.assertEqual(ContentType.RAW.value, "application/octet-stream")
        self.assertEqual(str(ContentType.RAW), "application/octet-stream")

    def test_form_type(self):
        """Test FORM content type"""
        self.assertEqual(ContentType.FORM.value, "application/x-www-form-urlencoded")
        self.assertEqual(str(ContentType.FORM), "application/x-www-form-urlencoded")


if __name__ == "__main__":
    unittest.main()
