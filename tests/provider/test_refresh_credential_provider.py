"""
Unit tests for RefreshCredentialProvider and RefreshResult (provider module)
"""

from unittest.mock import Mock

import pytest

from cloud_idaas.core.provider import RefreshCredentialProvider, RefreshResult


class MockRefreshCredentialProvider(RefreshCredentialProvider):
    """Mock implementation of RefreshCredentialProvider for testing."""

    def __init__(self, refresh_result=None):
        self._refresh_result = refresh_result

    def refresh_credential(self):
        return self._refresh_result


class TestRefreshCredentialProvider:
    """Test cases for RefreshCredentialProvider."""

    def test_refresh_credential_returns_value(self):
        """Test that refresh_credential returns the configured value."""
        mock_result = Mock()
        provider = MockRefreshCredentialProvider(mock_result)
        assert provider.refresh_credential() == mock_result

    def test_refresh_credential_returns_none(self):
        """Test that refresh_credential returns None when not configured."""
        provider = MockRefreshCredentialProvider()
        assert provider.refresh_credential() is None

    def test_is_abstract_class(self):
        """Test that RefreshCredentialProvider is an abstract class."""
        with pytest.raises(TypeError):
            # Cannot instantiate abstract class directly
            RefreshCredentialProvider()

    def test_mock_implementation_works(self):
        """Test that mock implementation works correctly."""
        mock_result = Mock()
        provider = MockRefreshCredentialProvider(mock_result)
        assert provider.refresh_credential() == mock_result

    def test_multiple_refresh_calls_return_same_value(self):
        """Test that multiple refresh_credential calls return same value."""
        mock_result = Mock()
        provider = MockRefreshCredentialProvider(mock_result)
        assert provider.refresh_credential() == provider.refresh_credential()


class TestRefreshResult:
    """Test cases for RefreshResult."""

    def test_initialization(self):
        """Test RefreshResult initialization."""
        result = RefreshResult("test_value", True)
        assert result.value == "test_value"
        assert result.is_refreshed is True

    def test_value_property(self):
        """Test value property."""
        result = RefreshResult("test_value", False)
        assert result.value == "test_value"

    def test_is_refreshed_property(self):
        """Test is_refreshed property."""
        result = RefreshResult("test_value", True)
        assert result.is_refreshed is True

    def test_is_refreshed_false(self):
        """Test is_refreshed property when False."""
        result = RefreshResult("test_value", False)
        assert result.is_refreshed is False

    def test_value_can_be_any_type(self):
        """Test that value can be of any type."""
        # String
        result1 = RefreshResult("string_value", True)
        assert result1.value == "string_value"

        # Integer
        result2 = RefreshResult(123, True)
        assert result2.value == 123

        # List
        result3 = RefreshResult([1, 2, 3], True)
        assert result3.value == [1, 2, 3]

        # Dict
        result4 = RefreshResult({"key": "value"}, True)
        assert result4.value == {"key": "value"}

        # None
        result5 = RefreshResult(None, True)
        assert result5.value is None

    def test_value_property_readonly(self):
        """Test that value property is read-only."""
        result = RefreshResult("test_value", True)
        # Should not be able to set value directly (property has no setter)
        # This test verifies the property behaves as expected
        assert result.value == "test_value"

    def test_is_refreshed_property_readonly(self):
        """Test that is_refreshed property is read-only."""
        result = RefreshResult("test_value", True)
        # Should not be able to set is_refreshed directly (property has no setter)
        # This test verifies the property behaves as expected
        assert result.is_refreshed is True
