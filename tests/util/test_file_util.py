"""
Tests for FileUtil class
"""

import os
import tempfile
import unittest

from cloud_idaas import FileUtil


class TestFileUtil(unittest.TestCase):
    """Test cases for FileUtil class"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.txt")

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_write_and_read_file(self):
        """Test write and read file"""
        content = "Hello, World!"
        FileUtil.write_file(self.test_file, content)
        result = FileUtil.read_file(self.test_file)
        self.assertEqual(result, content)

    def test_read_file_not_exists(self):
        """Test read file that doesn't exist"""
        with self.assertRaises(IOError):
            FileUtil.read_file("/nonexistent/file.txt")

    def test_write_file_creates_directories(self):
        """Test write file creates parent directories"""
        nested_file = os.path.join(self.temp_dir, "nested", "dir", "test.txt")
        FileUtil.write_file(nested_file, "content")
        self.assertTrue(os.path.exists(nested_file))
        self.assertEqual(FileUtil.read_file(nested_file), "content")

    def test_write_file_overwrites_existing(self):
        """Test write file overwrites existing content"""
        FileUtil.write_file(self.test_file, "original")
        FileUtil.write_file(self.test_file, "new content")
        result = FileUtil.read_file(self.test_file)
        self.assertEqual(result, "new content")


if __name__ == "__main__":
    unittest.main()
