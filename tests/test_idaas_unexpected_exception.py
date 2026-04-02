"""
IDaaS Python SDK - Test IDaaS Unexpected Exception
"""

import pytest

from cloud_idaas.core.exceptions import IDaaSUnexpectedException


class TestIDaaSUnexpectedException:
    """Tests for IDaaSUnexpectedException."""

    def test_create_with_message(self):
        """Test creating exception with message."""
        exc = IDaaSUnexpectedException(message="Something went wrong")

        assert str(exc) == "Something went wrong"
        assert exc.error_message == "Something went wrong"
        assert exc.error_code is None
        assert exc.cause is None

    def test_create_with_error_code_and_message(self):
        """Test creating exception with error code and message."""
        exc = IDaaSUnexpectedException(message="Something went wrong", error_code="ERR001")

        assert str(exc) == "Something went wrong"
        assert exc.error_message == "Something went wrong"
        assert exc.error_code == "ERR001"
        assert exc.cause is None

    def test_create_with_cause(self):
        """Test creating exception with cause."""
        cause = ValueError("Original error")
        exc = IDaaSUnexpectedException(message="Wrapped error", cause=cause)

        assert exc.error_message == "Wrapped error"
        assert exc.cause == cause
        assert isinstance(exc.cause, ValueError)

    def test_create_with_all_parameters(self):
        """Test creating exception with all parameters."""
        cause = RuntimeError("Original error")
        exc = IDaaSUnexpectedException(
            message="Something went wrong",
            error_code="ERR002",
            cause=cause,
        )

        assert exc.error_message == "Something went wrong"
        assert exc.error_code == "ERR002"
        assert exc.cause == cause

    def test_set_error_code(self):
        """Test setting error code."""
        exc = IDaaSUnexpectedException(message="Test")
        exc.error_code = "NEW_CODE"

        assert exc.error_code == "NEW_CODE"

    def test_set_error_message(self):
        """Test setting error message."""
        exc = IDaaSUnexpectedException(message="Test")
        exc.error_message = "New message"

        assert exc.error_message == "New message"

    def test_raise_exception(self):
        """Test raising the exception."""
        with pytest.raises(IDaaSUnexpectedException) as exc_info:
            raise IDaaSUnexpectedException(message="Test error")

        assert str(exc_info.value) == "Test error"

    def test_catch_as_exception(self):
        """Test catching as generic Exception."""
        with pytest.raises(Exception) as exc_info:
            raise IDaaSUnexpectedException(message="Test error")

        assert isinstance(exc_info.value, IDaaSUnexpectedException)
