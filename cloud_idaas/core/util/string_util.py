"""
IDaaS Python SDK - String Utility

This module provides string utility methods.
"""

import re
from typing import Optional


class StringUtil:
    """
    Utility class for string operations.
    """

    @staticmethod
    def is_blank(s: Optional[str]) -> bool:
        """
        Check if a string is blank (None, empty, or only whitespace).

        Args:
            s: String to check.

        Returns:
            True if the string is None, empty, or only whitespace, False otherwise.
        """
        return s is None or len(s.strip()) == 0

    @staticmethod
    def is_empty(s: Optional[str]) -> bool:
        """
        Check if a string is empty or None.

        Args:
            s: String to check.

        Returns:
            True if the string is None or empty, False otherwise.
        """
        return StringUtil.is_blank(s)

    @staticmethod
    def is_not_blank(s: Optional[str]) -> bool:
        """
        Check if a string is not blank.

        Args:
            s: String to check.

        Returns:
            True if the string is not None and not empty/whitespace, False otherwise.
        """
        return s is not None and len(s.strip()) > 0

    @staticmethod
    def is_not_empty(s: Optional[str]) -> bool:
        """
        Check if a string is not empty.

        Args:
            s: String to check.

        Returns:
            True if the string is not None and not empty, False otherwise.
        """
        return StringUtil.is_not_blank(s)

    @staticmethod
    def equals(str1: Optional[str], str2: Optional[str]) -> bool:
        """
        Compare two strings for equality.

        Args:
            str1: First string.
            str2: Second string.

        Returns:
            True if both strings are equal (including handling None), False otherwise.
        """
        if str1 is None:
            return str2 is None
        return str1 == str2

    @staticmethod
    def trim(s: Optional[str]) -> Optional[str]:
        """
        Trim whitespace from a string.

        Args:
            s: String to trim.

        Returns:
            Trimmed string, or None if input is None.
        """
        if s is None:
            return None
        return s.strip()

    @staticmethod
    def camel_to_snake(camel_str: Optional[str]) -> Optional[str]:
        """
        Convert camelCase string to snake_case.

        Args:
            camel_str: CamelCase string to convert (e.g., "idaasInstanceId").

        Returns:
            snake_case string (e.g., "idaas_instance_id").
        """
        if camel_str is None:
            return None

        # Insert underscore before uppercase letters that are followed by lowercase letters
        # or before uppercase letters that are preceded by lowercase letters
        # This handles cases like "idaasInstanceId" -> "idaas_instance_id"
        result = re.sub(r"([a-z])([A-Z])", r"\1_\2", camel_str)
        # Handle consecutive uppercase letters (e.g., "HTTPServer" -> "HTTP_Server")
        result = re.sub(r"([A-Z])([A-Z][a-z])", r"\1_\2", result)
        return result.lower()

    @staticmethod
    def snake_to_camel(snake_str: Optional[str], capitalize_first: bool = False) -> Optional[str]:
        """
        Convert snake_case string to camelCase.

        Args:
            snake_str: snake_case string to convert (e.g., "idaas_instance_id").
            capitalize_first: If True, produce PascalCase (e.g., "IdaasInstanceId").
                              If False, produce camelCase (e.g., "idaasInstanceId").

        Returns:
            CamelCase string.
        """
        if snake_str is None:
            return None

        components = snake_str.split("_")
        if capitalize_first:
            # PascalCase
            return "".join(x.capitalize() for x in components)
        else:
            # camelCase
            return components[0].lower() + "".join(x.capitalize() for x in components[1:])
