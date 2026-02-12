"""
IDaaS Python SDK - HTTP Response
"""

from typing import Dict, Optional


class HttpResponse:
    """
    HTTP response class.
    """

    def __init__(self, status_code: int = None, body: str = None):
        self._status_code: Optional[int] = status_code
        self._headers: Optional[Dict[str, str]] = None
        self._body: Optional[str] = body

    @property
    def status_code(self) -> Optional[int]:
        return self._status_code

    @status_code.setter
    def status_code(self, value: int):
        self._status_code = value

    @property
    def headers(self) -> Optional[Dict[str, str]]:
        return self._headers

    @headers.setter
    def headers(self, value: Dict[str, str]):
        self._headers = value

    @property
    def body(self) -> Optional[str]:
        return self._body

    @body.setter
    def body(self, value: str):
        self._body = value

    def is_success(self) -> bool:
        """
        Check if the response is successful (status code 2xx).

        Returns:
            True if successful, False otherwise.
        """
        return 200 <= self._status_code < 300

    def __repr__(self) -> str:
        """
        Return a string representation of the HTTP response.

        Returns:
            String representation of the response.
        """
        return f"HttpResponse(status_code={self._status_code}, headers={self._headers}, body={self._body!r})"

    def __eq__(self, other) -> bool:
        """
        Check if two HttpResponse objects are equal.

        Args:
            other: Another object to compare with.

        Returns:
            True if equal, False otherwise.
        """
        if not isinstance(other, HttpResponse):
            return NotImplemented
        return self._status_code == other._status_code and self._headers == other._headers and self._body == other._body

    def __hash__(self) -> int:
        """
        Return a hash value for the HttpResponse object.

        Returns:
            Hash value.
        """
        return hash((self._status_code, tuple(sorted(self._headers.items())) if self._headers else None, self._body))
