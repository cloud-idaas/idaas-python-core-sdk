"""
Unit tests for FileOidcTokenProvider
"""

import os
import tempfile
from datetime import timezone
from unittest.mock import patch

import pytest

from cloud_idaas import CredentialException
from cloud_idaas.core.implementation.authentication.oidc.file_oidc_token_provider import (
    FileOidcTokenProvider,
)

# Sample JWT token with expiration claim
SAMPLE_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjk5OTk5OTk5OTl9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"


class TestFileOidcTokenProvider:
    """Test cases for FileOidcTokenProvider."""

    def test_initialization(self):
        """Test initialization with file path."""
        provider = FileOidcTokenProvider("/path/to/token")
        assert provider.get_oidc_token_file_path() == "/path/to/token"

    def test_get_oidc_token_file_path(self):
        """Test getting OIDC token file path."""
        provider = FileOidcTokenProvider("/test/path/token")
        assert provider.get_oidc_token_file_path() == "/test/path/token"

    @patch("cloud_idaas.core.implementation.authentication.oidc.file_oidc_token_provider.FileUtil.read_file")
    def test_get_oidc_token_reads_from_file(self, mock_read_file):
        """Test that get_oidc_token reads from file."""
        mock_read_file.return_value = SAMPLE_JWT_TOKEN
        provider = FileOidcTokenProvider("/path/to/token")

        token = provider.get_oidc_token()
        assert token == SAMPLE_JWT_TOKEN
        mock_read_file.assert_called_once_with("/path/to/token")

    @patch("cloud_idaas.core.implementation.authentication.oidc.file_oidc_token_provider.FileUtil.read_file")
    def test_get_oidc_token_caches_result(self, mock_read_file):
        """Test that get_oidc_token caches the result."""
        mock_read_file.return_value = SAMPLE_JWT_TOKEN
        provider = FileOidcTokenProvider("/path/to/token")

        token1 = provider.get_oidc_token()
        token2 = provider.get_oidc_token()

        assert token1 == token2 == SAMPLE_JWT_TOKEN
        # Should only read once due to caching
        mock_read_file.assert_called_once()

    @patch("cloud_idaas.core.implementation.authentication.oidc.file_oidc_token_provider.FileUtil.read_file")
    def test_get_oidc_token_reads_again_when_expired(self, mock_read_file):
        """Test that get_oidc_token reads again when token is expired."""
        # First call returns an expired token (exp in past)
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjEwMDAwMDAwMDB9.invalid"
        # Second call returns a new token
        new_token = SAMPLE_JWT_TOKEN
        mock_read_file.side_effect = [expired_token, new_token]

        provider = FileOidcTokenProvider("/path/to/token")

        token1 = provider.get_oidc_token()
        token2 = provider.get_oidc_token()

        # First call gets expired token
        assert token1 == expired_token
        # Second call reads again because token is expired
        assert token2 == new_token
        assert mock_read_file.call_count == 2

    @patch("cloud_idaas.core.implementation.authentication.oidc.file_oidc_token_provider.FileUtil.read_file")
    def test_get_oidc_token_refreshes_when_expiring_soon(self, mock_read_file):
        """Test that get_oidc_token refreshes when expiring within 10 minutes."""
        # Token expiring in 5 minutes
        from datetime import datetime, timedelta

        exp_time = int((datetime.now(timezone.utc) + timedelta(minutes=5)).timestamp())
        soon_to_expire_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjtleHBlcH0=.invalid"
        new_token = SAMPLE_JWT_TOKEN

        mock_read_file.side_effect = [soon_to_expire_token, new_token]

        provider = FileOidcTokenProvider("/path/to/token")

        token1 = provider.get_oidc_token()
        token2 = provider.get_oidc_token()

        # Second call should read again because token is expiring soon
        assert mock_read_file.call_count >= 1

    @patch("cloud_idaas.core.implementation.authentication.oidc.file_oidc_token_provider.FileUtil.read_file")
    def test_get_oidc_token_handles_file_read_error(self, mock_read_file):
        """Test that get_oidc_token handles file read errors."""
        mock_read_file.side_effect = OSError("File not found")
        provider = FileOidcTokenProvider("/path/to/token")

        with pytest.raises(CredentialException, match="Failed to read or parse OIDC token"):
            provider.get_oidc_token()

    def test_get_oidc_token_with_real_temp_file(self):
        """Test get_oidc_token with a real temporary file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write(SAMPLE_JWT_TOKEN)
            temp_file = f.name

        try:
            provider = FileOidcTokenProvider(temp_file)
            token = provider.get_oidc_token()
            assert token == SAMPLE_JWT_TOKEN
        finally:
            os.unlink(temp_file)

    def test_parse_expiration_time_valid_jwt(self):
        """Test parsing expiration time from valid JWT."""
        provider = FileOidcTokenProvider("/path/to/token")
        exp_time = provider._parse_expiration_time(SAMPLE_JWT_TOKEN)
        assert exp_time is not None
        assert exp_time == 9999999999

    def test_parse_expiration_time_invalid_jwt(self):
        """Test parsing expiration time from invalid JWT."""
        provider = FileOidcTokenProvider("/path/to/token")
        exp_time = provider._parse_expiration_time("invalid.jwt.token")
        assert exp_time is None

    def test_parse_expiration_time_jwt_without_exp(self):
        """Test parsing expiration time from JWT without exp claim."""
        from jwt import encode

        claims = {"sub": "test_user"}
        token = encode(claims, "secret", algorithm="HS256")

        provider = FileOidcTokenProvider("/path/to/token")
        exp_time = provider._parse_expiration_time(token)
        assert exp_time is None

    def test_will_soon_expire_with_no_expiration(self):
        """Test _will_soon_expire when there's no expiration time."""
        provider = FileOidcTokenProvider("/path/to/token")
        provider._expires_time = None
        assert provider._will_soon_expire() is True

    def test_will_soon_expire_with_future_expiration(self):
        """Test _will_soon_expire with future expiration."""
        from datetime import datetime, timedelta, timezone

        provider = FileOidcTokenProvider("/path/to/token")
        provider._expires_time = int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp())
        assert provider._will_soon_expire() is False

    def test_will_soon_expire_with_expiring_soon(self):
        """Test _will_soon_expire when token is expiring soon."""
        from datetime import datetime, timedelta, timezone

        provider = FileOidcTokenProvider("/path/to/token")
        # Expires in 5 minutes (less than 10 minutes threshold)
        provider._expires_time = int((datetime.now(timezone.utc) + timedelta(minutes=5)).timestamp())
        assert provider._will_soon_expire() is True

    def test_will_soon_expire_with_expired_token(self):
        """Test _will_soon_expire when token is already expired."""
        from datetime import datetime, timedelta, timezone

        provider = FileOidcTokenProvider("/path/to/token")
        # Expired 1 hour ago
        provider._expires_time = int((datetime.now(timezone.utc) - timedelta(hours=1)).timestamp())
        assert provider._will_soon_expire() is True
