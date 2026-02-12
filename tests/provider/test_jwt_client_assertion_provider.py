"""
Unit tests for JwtClientAssertionProvider
"""

import pytest

from cloud_idaas.core.provider import JwtClientAssertionProvider


class MockJwtClientAssertionProvider(JwtClientAssertionProvider):
    """Mock implementation of JwtClientAssertionProvider for testing."""

    def __init__(self, assertion=None):
        self._assertion = assertion

    def get_client_assertion(self):
        return self._assertion


class TestJwtClientAssertionProvider:
    """Test cases for JwtClientAssertionProvider."""

    def test_get_client_assertion_returns_value(self):
        """Test that get_client_assertion returns the configured value."""
        provider = MockJwtClientAssertionProvider("test_assertion")
        assert provider.get_client_assertion() == "test_assertion"

    def test_get_client_assertion_returns_none(self):
        """Test that get_client_assertion returns None when not configured."""
        provider = MockJwtClientAssertionProvider()
        assert provider.get_client_assertion() is None

    def test_is_abstract_class(self):
        """Test that JwtClientAssertionProvider is an abstract class."""
        with pytest.raises(TypeError):
            # Cannot instantiate abstract class directly
            JwtClientAssertionProvider()

    def test_mock_implementation_works(self):
        """Test that mock implementation works correctly."""
        provider = MockJwtClientAssertionProvider("jwt.token.here")
        assert provider.get_client_assertion() == "jwt.token.here"

    def test_multiple_get_calls_return_same_value(self):
        """Test that multiple get_client_assertion calls return same value."""
        provider = MockJwtClientAssertionProvider("consistent_assertion")
        assert provider.get_client_assertion() == provider.get_client_assertion()
