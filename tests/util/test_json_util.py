"""
Tests for JSONUtil class
"""

import unittest

from cloud_idaas import JSONUtil


class TestJSONUtil(unittest.TestCase):
    """Test cases for JSONUtil class"""

    def test_to_json_string_with_dict(self):
        """Test to_json_string with dict"""
        data = {"key": "value", "number": 42}
        result = JSONUtil.to_json_string(data)
        self.assertIn('"key"', result)
        self.assertIn('"value"', result)
        self.assertIn("42", result)

    def test_to_json_bytes_with_dict(self):
        """Test to_json_bytes with dict"""
        data = {"key": "value"}
        result = JSONUtil.to_json_bytes(data)
        self.assertIsInstance(result, bytes)
        self.assertIn(b'"key"', result)
        self.assertIn(b'"value"', result)

    def test_parse_object_to_dict(self):
        """Test parse_object to dict"""
        json_str = '{"key": "value", "number": 42}'
        result = JSONUtil.parse_object(json_str, dict)
        self.assertEqual(result["key"], "value")
        self.assertEqual(result["number"], 42)

    def test_parse_object_invalid_json(self):
        """Test parse_object with invalid JSON"""
        with self.assertRaises(ValueError):
            JSONUtil.parse_object("invalid json", dict)

    def test_parse_array_to_list(self):
        """Test parse_array to list"""
        json_str = '[1, 2, 3, "four"]'
        result = JSONUtil.parse_array(json_str, str)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[3], "four")

    def test_parse_array_invalid_json(self):
        """Test parse_array with invalid JSON"""
        with self.assertRaises(ValueError):
            JSONUtil.parse_array("invalid", str)

    def test_parse_array_not_array(self):
        """Test parse_array with non-array JSON"""
        with self.assertRaises(ValueError):
            JSONUtil.parse_array('{"key": "value"}', str)

    def test_parse_map_to_dict(self):
        """Test parse_map to dict"""
        json_str = '{"key1": "value1", "key2": "value2"}'
        result = JSONUtil.parse_map(json_str, str, str)
        self.assertEqual(result["key1"], "value1")
        self.assertEqual(result["key2"], "value2")

    def test_parse_map_invalid_json(self):
        """Test parse_map with invalid JSON"""
        with self.assertRaises(ValueError):
            JSONUtil.parse_map("invalid", str, str)

    def test_parse_map_not_object(self):
        """Test parse_map with non-object JSON"""
        with self.assertRaises(ValueError):
            JSONUtil.parse_map('["item"]', str, str)


if __name__ == "__main__":
    unittest.main()
