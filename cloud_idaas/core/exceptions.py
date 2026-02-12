"""
IDaaS Python SDK - Exceptions

This module contains all exception classes used in the SDK.
"""

from typing import Optional


class IDaaSException(Exception):
    """
    Base exception class for all IDaaS SDK exceptions.
    """

    def __init__(self, message: Optional[str] = None, cause: Optional[Exception] = None):
        self._message = message
        self._cause = cause
        super().__init__(message)

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def cause(self) -> Optional[Exception]:
        return self._cause


class _CodeMessageException(IDaaSException):
    """
    Base class for exceptions with error_code and error_message attributes.
    """

    def __init__(
        self, error_code: Optional[str] = None, error_message: Optional[str] = None, cause: Optional[Exception] = None
    ):
        # Handle single string argument case (treated as error_message)
        if error_code is not None and error_message is None and cause is None:
            error_message = error_code
            error_code = None

        self._error_code = error_code
        self._error_message = error_message
        message = f"{error_code}: {error_message}" if error_code and error_message else error_message
        super().__init__(message, cause)

    @property
    def error_code(self) -> Optional[str]:
        return self._error_code

    @error_code.setter
    def error_code(self, value: str):
        self._error_code = value

    @property
    def error_message(self) -> Optional[str]:
        return self._error_message

    @error_message.setter
    def error_message(self, value: str):
        self._error_message = value


class ClientException(_CodeMessageException):
    """
    Exception thrown when a client-side error occurs.
    """

    def __init__(
        self, error_code: Optional[str] = None, error_message: Optional[str] = None, request_id: Optional[str] = None
    ):
        super().__init__(error_code, error_message)
        self._request_id = request_id

    @property
    def request_id(self) -> Optional[str]:
        return self._request_id

    @request_id.setter
    def request_id(self, value: str):
        self._request_id = value


class ServerException(_CodeMessageException):
    """
    Exception thrown when a server-side error occurs.
    """

    def __init__(
        self, error_code: Optional[str] = None, error_message: Optional[str] = None, request_id: Optional[str] = None
    ):
        super().__init__(error_code, error_message)
        self._request_id = request_id

    @property
    def request_id(self) -> Optional[str]:
        return self._request_id

    @request_id.setter
    def request_id(self, value: str):
        self._request_id = value


class ConfigException(ClientException):
    """
    Exception thrown when a configuration error occurs.
    """

    def __init__(self, error_code: Optional[str] = None, error_message: Optional[str] = None):
        # Handle single string argument case (treated as error_message)
        if error_code is not None and error_message is None:
            error_message = error_code
            error_code = None
        super().__init__(error_code, error_message)


class CacheException(_CodeMessageException):
    """
    Exception thrown when a cache operation fails.
    """


class ConcurrentOperationException(ClientException):
    """
    Exception thrown when a concurrent operation fails.
    """

    def __init__(
        self,
        error_code: str = "ConcurrentOperationFailed",
        error_message: str = "A concurrent operation is in progress, causing the current operation to fail.",
    ):
        super().__init__(error_code, error_message)


class CredentialException(_CodeMessageException):
    """
    Exception thrown when a credential operation fails.
    """


class EncodingException(_CodeMessageException):
    """
    Exception thrown when an encoding operation fails.
    """


class HttpException(IDaaSException):
    """
    Exception thrown when an HTTP operation fails.
    """

    def __init__(self, error_message: Optional[str] = None, cause: Optional[Exception] = None):
        super().__init__(error_message, cause)
