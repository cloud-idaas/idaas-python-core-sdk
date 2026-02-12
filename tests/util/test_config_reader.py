"""
Tests for ConfigReader class
"""

import os
import tempfile
import unittest

from cloud_idaas import ConfigException
from cloud_idaas.core import ConfigPathConstants
from cloud_idaas.core.util.config_reader import ConfigReader


class TestConfigReader(unittest.TestCase):
    """Test cases for ConfigReader class"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "config.json")

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        # Clean up environment variable
        if ConfigPathConstants.ENV_CONFIG_PATH_KEY in os.environ:
            del os.environ[ConfigPathConstants.ENV_CONFIG_PATH_KEY]

    def test_get_config_as_string_with_env_var(self):
        """Test get_config_as_string with environment variable"""
        config_content = '{"key": "value"}'
        with open(self.config_file, "w") as f:
            f.write(config_content)

        os.environ[ConfigPathConstants.ENV_CONFIG_PATH_KEY] = self.config_file
        result = ConfigReader.get_config_as_string()
        self.assertEqual(result, config_content)

    def test_get_config_as_string_file_not_found(self):
        """Test get_config_as_string with non-existent file"""
        os.environ[ConfigPathConstants.ENV_CONFIG_PATH_KEY] = "/nonexistent/config.json"
        with self.assertRaises(ConfigException) as context:
            ConfigReader.get_config_as_string()
        self.assertIn("IDaaS config file not found", str(context.exception))

    def test_get_config_as_string_empty_path(self):
        """Test get_config_as_string with empty path"""
        # Backup current environment variable
        original_env_var = os.environ.get(ConfigPathConstants.ENV_CONFIG_PATH_KEY)

        # Remove environment variable
        if ConfigPathConstants.ENV_CONFIG_PATH_KEY in os.environ:
            del os.environ[ConfigPathConstants.ENV_CONFIG_PATH_KEY]

        try:
            # When env var is not set, it should use default path
            # If default file exists, it should return content without exception
            # If default file doesn't exist, it should raise exception
            try:
                result = ConfigReader.get_config_as_string()
                # If we get here, the default file exists, which is valid behavior
                self.assertIsInstance(result, str)
            except ConfigException as e:
                # If exception is raised, it should be because default file doesn't exist
                self.assertIn("IDaaS config not specified", str(e))
        finally:
            # Restore original environment variable
            if original_env_var is not None:
                os.environ[ConfigPathConstants.ENV_CONFIG_PATH_KEY] = original_env_var
            elif ConfigPathConstants.ENV_CONFIG_PATH_KEY in os.environ:
                del os.environ[ConfigPathConstants.ENV_CONFIG_PATH_KEY]

    def test_get_config_as_string_with_custom_path(self):
        """Test get_config_as_string with custom path parameter"""
        config_content = '{"key": "custom_value"}'
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Pass custom path directly to the function
        result = ConfigReader.get_config_as_string(config_path=self.config_file)
        self.assertEqual(result, config_content)

    def test_get_config_as_string_priority_parameter_over_env(self):
        """Test that function parameter has higher priority than environment variable"""
        # Create two different config files
        env_config_file = os.path.join(self.temp_dir, "env_config.json")
        param_config_file = os.path.join(self.temp_dir, "param_config.json")

        env_content = '{"source": "env"}'
        param_content = '{"source": "param"}'

        with open(env_config_file, "w") as f:
            f.write(env_content)
        with open(param_config_file, "w") as f:
            f.write(param_content)

        # Set environment variable
        os.environ[ConfigPathConstants.ENV_CONFIG_PATH_KEY] = env_config_file

        # Pass custom path parameter - should override env var
        result = ConfigReader.get_config_as_string(config_path=param_config_file)
        self.assertEqual(result, param_content)
        self.assertNotEqual(result, env_content)

    def test_get_config_as_string_with_custom_path_not_found(self):
        """Test get_config_as_string with non-existent custom path"""
        nonexistent_path = "/path/to/nonexistent/config.json"
        with self.assertRaises(ConfigException) as context:
            ConfigReader.get_config_as_string(config_path=nonexistent_path)
        self.assertIn("IDaaS config file not found", str(context.exception))
        self.assertIn(nonexistent_path, str(context.exception))


if __name__ == "__main__":
    from cloud_idaas.core import ConfigPathConstants

    unittest.main()
