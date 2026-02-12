"""
IDaaS Python SDK - Default HTTP Client Implementation
"""

import socket
from typing import Dict, Optional
from urllib.error import URLError
from urllib.parse import urlencode

import urllib3

from cloud_idaas.core.constants import ErrorCode, HttpConstants
from cloud_idaas.core.domain import ErrResponse
from cloud_idaas.core.exceptions import ClientException, HttpException, ServerException
from cloud_idaas.core.http.content_type import ContentType
from cloud_idaas.core.http.http_client import HttpClient
from cloud_idaas.core.http.http_request import HttpRequest
from cloud_idaas.core.http.http_response import HttpResponse
from cloud_idaas.core.util.json_util import JSONUtil


class DefaultHttpClient(HttpClient):
    """
    Default HTTP client implementation using urllib3.
    """

    def __init__(self, connect_timeout: int = 5000, read_timeout: int = 10000):
        """
        Initialize the HTTP client.

        Args:
            connect_timeout: Connect timeout in milliseconds.
            read_timeout: Read timeout in milliseconds.
        """
        self._connect_timeout = connect_timeout / 1000.0
        self._read_timeout = read_timeout / 1000.0
        self._http = urllib3.PoolManager(
            timeout=urllib3.Timeout(connect=self._connect_timeout, read=self._read_timeout),
            retries=False,
            cert_reqs="CERT_REQUIRED",
        )

    def send(self, request: HttpRequest) -> HttpResponse:
        """
        Send HTTP request.

        Args:
            request: HTTP request.

        Returns:
            HTTP response.
        """
        headers = self._build_headers(request)
        body = self._build_body(request)

        try:
            method = request.method.value if request.method else "GET"
            response = self._http.request(method=method, url=request.url, headers=headers, body=body, redirect=True)

            return self._handle_response(response)

        except urllib3.exceptions.TimeoutError as e:
            if "connect" in str(e).lower():
                raise ClientException(ErrorCode.CONNECT_TIME_OUT.value, "Connect Timeout: " + str(e))
            else:
                raise ServerException(ErrorCode.READ_TIME_OUT.value, "Read Timeout: " + str(e))
        except urllib3.exceptions.MaxRetryError as e:
            if isinstance(e.reason, URLError):
                raise HttpException("Connect Failed: " + str(e.reason))
            raise HttpException("HTTP Request Failed: " + str(e))
        except urllib3.exceptions.HTTPError as e:
            raise HttpException("HTTP Error: " + str(e))
        except socket.timeout:
            raise ServerException(ErrorCode.READ_TIME_OUT.value, "Read Timeout")

    def _build_headers(self, request: HttpRequest) -> Dict[str, str]:
        """
        Build request headers.

        Args:
            request: HTTP request.

        Returns:
            Headers dictionary.
        """
        headers = {}

        if request.headers:
            for key, values in request.headers.items():
                headers[key] = ",".join(values) if values else ""

        if request.content_type:
            headers[HttpConstants.CONTENT_TYPE_HEADER] = str(request.content_type)

        return headers

    def _build_body(self, request: HttpRequest) -> Optional[str]:
        """
        Build request body.

        Args:
            request: HTTP request.

        Returns:
            Body string or None.
        """
        if request.content_type == ContentType.FORM and request.form_body:
            form_data = {}
            for key, values in request.form_body.items():
                form_data[key] = ",".join(values) if values else ""
            return urlencode(form_data)
        elif request.body:
            return request.body

        return None

    def _handle_response(self, response) -> HttpResponse:
        """
        Handle HTTP response.

        Args:
            response: urllib3 response.

        Returns:
            HttpResponse.

        Raises:
            ClientException: For 4xx errors.
            ServerException: For 5xx errors.
        """
        status_code = response.status
        body = response.data.decode("utf-8") if response.data else ""

        if 200 <= status_code < 300:
            return HttpResponse(status_code, body)
        elif 300 <= status_code < 400:
            redirect_location = response.headers.get(HttpConstants.LOCATION)
            redirect_message = f"{HttpConstants.REDIRECT_TO}{redirect_location}" if redirect_location else ""
            raise ClientException(str(status_code), f"{body} {redirect_message}")
        elif 400 <= status_code < 500:
            try:
                err_response = self._parse_error_response(body)
                raise ClientException(err_response.error, err_response.error_description, err_response.request_id)
            except (ValueError, KeyError):
                raise ClientException(str(status_code), body)
        else:
            try:
                err_response = self._parse_error_response(body)
                raise ServerException(err_response.error, err_response.error_description, err_response.request_id)
            except (ValueError, KeyError):
                raise ServerException(str(status_code), body)

    def _parse_error_response(self, body: str) -> ErrResponse:
        """
        Parse error response from body.

        Args:
            body: Response body.

        Returns:
            ErrResponse.
        """
        try:
            data = JSONUtil.parse_object(body, dict)
        except (ValueError, KeyError):
            data = {}

        error = data.get("error") or data.get("Code")
        error_description = data.get("error_description") or data.get("Message")
        request_id = data.get("request_id") or data.get("RequestId")

        return ErrResponse(error=error, error_description=error_description, request_id=request_id)


class HttpClientFactory:
    """
    Factory for creating HTTP client instances.
    """

    _singleton_client: Optional[DefaultHttpClient] = None

    @classmethod
    def get_default_http_client(cls, connect_timeout: int = 5000, read_timeout: int = 10000) -> DefaultHttpClient:
        """
        Get default HTTP client instance (singleton).

        Args:
            connect_timeout: Connect timeout in milliseconds.
            read_timeout: Read timeout in milliseconds.

        Returns:
            DefaultHttpClient instance.
        """
        if cls._singleton_client is None:
            cls._singleton_client = DefaultHttpClient(connect_timeout, read_timeout)
        return cls._singleton_client

    @classmethod
    def reset(cls):
        """Reset the singleton client (useful for testing)."""
        cls._singleton_client = None
