"""
IDaaS Python SDK - HTTP Client Interface
"""

from abc import ABC, abstractmethod

from cloud_idaas.core.http.http_request import HttpRequest
from cloud_idaas.core.http.http_response import HttpResponse


class HttpClient(ABC):
    """
    Interface for HTTP client.
    """

    @abstractmethod
    def send(self, request: HttpRequest) -> HttpResponse:
        """
        Send HTTP request.

        Args:
            request: HTTP request.

        Returns:
            HTTP response.
        """
        pass
