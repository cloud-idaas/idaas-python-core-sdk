"""
Unit tests for IDaaS Python SDK exceptions
"""

from cloud_idaas import (
    CacheException,
    ClientException,
    ConcurrentOperationException,
    ConfigException,
    CredentialException,
    EncodingException,
    HttpException,
    IDaaSException,
    ServerException,
)


class TestIDaaSException:
    """Test cases for IDaaSException"""

    def test_init_with_message_only(self):
        exc = IDaaSException("Test message")
        assert exc.message == "Test message"
        assert exc.cause is None
        assert str(exc) == "Test message"

    def test_init_with_message_and_cause(self):
        cause = ValueError("Original error")
        exc = IDaaSException("Test message", cause)
        assert exc.message == "Test message"
        assert exc.cause == cause

    def test_init_without_message(self):
        exc = IDaaSException()
        assert exc.message is None
        assert exc.cause is None


class TestClientException:
    """Test cases for ClientException"""

    def test_init_with_all_params(self):
        exc = ClientException("ERR001", "Test error message", "req-123")
        assert exc.error_code == "ERR001"
        assert exc.error_message == "Test error message"
        assert exc.request_id == "req-123"
        assert "ERR001" in str(exc)

    def test_init_with_error_code_and_message(self):
        exc = ClientException("ERR001", "Test error message")
        assert exc.error_code == "ERR001"
        assert exc.error_message == "Test error message"
        assert exc.request_id is None

    def test_init_with_message_only(self):
        exc = ClientException("Test error message")
        assert exc.error_code is None
        assert exc.error_message == "Test error message"

    def test_setters(self):
        exc = ClientException()
        exc.error_code = "ERR001"
        exc.error_message = "Test message"
        exc.request_id = "req-123"
        assert exc.error_code == "ERR001"
        assert exc.error_message == "Test message"
        assert exc.request_id == "req-123"


class TestServerException:
    """Test cases for ServerException"""

    def test_init_with_all_params(self):
        exc = ServerException("ERR002", "Server error", "req-456")
        assert exc.error_code == "ERR002"
        assert exc.error_message == "Server error"
        assert exc.request_id == "req-456"

    def test_init_with_error_code_and_message(self):
        exc = ServerException("ERR002", "Server error")
        assert exc.error_code == "ERR002"
        assert exc.error_message == "Server error"
        assert exc.request_id is None

    def test_setters(self):
        exc = ServerException()
        exc.error_code = "ERR002"
        exc.error_message = "Server message"
        exc.request_id = "req-789"
        assert exc.error_code == "ERR002"
        assert exc.error_message == "Server message"
        assert exc.request_id == "req-789"


class TestConfigException:
    """Test cases for ConfigException"""

    def test_init_with_message(self):
        exc = ConfigException("Config error")
        assert exc.error_message == "Config error"
        assert exc.error_code is None

    def test_init_with_error_code_and_message(self):
        exc = ConfigException("CONFIG_ERR", "Config not found")
        assert exc.error_code == "CONFIG_ERR"
        assert exc.error_message == "Config not found"

    def test_is_client_exception(self):
        exc = ConfigException("Config error")
        assert isinstance(exc, ClientException)


class TestCacheException:
    """Test cases for CacheException"""

    def test_init_with_message(self):
        exc = CacheException("Cache error")
        assert exc.error_message == "Cache error"
        assert exc.error_code is None

    def test_init_with_error_code_and_message(self):
        exc = CacheException("CACHE_ERR", "Cache miss")
        assert exc.error_code == "CACHE_ERR"
        assert exc.error_message == "Cache miss"

    def test_init_with_cause(self):
        cause = ValueError("Cache failure")
        exc = CacheException("CACHE_ERR", "Cache miss", cause)
        assert exc.error_code == "CACHE_ERR"
        assert exc.error_message == "Cache miss"
        assert exc.cause == cause


class TestConcurrentOperationException:
    """Test cases for ConcurrentOperationException"""

    def test_init_default(self):
        exc = ConcurrentOperationException()
        assert exc.error_code == "ConcurrentOperationFailed"
        assert "concurrent operation" in exc.error_message.lower()

    def test_init_with_custom_values(self):
        exc = ConcurrentOperationException("CUSTOM_ERR", "Custom concurrent error")
        assert exc.error_code == "CUSTOM_ERR"
        assert exc.error_message == "Custom concurrent error"

    def test_is_client_exception(self):
        exc = ConcurrentOperationException()
        assert isinstance(exc, ClientException)


class TestCredentialException:
    """Test cases for CredentialException"""

    def test_init_with_message(self):
        exc = CredentialException("Credential error")
        assert exc.error_message == "Credential error"
        assert exc.error_code is None

    def test_init_with_error_code_and_message(self):
        exc = CredentialException("CRED_ERR", "Invalid credential")
        assert exc.error_code == "CRED_ERR"
        assert exc.error_message == "Invalid credential"

    def test_init_with_cause(self):
        cause = ValueError("Credential failure")
        exc = CredentialException("CRED_ERR", "Invalid credential", cause)
        assert exc.error_code == "CRED_ERR"
        assert exc.error_message == "Invalid credential"
        assert exc.cause == cause


class TestEncodingException:
    """Test cases for EncodingException"""

    def test_init_with_message(self):
        exc = EncodingException("Encoding error")
        assert exc.error_message == "Encoding error"
        assert exc.error_code is None

    def test_init_with_error_code_and_message(self):
        exc = EncodingException("ENC_ERR", "Encoding failed")
        assert exc.error_code == "ENC_ERR"
        assert exc.error_message == "Encoding failed"

    def test_init_with_cause(self):
        cause = ValueError("Encoding failure")
        exc = EncodingException("ENC_ERR", "Encoding failed", cause)
        assert exc.error_code == "ENC_ERR"
        assert exc.error_message == "Encoding failed"
        assert exc.cause == cause


class TestHttpException:
    """Test cases for HttpException"""

    def test_init_with_message(self):
        exc = HttpException("HTTP error")
        assert exc.message == "HTTP error"
        assert exc.cause is None

    def test_init_with_cause(self):
        cause = ConnectionError("Connection failed")
        exc = HttpException("HTTP error", cause)
        assert exc.message == "HTTP error"
        assert exc.cause == cause
