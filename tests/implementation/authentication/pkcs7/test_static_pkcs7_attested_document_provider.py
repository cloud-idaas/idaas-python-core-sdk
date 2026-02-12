"""
Unit tests for StaticPkcs7AttestedDocumentProvider
"""

from cloud_idaas.core.implementation.authentication.pkcs7.static_pkcs7_attested_document_provider import (
    StaticPkcs7AttestedDocumentProvider,
)


class TestStaticPkcs7AttestedDocumentProvider:
    """Test cases for StaticPkcs7AttestedDocumentProvider."""

    def test_initialization_with_document(self):
        """Test initialization with attested document."""
        provider = StaticPkcs7AttestedDocumentProvider("test_document")
        assert provider._attested_document == "test_document"

    def test_initialization_without_document(self):
        """Test initialization without attested document."""
        provider = StaticPkcs7AttestedDocumentProvider()
        assert provider._attested_document is None

    def test_get_attested_document(self):
        """Test getting attested document."""
        provider = StaticPkcs7AttestedDocumentProvider("test_document")
        document = provider.get_attested_document()
        assert document == "test_document"

    def test_get_attested_document_returns_none_when_not_set(self):
        """Test that get_attested_document returns None when not set."""
        provider = StaticPkcs7AttestedDocumentProvider()
        document = provider.get_attested_document()
        assert document is None

    def test_set_attested_document(self):
        """Test setting attested document."""
        provider = StaticPkcs7AttestedDocumentProvider()
        provider.set_attested_document("new_document")
        assert provider.get_attested_document() == "new_document"

    def test_set_attested_document_overwrites_existing(self):
        """Test that setting attested document overwrites existing value."""
        provider = StaticPkcs7AttestedDocumentProvider("old_document")
        provider.set_attested_document("new_document")
        assert provider.get_attested_document() == "new_document"

    def test_multiple_get_attested_document_calls(self):
        """Test that multiple get_attested_document calls return the same value."""
        provider = StaticPkcs7AttestedDocumentProvider("test_document")
        doc1 = provider.get_attested_document()
        doc2 = provider.get_attested_document()
        assert doc1 == doc2 == "test_document"

    def test_get_attested_document_with_empty_string(self):
        """Test getting attested document with empty string."""
        provider = StaticPkcs7AttestedDocumentProvider("")
        document = provider.get_attested_document()
        assert document == ""

    def test_set_attested_document_with_empty_string(self):
        """Test setting attested document with empty string."""
        provider = StaticPkcs7AttestedDocumentProvider("old_document")
        provider.set_attested_document("")
        assert provider.get_attested_document() == ""
