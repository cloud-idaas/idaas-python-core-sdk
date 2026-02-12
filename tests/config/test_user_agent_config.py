"""
Tests for UserAgentConfig class
"""

import unittest

from cloud_idaas.core.config.user_agent_config import UserAgentConfig


class TestUserAgentConfig(unittest.TestCase):
    """Test cases for UserAgentConfig class"""

    def test_get_user_agent_message(self):
        """Test get_user_agent_message returns a valid string"""
        message = UserAgentConfig.get_user_agent_message()
        self.assertIsInstance(message, str)
        self.assertIn("IDaaS core", message)
        self.assertIn("Python", message)
        self.assertIn("OS", message)

    def test_get_user_agent_message_cached(self):
        """Test that user agent message is cached"""
        message1 = UserAgentConfig.get_user_agent_message()
        message2 = UserAgentConfig.get_user_agent_message()
        self.assertEqual(message1, message2)


if __name__ == "__main__":
    unittest.main()
