import re


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
