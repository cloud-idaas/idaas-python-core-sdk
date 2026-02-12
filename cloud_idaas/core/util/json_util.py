"""
IDaaS Python SDK - JSON Utility

This module provides JSON serialization and deserialization utilities.
"""

import json
from typing import Any, Dict, List, Type, TypeVar

T = TypeVar("T")


class JSONUtil:
    """
    Utility class for JSON operations.
    """

    @staticmethod
    def to_json_string(obj: Any) -> str:
        """
        Convert an object to JSON string.

        Args:
            obj: Object to convert.

        Returns:
            JSON string representation.
        """
        return json.dumps(obj)

    @staticmethod
    def to_json_bytes(obj: Any) -> bytes:
        """
        Convert an object to JSON bytes.

        Args:
            obj: Object to convert.

        Returns:
            JSON bytes representation.
        """
        return JSONUtil.to_json_string(obj).encode("utf-8")

    @staticmethod
    def parse_object(json_string: str, clazz: Type[T]) -> T:
        """
        Parse JSON string to an object of specified class.

        Args:
            json_string: JSON string to parse.
            clazz: Target class type.

        Returns:
            Parsed object.

        Raises:
            ValueError: If JSON parsing fails.
        """
        try:
            data = json.loads(json_string)
            if clazz is dict:
                return data
            # For simple classes, try to construct from dict
            if hasattr(clazz, "from_dict"):
                return clazz.from_dict(data)
            # For simple types like dict, return as-is
            return data
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse JSON: {e}")

    @staticmethod
    def parse_object_with_type(json_string: str, target_type: Any) -> Any:
        """
        Parse JSON string to an object of specified type.

        Args:
            json_string: JSON string to parse.
            target_type: Target type hint.

        Returns:
            Parsed object.

        Raises:
            ValueError: If JSON parsing fails.
        """
        try:
            return json.loads(json_string)
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse JSON: {e}")

    @staticmethod
    def parse_array(json_string: str, element_type: Type[T]) -> List[T]:
        """
        Parse JSON string to a list of objects.

        Args:
            json_string: JSON string to parse.
            element_type: Type of list elements.

        Returns:
            List of parsed objects.

        Raises:
            ValueError: If JSON parsing fails.
        """
        try:
            data = json.loads(json_string)
            if isinstance(data, list):
                return data
            raise ValueError("JSON is not an array")
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse JSON array: {e}")

    @staticmethod
    def parse_map(json_string: str, key_type: Type, value_type: Type) -> Dict[Any, Any]:
        """
        Parse JSON string to a map.

        Args:
            json_string: JSON string to parse.
            key_type: Type of map keys.
            value_type: Type of map values.

        Returns:
            Parsed map.

        Raises:
            ValueError: If JSON parsing fails.
        """
        try:
            data = json.loads(json_string)
            if isinstance(data, dict):
                return data
            raise ValueError("JSON is not an object")
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse JSON map: {e}")
