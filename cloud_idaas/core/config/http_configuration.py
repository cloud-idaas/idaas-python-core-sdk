"""
IDaaS Python SDK - HTTP Configuration
"""

from typing import Optional


class HttpConfiguration:
    """
    HTTP configuration class.
    """

    def __init__(self):
        self._connect_timeout: int = 5000
        self._read_timeout: int = 10000
        self._unsafe_ignore_ssl_cert: bool = False

    @property
    def connect_timeout(self) -> int:
        return self._connect_timeout

    @connect_timeout.setter
    def connect_timeout(self, value: int):
        self._connect_timeout = value

    @property
    def read_timeout(self) -> int:
        return self._read_timeout

    @read_timeout.setter
    def read_timeout(self, value: int):
        self._read_timeout = value

    @property
    def unsafe_ignore_ssl_cert(self) -> bool:
        return self._unsafe_ignore_ssl_cert

    @unsafe_ignore_ssl_cert.setter
    def unsafe_ignore_ssl_cert(self, value: bool):
        self._unsafe_ignore_ssl_cert = value

    def __repr__(self) -> str:
        """
        Return a string representation of the HTTP configuration.

        Returns:
            String representation of the configuration.
        """
        return (
            f"HttpConfiguration(connect_timeout={self._connect_timeout}, "
            f"read_timeout={self._read_timeout}, "
            f"unsafe_ignore_ssl_cert={self._unsafe_ignore_ssl_cert})"
        )

    def __eq__(self, other) -> bool:
        """
        Check if two HttpConfiguration objects are equal.

        Args:
            other: Another object to compare with.

        Returns:
            True if equal, False otherwise.
        """
        if not isinstance(other, HttpConfiguration):
            return NotImplemented
        return (
            self._connect_timeout == other._connect_timeout
            and self._read_timeout == other._read_timeout
            and self._unsafe_ignore_ssl_cert == other._unsafe_ignore_ssl_cert
        )

    def __hash__(self) -> int:
        """
        Return a hash value for the HttpConfiguration object.

        Returns:
            Hash value.
        """
        return hash((self._connect_timeout, self._read_timeout, self._unsafe_ignore_ssl_cert))

    @staticmethod
    def copy(source: "HttpConfiguration") -> Optional["HttpConfiguration"]:
        """
        Create a copy of the HTTP configuration.

        Args:
            source: The source configuration to copy.

        Returns:
            A new HttpConfiguration instance with copied values.
        """
        if source is None:
            return None
        http_configuration = HttpConfiguration()
        http_configuration._connect_timeout = source._connect_timeout
        http_configuration._read_timeout = source._read_timeout
        http_configuration._unsafe_ignore_ssl_cert = source._unsafe_ignore_ssl_cert
        return http_configuration

    @classmethod
    def from_dict(cls, data: dict) -> "HttpConfiguration":
        """
        Create an HttpConfiguration instance from a dictionary.

        Supports both camelCase (JSON config style) and snake_case (Python style) keys.

        Args:
            data: Dictionary containing HttpConfiguration properties.

        Returns:
            An HttpConfiguration instance with values from the dictionary.
        """
        from cloud_idaas.core.util.string_util import StringUtil

        http_config = cls()
        if data is not None:
            # Normalize keys: convert camelCase to snake_case for lookup
            normalized_data = {}
            for key, value in data.items():
                normalized_key = StringUtil.camel_to_snake(key)
                normalized_data[normalized_key] = value

            if "connect_timeout" in normalized_data:
                http_config.connect_timeout = normalized_data["connect_timeout"]
            if "read_timeout" in normalized_data:
                http_config.read_timeout = normalized_data["read_timeout"]
            if "unsafe_ignore_ssl_cert" in normalized_data:
                http_config.unsafe_ignore_ssl_cert = normalized_data["unsafe_ignore_ssl_cert"]
        return http_config
