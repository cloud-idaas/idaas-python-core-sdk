"""
Unit tests for Pkcs7AttestedDocumentProvider
"""

import pytest

from cloud_idaas.core.provider import Pkcs7AttestedDocumentProvider


class MockPkcs7AttestedDocumentProvider(Pkcs7AttestedDocumentProvider):
    """Mock implementation of Pkcs7AttestedDocumentProvider for testing."""

    def __init__(self, document=None):
        self._document = document

    def get_attested_document(self):
        return self._document


class TestPkcs7AttestedDocumentProvider:
    """Test cases for Pkcs7AttestedDocumentProvider."""

    def test_get_attested_document_returns_value(self):
        """Test that get_attested_document returns the configured value."""
        provider = MockPkcs7AttestedDocumentProvider("test_document")
        assert provider.get_attested_document() == "test_document"

    def test_get_attested_document_returns_none(self):
        """Test that get_attested_document returns None when not configured."""
        provider = MockPkcs7AttestedDocumentProvider()
        assert provider.get_attested_document() is None

    def test_is_abstract_class(self):
        """Test that Pkcs7AttestedDocumentProvider is an abstract class."""
        with pytest.raises(TypeError):
            # Cannot instantiate abstract class directly
            Pkcs7AttestedDocumentProvider()

    def test_mock_implementation_works(self):
        """Test that mock implementation works correctly."""
        provider = MockPkcs7AttestedDocumentProvider("pkcs7.document.here")
        assert provider.get_attested_document() == "pkcs7.document.here"

    def test_multiple_get_calls_return_same_value(self):
        """Test that multiple get_attested_document calls return same value."""
        provider = MockPkcs7AttestedDocumentProvider("consistent_document")
        assert provider.get_attested_document() == provider.get_attested_document()

    def test_get_attested_document_with_empty_string(self):
        """Test get_attested_document with empty string."""
        provider = MockPkcs7AttestedDocumentProvider("")
        assert provider.get_attested_document() == ""

    def test_get_attested_document_with_base64_like_string(self):
        """Test get_attested_document with base64-like string."""
        base64_doc = "dGVzdC1kb2N1bWVudC1kYXRh"
        provider = MockPkcs7AttestedDocumentProvider(base64_doc)
        assert provider.get_attested_document() == base64_doc
