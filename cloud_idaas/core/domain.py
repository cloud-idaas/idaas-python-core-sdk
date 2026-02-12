"""
IDaaS Python SDK - Domain Objects

This module contains domain objects used in the SDK.
"""

from typing import Optional


class ErrResponse:
    """
    Error response from the server.
    """

    def __init__(
        self, error: Optional[str] = None, error_description: Optional[str] = None, request_id: Optional[str] = None
    ):
        self.error: Optional[str] = error
        self.error_description: Optional[str] = error_description
        self.request_id: Optional[str] = request_id

    def __getattr__(self, name: str):
        """
        Support backward compatibility with private attribute access.
        Maps _error -> error, etc.
        """
        public_name = name.lstrip("_")
        if public_name in ("error", "error_description", "request_id"):
            return object.__getattribute__(self, public_name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value):
        """
        Support backward compatibility with private attribute access.
        Maps _error -> error, etc.
        """
        public_name = name.lstrip("_")
        if public_name in ("error", "error_description", "request_id"):
            object.__setattr__(self, public_name, value)
        else:
            object.__setattr__(self, name, value)

    def to_dict(self) -> dict:
        """
        Convert the error response to a dictionary.

        Returns:
            A dictionary representation of the error response.
        """
        result = {}
        if self.error:
            result["error"] = self.error
        if self.error_description:
            result["error_description"] = self.error_description
        if self.request_id:
            result["request_id"] = self.request_id
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "ErrResponse":
        """
        Create an error response from a dictionary.

        Args:
            data: The dictionary containing error data.

        Returns:
            A new ErrResponse instance.
        """
        return cls(
            error=data.get("error") or data.get("Code"),
            error_description=data.get("error_description") or data.get("Message"),
            request_id=data.get("request_id") or data.get("RequestId"),
        )

    def __repr__(self) -> str:
        """
        Return a string representation of the error response.

        Returns:
            String representation of the error response.
        """
        return (
            f"ErrResponse(error={self.error!r}, "
            f"error_description={self.error_description!r}, "
            f"request_id={self.request_id!r})"
        )

    def __eq__(self, other) -> bool:
        """
        Check if two ErrResponse objects are equal.

        Args:
            other: Another object to compare with.

        Returns:
            True if equal, False otherwise.
        """
        if not isinstance(other, ErrResponse):
            return NotImplemented
        return (
            self.error == other.error
            and self.error_description == other.error_description
            and self.request_id == other.request_id
        )

    def __hash__(self) -> int:
        """
        Return a hash value for the ErrResponse object.

        Returns:
            Hash value.
        """
        return hash((self.error, self.error_description, self.request_id))


class DeviceCodeResponse:
    """
    Device code response from the authorization endpoint.
    """

    def __init__(self):
        self.device_code: Optional[str] = None
        self.user_code: Optional[str] = None
        self.verification_uri: Optional[str] = None
        self.verification_uri_complete: Optional[str] = None
        self.expires_in: Optional[int] = None
        self.expires_at: Optional[int] = None
        self.interval: Optional[int] = None

    def __getattr__(self, name: str):
        """
        Support backward compatibility with private attribute access.
        Maps _device_code -> device_code, etc.
        """
        public_name = name.lstrip("_")
        if public_name in (
            "device_code",
            "user_code",
            "verification_uri",
            "verification_uri_complete",
            "expires_in",
            "expires_at",
            "interval",
        ):
            return object.__getattribute__(self, public_name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value):
        """
        Support backward compatibility with private attribute access.
        Maps _device_code -> device_code, etc.
        """
        public_name = name.lstrip("_")
        if public_name in (
            "device_code",
            "user_code",
            "verification_uri",
            "verification_uri_complete",
            "expires_in",
            "expires_at",
            "interval",
        ):
            object.__setattr__(self, public_name, value)
        else:
            object.__setattr__(self, name, value)

    def to_dict(self) -> dict:
        """
        Convert the device code response to a dictionary.

        Returns:
            A dictionary representation of the device code response.
        """
        result = {}
        if self.device_code:
            result["device_code"] = self.device_code
        if self.user_code:
            result["user_code"] = self.user_code
        if self.verification_uri:
            result["verification_uri"] = self.verification_uri
        if self.verification_uri_complete:
            result["verification_uri_complete"] = self.verification_uri_complete
        if self.expires_in is not None:
            result["expires_in"] = self.expires_in
        if self.expires_at is not None:
            result["expires_at"] = self.expires_at
        if self.interval is not None:
            result["interval"] = self.interval
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "DeviceCodeResponse":
        """
        Create a device code response from a dictionary.

        Args:
            data: The dictionary containing device code data.

        Returns:
            A new DeviceCodeResponse instance.
        """
        response = cls()
        response.device_code = data.get("device_code")
        response.user_code = data.get("user_code")
        response.verification_uri = data.get("verification_uri")
        response.verification_uri_complete = data.get("verification_uri_complete")
        response.expires_in = data.get("expires_in")
        response.expires_at = data.get("expires_at")
        response.interval = data.get("interval")
        return response

    def __repr__(self) -> str:
        """
        Return a string representation of the device code response.

        Returns:
            String representation of the device code response.
        """
        return (
            f"DeviceCodeResponse(device_code={self.device_code!r}, "
            f"user_code={self.user_code!r}, verification_uri={self.verification_uri!r}, "
            f"verification_uri_complete={self.verification_uri_complete!r}, "
            f"expires_in={self.expires_in}, expires_at={self.expires_at}, "
            f"interval={self.interval})"
        )

    def __eq__(self, other) -> bool:
        """
        Check if two DeviceCodeResponse objects are equal.

        Args:
            other: Another object to compare with.

        Returns:
            True if equal, False otherwise.
        """
        if not isinstance(other, DeviceCodeResponse):
            return NotImplemented
        return (
            self.device_code == other.device_code
            and self.user_code == other.user_code
            and self.verification_uri == other.verification_uri
            and self.verification_uri_complete == other.verification_uri_complete
            and self.expires_in == other.expires_in
            and self.expires_at == other.expires_at
            and self.interval == other.interval
        )

    def __hash__(self) -> int:
        """
        Return a hash value for the DeviceCodeResponse object.

        Returns:
            Hash value.
        """
        return hash(
            (
                self.device_code,
                self.user_code,
                self.verification_uri,
                self.verification_uri_complete,
                self.expires_in,
                self.expires_at,
                self.interval,
            )
        )
