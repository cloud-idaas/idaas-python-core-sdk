"""
Tests for StringUtil class
"""

import unittest

from cloud_idaas import StringUtil


class TestStringUtil(unittest.TestCase):
    """Test cases for StringUtil class"""

    def test_is_empty_with_none(self):
        """Test is_empty with None"""
        self.assertTrue(StringUtil.is_empty(None))

    def test_is_empty_with_empty_string(self):
        """Test is_empty with empty string"""
        self.assertTrue(StringUtil.is_empty(""))

    def test_is_empty_with_whitespace(self):
        """Test is_empty with whitespace only"""
        self.assertTrue(StringUtil.is_empty("   "))

    def test_is_empty_with_valid_string(self):
        """Test is_empty with valid string"""
        self.assertFalse(StringUtil.is_empty("test"))

    def test_is_not_empty_with_none(self):
        """Test is_not_empty with None"""
        self.assertFalse(StringUtil.is_not_empty(None))

    def test_is_not_empty_with_empty_string(self):
        """Test is_not_empty with empty string"""
        self.assertFalse(StringUtil.is_not_empty(""))

    def test_is_not_empty_with_valid_string(self):
        """Test is_not_empty with valid string"""
        self.assertTrue(StringUtil.is_not_empty("test"))

    def test_equals_with_none_values(self):
        """Test equals with both None values"""
        self.assertTrue(StringUtil.equals(None, None))

    def test_equals_with_one_none(self):
        """Test equals with one None value"""
        self.assertFalse(StringUtil.equals("test", None))
        self.assertFalse(StringUtil.equals(None, "test"))

    def test_equals_with_same_strings(self):
        """Test equals with same strings"""
        self.assertTrue(StringUtil.equals("test", "test"))

    def test_equals_with_different_strings(self):
        """Test equals with different strings"""
        self.assertFalse(StringUtil.equals("test", "other"))

    def test_trim_with_none(self):
        """Test trim with None"""
        self.assertIsNone(StringUtil.trim(None))

    def test_trim_with_whitespace(self):
        """Test trim with whitespace"""
        self.assertEqual(StringUtil.trim("  test  "), "test")

    def test_trim_with_no_whitespace(self):
        """Test trim with no whitespace"""
        self.assertEqual(StringUtil.trim("test"), "test")


if __name__ == "__main__":
    unittest.main()
