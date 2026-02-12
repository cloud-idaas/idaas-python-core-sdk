"""
IDaaS Python SDK - HTTP Request
"""

from typing import Dict, List, Optional

from cloud_idaas.core.http.content_type import ContentType
from cloud_idaas.core.http.http_method import HttpMethod


class HttpRequest:
    """
    HTTP request class.
    """

    def __init__(self):
        self._method: Optional[HttpMethod] = None
        self._url: Optional[str] = None
        self._headers: Optional[Dict[str, List[str]]] = None
        self._body: Optional[str] = None
        self._form_body: Optional[Dict[str, List[str]]] = None
        self._content_type: Optional[ContentType] = None

    @property
    def method(self) -> Optional[HttpMethod]:
        return self._method

    @method.setter
    def method(self, value: HttpMethod):
        self._method = value

    @property
    def url(self) -> Optional[str]:
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = value

    @property
    def headers(self) -> Optional[Dict[str, List[str]]]:
        return self._headers

    @headers.setter
    def headers(self, value: Dict[str, List[str]]):
        self._headers = value

    @property
    def body(self) -> Optional[str]:
        return self._body

    @body.setter
    def body(self, value: str):
        self._body = value

    @property
    def form_body(self) -> Optional[Dict[str, List[str]]]:
        return self._form_body

    @form_body.setter
    def form_body(self, value: Dict[str, List[str]]):
        self._form_body = value

    @property
    def content_type(self) -> Optional[ContentType]:
        return self._content_type

    @content_type.setter
    def content_type(self, value: ContentType):
        self._content_type = value

    def __repr__(self) -> str:
        """
        Return a string representation of the HTTP request.

        Returns:
            String representation of the request.
        """
        return (
            f"HttpRequest(method={self._method}, url={self._url!r}, "
            f"headers={self._headers}, body={self._body!r}, "
            f"form_body={self._form_body}, content_type={self._content_type})"
        )

    def __eq__(self, other) -> bool:
        """
        Check if two HttpRequest objects are equal.

        Args:
            other: Another object to compare with.

        Returns:
            True if equal, False otherwise.
        """
        if not isinstance(other, HttpRequest):
            return NotImplemented
        return (
            self._method == other._method
            and self._url == other._url
            and self._headers == other._headers
            and self._body == other._body
            and self._form_body == other._form_body
            and self._content_type == other._content_type
        )

    def __hash__(self) -> int:
        """
        Return a hash value for the HttpRequest object.

        Returns:
            Hash value.
        """
        # Convert headers to a hashable format
        hashable_headers = None
        if self._headers:
            hashable_headers = tuple(sorted((k, tuple(sorted(v))) for k, v in self._headers.items()))

        # Convert form_body to a hashable format
        hashable_form_body = None
        if self._form_body:
            hashable_form_body = tuple(sorted((k, tuple(sorted(v))) for k, v in self._form_body.items()))

        return hash((self._method, self._url, hashable_headers, self._body, hashable_form_body, self._content_type))

    @staticmethod
    def builder() -> "Builder":
        """
        Create a new builder instance.

        Returns:
            A new Builder instance.
        """
        return Builder()


class Builder:
    """
    Builder class for constructing HttpRequest objects.
    """

    def __init__(self):
        self._method: Optional[HttpMethod] = None
        self._url: Optional[str] = None
        self._headers: Optional[Dict[str, List[str]]] = None
        self._body: Optional[str] = None
        self._form_body: Optional[Dict[str, List[str]]] = None
        self._content_type: Optional[ContentType] = None

    def http_method(self, method: HttpMethod) -> "Builder":
        """
        Set the HTTP method.

        Args:
            method: The HTTP method.

        Returns:
            The builder instance.
        """
        self._method = method
        return self

    def url(self, url: str) -> "Builder":
        """
        Set the URL.

        Args:
            url: The URL.

        Returns:
            The builder instance.
        """
        self._url = url
        return self

    def headers(self, headers: Dict[str, List[str]]) -> "Builder":
        """
        Set the headers.

        Args:
            headers: The headers.

        Returns:
            The builder instance.
        """
        self._headers = headers
        return self

    def body(self, body: str) -> "Builder":
        """
        Set the body.

        Args:
            body: The body.

        Returns:
            The builder instance.
        """
        self._body = body
        return self

    def form_body(self, form_body: Dict[str, List[str]]) -> "Builder":
        """
        Set the form body.

        Args:
            form_body: The form body.

        Returns:
            The builder instance.
        """
        self._form_body = form_body
        return self

    def content_type(self, content_type: ContentType) -> "Builder":
        """
        Set the content type.

        Args:
            content_type: The content type.

        Returns:
            The builder instance.
        """
        self._content_type = content_type
        return self

    def __repr__(self) -> str:
        """
        Return a string representation of the builder.

        Returns:
            String representation of the builder.
        """
        return (
            f"Builder(method={self._method}, url={self._url!r}, "
            f"headers={self._headers}, body={self._body!r}, "
            f"form_body={self._form_body}, content_type={self._content_type})"
        )

    def __eq__(self, other) -> bool:
        """
        Check if two Builder objects are equal.

        Args:
            other: Another object to compare with.

        Returns:
            True if equal, False otherwise.
        """
        if not isinstance(other, Builder):
            return NotImplemented
        return (
            self._method == other._method
            and self._url == other._url
            and self._headers == other._headers
            and self._body == other._body
            and self._form_body == other._form_body
            and self._content_type == other._content_type
        )

    def __hash__(self) -> int:
        """
        Return a hash value for the Builder object.

        Returns:
            Hash value.
        """
        # Convert headers to a hashable format
        hashable_headers = None
        if self._headers:
            hashable_headers = tuple(sorted((k, tuple(sorted(v))) for k, v in self._headers.items()))

        # Convert form_body to a hashable format
        hashable_form_body = None
        if self._form_body:
            hashable_form_body = tuple(sorted((k, tuple(sorted(v))) for k, v in self._form_body.items()))

        return hash((self._method, self._url, hashable_headers, self._body, hashable_form_body, self._content_type))

    def build(self) -> HttpRequest:
        """
        Build the HttpRequest.

        Returns:
            The HttpRequest instance.
        """
        request = HttpRequest()
        request._method = self._method
        request._url = self._url
        request._headers = self._headers
        request._body = self._body
        request._form_body = self._form_body
        request._content_type = self._content_type
        return request
