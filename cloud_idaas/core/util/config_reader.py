"""
IDaaS Python SDK - Config Reader

This module provides utilities for reading configuration files.
"""

import os

from cloud_idaas.core.constants import ConfigPathConstants, ErrorCode
from cloud_idaas.core.exceptions import ConfigException


class ConfigReader:
    """
    Utility class for reading configuration files.
    """

    @staticmethod
    def _get_config_path() -> str:
        """
        Get the configuration file path.

        Priority: environment variable > default

        Returns:
            The configuration file path.
        """
        # Check environment variable
        config_path = os.environ.get(ConfigPathConstants.ENV_CONFIG_PATH_KEY)
        if config_path and config_path.strip():
            return config_path

        # Default value
        return ConfigPathConstants.DEFAULT_CONFIG_PATH

    @staticmethod
    def get_config_as_string(config_path: str = None) -> str:
        """
        Load configuration file content as string.

        Priority: function parameter > environment variable > default

        Args:
            config_path: Optional. Custom config file path.
                        If not provided, will use environment variable or default path.

        Returns:
            Configuration file content as string.

        Raises:
            ConfigException: If config file doesn't exist or read fails.
        """
        # Determine which path to use and whether it's custom
        if config_path:
            # Priority 1: Use function parameter
            path_to_use = config_path
            is_custom = True
        else:
            # Priority 2 & 3: Use environment variable or default
            path_to_use = ConfigReader._get_config_path()
            env_var_set = os.environ.get(ConfigPathConstants.ENV_CONFIG_PATH_KEY)
            is_custom = bool(env_var_set and env_var_set.strip())

        # Expand ~ to home directory for existence check
        expanded_config_path = os.path.expanduser(path_to_use)

        # Check if the config file exists
        if not os.path.exists(expanded_config_path):
            if not is_custom:
                # Using default path, return a different error message
                raise ConfigException(ErrorCode.LOAD_CONFIG_FILE_FAILED, "IDaaS config not specified")
            else:
                # Using custom path from function parameter or env var
                raise ConfigException(
                    ErrorCode.LOAD_CONFIG_FILE_FAILED,
                    f"IDaaS config file not found at path: {expanded_config_path}. "
                    f"Please ensure the config file exists or set the environment variable "
                    f"{ConfigPathConstants.ENV_CONFIG_PATH_KEY} to specify the config path.",
                )

        return ConfigReader._load_file_as_string(path_to_use)

    @staticmethod
    def _load_file_as_string(file_path: str) -> str:
        """
        Load file content as string.

        Args:
            file_path: The file path.

        Returns:
            File content as string.

        Raises:
            ConfigException: If file doesn't exist or read fails.
        """
        # Expand ~ to home directory
        file_path = os.path.expanduser(file_path)

        # Try to read from absolute path
        if os.path.isabs(file_path) and os.path.exists(file_path):
            with open(file_path, encoding="utf-8") as f:
                return f.read()

        # Try to read from relative to CWD
        cwd_path = os.path.join(os.getcwd(), file_path)
        if os.path.exists(cwd_path):
            with open(cwd_path, encoding="utf-8") as f:
                return f.read()

        raise ConfigException(ErrorCode.LOAD_CONFIG_FILE_FAILED, f"Config file not found: {file_path}")
