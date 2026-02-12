"""
IDaaS Python SDK - Content Type
"""

from enum import Enum


class _StrEnum(Enum):
    """
    Base enum class that returns the value when converted to string.
    """

    def __str__(self) -> str:
        return self.value


class ContentType(_StrEnum):
    """
    Enum for content types.
    """

    XML = "application/xml"

    JSON = "application/json"

    RAW = "application/octet-stream"

    FORM = "application/x-www-form-urlencoded"
