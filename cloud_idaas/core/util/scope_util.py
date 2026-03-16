import re

from cloud_idaas.core.constants import ErrorCode
from cloud_idaas.core.exceptions import ConfigException


class ScopeUtil:
    """Utility class for handling OAuth2 Scope strings."""

    _SCOPE_PATTERN = re.compile(r"^[^|]+\|[^|]+$")

    @staticmethod
    def split_scope(scope: str) -> list[str]:
        """
        Split a space-separated scope string into a list.

        Args:
            scope: A space-separated scope string

        Returns:
            A sorted list of scopes
        """
        if not scope or not scope.strip():
            return []
        return sorted(filter(None, (s.strip() for s in scope.split())))

    @staticmethod
    def is_valid_scope(scope: str) -> bool:
        """
        Check if the scope format is valid (format: prefix|value).

        Args:
            scope: The scope string to validate

        Returns:
            Whether the scope matches the expected format
        """
        if not scope:
            return False
        return bool(ScopeUtil._SCOPE_PATTERN.match(scope))

    @staticmethod
    def validate_scope(scope: str) -> None:
        """
        Validate scope string format.

        Rules:
        - Each scope item must follow format: audience|scope_value
        - Multiple scope items are separated by space
        - Only one unique audience is allowed

        Args:
            scope: The scope string to validate

        Raises:
            ConfigException: If scope is empty, invalid format, or has multiple audiences.

        Examples:
            - "api://target-service|read write" -> valid
            - "api://target-service|read" -> valid
            - "api://service1|read api://service2|write" -> raises ConfigException (multiple audiences)
            - "read write" -> raises ConfigException (missing audience)
        """
        scope_items = ScopeUtil.split_scope(scope)
        if not scope_items:
            raise ConfigException(ErrorCode.INVALID_SCOPE, "Scope is empty")

        audiences = set()
        for item in scope_items:
            if not ScopeUtil.is_valid_scope(item):
                raise ConfigException(ErrorCode.INVALID_SCOPE, f"Invalid scope: {item}")
            audience = item.split("|")[0]
            audiences.add(audience)

        if len(audiences) > 1:
            raise ConfigException(ErrorCode.MULTIPLE_AUDIENCE_NOT_SUPPORTED, "Multiple audiences are not supported")
