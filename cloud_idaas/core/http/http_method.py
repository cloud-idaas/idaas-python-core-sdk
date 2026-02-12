"""
IDaaS Python SDK - HTTP Method
"""

from enum import Enum


class _StrEnum(Enum):
    """
    Base enum class that returns the value when converted to string.
    """

    def __str__(self) -> str:
        return self.value


class HttpMethod(_StrEnum):
    """
    Enum for HTTP methods.
    """

    GET = "GET"

    POST = "POST"

    PUT = "PUT"
