"""
IDaaS Python SDK - User Agent Configuration
"""

import platform
import sys


class UserAgentConfig:
    """
    User agent configuration class.
    """

    _user_agent_message = None

    @classmethod
    def _init_user_agent(cls) -> None:
        """
        Initialize the user agent message.
        """
        from cloud_idaas import __version__

        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        os_name = platform.system()
        os_arch = platform.machine()
        cls._user_agent_message = f"IDaaS core/{__version__} Python/{python_version} OS({os_name}; {os_arch})"

    @classmethod
    def get_user_agent_message(cls) -> str:
        """
        Get the user agent message.

        Returns:
            The user agent message string.
        """
        if cls._user_agent_message is None:
            cls._init_user_agent()
        return cls._user_agent_message
