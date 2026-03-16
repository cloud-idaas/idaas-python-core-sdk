from cloud_idaas.core.constants import ErrorCode
from cloud_idaas.core.exceptions import ConfigException
from cloud_idaas.core.util.scope_util import ScopeUtil


class TestScopeUtil:
    """Test cases for ScopeUtil class."""

    class TestSplitScope:
        """Test cases for split_scope method."""

        def test_empty_string_returns_empty_list(self):
            """Test that empty string returns empty list."""
            result = ScopeUtil.split_scope("")
            assert result == []

        def test_none_returns_empty_list(self):
            """Test that None returns empty list."""
            result = ScopeUtil.split_scope(None)
            assert result == []

        def test_whitespace_only_returns_empty_list(self):
            """Test that whitespace-only string returns empty list."""
            result = ScopeUtil.split_scope("   ")
            assert result == []

        def test_single_scope_returns_list_with_one_item(self):
            """Test that single scope returns list with one item."""
            result = ScopeUtil.split_scope("openid")
            assert result == ["openid"]

        def test_multiple_scopes_returns_sorted_list(self):
            """Test that multiple scopes returns sorted list."""
            result = ScopeUtil.split_scope("profile openid email")
            assert result == ["email", "openid", "profile"]

        def test_extra_whitespace_is_trimmed(self):
            """Test that extra whitespace is trimmed."""
            result = ScopeUtil.split_scope("  openid   profile  ")
            assert result == ["openid", "profile"]

        def test_multiple_spaces_between_scopes(self):
            """Test handling of multiple spaces between scopes."""
            result = ScopeUtil.split_scope("openid    profile   email")
            assert result == ["email", "openid", "profile"]

        def test_duplicate_scopes_are_kept(self):
            """Test that duplicate scopes are kept in result."""
            result = ScopeUtil.split_scope("openid openid profile")
            assert result == ["openid", "openid", "profile"]

    class TestIsValidScope:
        """Test cases for is_valid_scope method."""

        def test_none_returns_false(self):
            """Test that None returns False."""
            result = ScopeUtil.is_valid_scope(None)
            assert result is False

        def test_empty_string_returns_false(self):
            """Test that empty string returns False."""
            result = ScopeUtil.is_valid_scope("")
            assert result is False

        def test_valid_scope_with_prefix_and_value(self):
            """Test valid scope with prefix and value."""
            result = ScopeUtil.is_valid_scope("api|read")
            assert result is True

        def test_valid_scope_with_complex_prefix(self):
            """Test valid scope with complex prefix."""
            result = ScopeUtil.is_valid_scope("https://api.example.com|read")
            assert result is True

        def test_invalid_scope_without_pipe(self):
            """Test invalid scope without pipe character."""
            result = ScopeUtil.is_valid_scope("read")
            assert result is False

        def test_invalid_scope_with_multiple_pipes(self):
            """Test invalid scope with multiple pipe characters."""
            result = ScopeUtil.is_valid_scope("api|read|write")
            assert result is False

        def test_invalid_scope_with_empty_prefix(self):
            """Test invalid scope with empty prefix before pipe."""
            result = ScopeUtil.is_valid_scope("|read")
            assert result is False

        def test_invalid_scope_with_empty_value(self):
            """Test invalid scope with empty value after pipe."""
            result = ScopeUtil.is_valid_scope("api|")
            assert result is False

        def test_invalid_scope_with_only_pipe(self):
            """Test invalid scope with only pipe character."""
            result = ScopeUtil.is_valid_scope("|")
            assert result is False

    class TestValidateScope:
        """Test cases for validate_scope method."""

        def test_valid_single_scope(self):
            """Test valid single scope with audience."""
            # Should not raise any exception
            ScopeUtil.validate_scope("api://test|read")

        def test_valid_multiple_scopes_same_audience(self):
            """Test valid multiple scopes with same audience."""
            # Should not raise any exception
            ScopeUtil.validate_scope("api://test|read api://test|write")

        def test_empty_scope_raises_exception(self):
            """Test that empty scope raises ConfigException."""
            import pytest

            with pytest.raises(ConfigException) as exc_info:
                ScopeUtil.validate_scope("")
            assert exc_info.value.error_code == ErrorCode.INVALID_SCOPE
            assert "empty" in str(exc_info.value).lower()

        def test_none_scope_raises_exception(self):
            """Test that None scope raises ConfigException."""
            import pytest

            with pytest.raises(ConfigException) as exc_info:
                ScopeUtil.validate_scope(None)
            assert exc_info.value.error_code == ErrorCode.INVALID_SCOPE

        def test_whitespace_scope_raises_exception(self):
            """Test that whitespace-only scope raises ConfigException."""
            import pytest

            with pytest.raises(ConfigException) as exc_info:
                ScopeUtil.validate_scope("   ")
            assert exc_info.value.error_code == ErrorCode.INVALID_SCOPE

        def test_invalid_scope_format_raises_exception(self):
            """Test that invalid scope format raises ConfigException."""
            import pytest

            with pytest.raises(ConfigException) as exc_info:
                ScopeUtil.validate_scope("read write")
            assert exc_info.value.error_code == ErrorCode.INVALID_SCOPE

        def test_multiple_audiences_raises_exception(self):
            """Test that multiple audiences raises ConfigException."""
            import pytest

            with pytest.raises(ConfigException) as exc_info:
                ScopeUtil.validate_scope("api://service1|read api://service2|write")
            assert exc_info.value.error_code == ErrorCode.MULTIPLE_AUDIENCE_NOT_SUPPORTED

        def test_scope_with_empty_audience_raises_exception(self):
            """Test that scope with empty audience raises ConfigException."""
            import pytest

            with pytest.raises(ConfigException) as exc_info:
                ScopeUtil.validate_scope("|read")
            assert exc_info.value.error_code == ErrorCode.INVALID_SCOPE
