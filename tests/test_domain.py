"""
Unit tests for IDaaS Python SDK domain objects
"""

from cloud_idaas import (
    DeviceCodeResponse,
    ErrResponse,
)


class TestErrResponse:
    """Test cases for ErrResponse"""

    def test_init_default(self):
        """Test default initialization"""
        err = ErrResponse()
        assert err._error is None
        assert err._error_description is None
        assert err._request_id is None

    def test_init_with_params(self):
        """Test initialization with parameters"""
        err = ErrResponse("invalid_request", "The request is invalid", "req-123")
        assert err._error == "invalid_request"
        assert err._error_description == "The request is invalid"
        assert err._request_id == "req-123"

    def test_error_property(self):
        """Test error property getter and setter"""
        err = ErrResponse()
        assert err.error is None

        err.error = "invalid_request"
        assert err.error == "invalid_request"

    def test_error_description_property(self):
        """Test error_description property getter and setter"""
        err = ErrResponse()
        assert err.error_description is None

        err.error_description = "The request is invalid"
        assert err.error_description == "The request is invalid"

    def test_request_id_property(self):
        """Test request_id property getter and setter"""
        err = ErrResponse()
        assert err.request_id is None

        err.request_id = "req-123"
        assert err.request_id == "req-123"

    def test_to_dict_empty(self):
        """Test to_dict with empty response"""
        err = ErrResponse()
        result = err.to_dict()
        assert result == {}

    def test_to_dict_partial(self):
        """Test to_dict with partial data"""
        err = ErrResponse()
        err.error = "invalid_request"
        err.error_description = "The request is invalid"

        result = err.to_dict()
        assert result["error"] == "invalid_request"
        assert result["error_description"] == "The request is invalid"
        assert "request_id" not in result

    def test_to_dict_full(self):
        """Test to_dict with full data"""
        err = ErrResponse("invalid_request", "The request is invalid", "req-123")
        result = err.to_dict()
        assert result["error"] == "invalid_request"
        assert result["error_description"] == "The request is invalid"
        assert result["request_id"] == "req-123"

    def test_from_dict_oauth2_format(self):
        """Test from_dict with OAuth2 error format"""
        data = {"error": "invalid_request", "error_description": "The request is invalid", "request_id": "req-123"}

        err = ErrResponse.from_dict(data)
        assert err.error == "invalid_request"
        assert err.error_description == "The request is invalid"
        assert err.request_id == "req-123"

    def test_from_dict_aliyun_format(self):
        """Test from_dict with Aliyun error format"""
        data = {"Code": "InvalidParameter", "Message": "The parameter is invalid", "RequestId": "req-456"}

        err = ErrResponse.from_dict(data)
        assert err.error == "InvalidParameter"
        assert err.error_description == "The parameter is invalid"
        assert err.request_id == "req-456"

    def test_from_dict_mixed_format(self):
        """Test from_dict with mixed format (OAuth2 fields take precedence)"""
        data = {
            "error": "invalid_request",
            "Code": "InvalidParameter",
            "error_description": "The request is invalid",
            "Message": "The parameter is invalid",
            "request_id": "req-123",
            "RequestId": "req-456",
        }

        err = ErrResponse.from_dict(data)
        assert err.error == "invalid_request"
        assert err.error_description == "The request is invalid"
        assert err.request_id == "req-123"

    def test_from_dict_empty(self):
        """Test from_dict with empty data"""
        err = ErrResponse.from_dict({})
        assert err.error is None
        assert err.error_description is None
        assert err.request_id is None

    def test_repr(self):
        """Test __repr__ method"""
        err = ErrResponse("invalid_request", "The request is invalid", "req-123")
        repr_str = repr(err)
        assert "ErrResponse" in repr_str
        assert "invalid_request" in repr_str
        assert "The request is invalid" in repr_str
        assert "req-123" in repr_str

    def test_repr_empty(self):
        """Test __repr__ method with empty response"""
        err = ErrResponse()
        repr_str = repr(err)
        assert "ErrResponse" in repr_str
        assert "None" in repr_str

    def test_eq_equal(self):
        """Test __eq__ method with equal responses"""
        err1 = ErrResponse("invalid_request", "The request is invalid", "req-123")
        err2 = ErrResponse("invalid_request", "The request is invalid", "req-123")
        assert err1 == err2

    def test_eq_not_equal_error(self):
        """Test __eq__ method with different error"""
        err1 = ErrResponse("invalid_request", "The request is invalid", "req-123")
        err2 = ErrResponse("invalid_client", "Client is invalid", "req-123")
        assert err1 != err2

    def test_eq_not_equal_error_description(self):
        """Test __eq__ method with different error_description"""
        err1 = ErrResponse("invalid_request", "The request is invalid", "req-123")
        err2 = ErrResponse("invalid_request", "Different description", "req-123")
        assert err1 != err2

    def test_eq_not_equal_request_id(self):
        """Test __eq__ method with different request_id"""
        err1 = ErrResponse("invalid_request", "The request is invalid", "req-123")
        err2 = ErrResponse("invalid_request", "The request is invalid", "req-456")
        assert err1 != err2

    def test_eq_with_none_values(self):
        """Test __eq__ method with None values"""
        err1 = ErrResponse(None, None, None)
        err2 = ErrResponse(None, None, None)
        assert err1 == err2

    def test_eq_different_type(self):
        """Test __eq__ method with different type"""
        err = ErrResponse("invalid_request", "The request is invalid", "req-123")
        assert err != "invalid_request"
        assert err != 123
        assert err != None

    def test_hash_equal(self):
        """Test __hash__ method with equal responses"""
        err1 = ErrResponse("invalid_request", "The request is invalid", "req-123")
        err2 = ErrResponse("invalid_request", "The request is invalid", "req-123")
        assert hash(err1) == hash(err2)

    def test_hash_not_equal(self):
        """Test __hash__ method with different responses"""
        err1 = ErrResponse("invalid_request", "The request is invalid", "req-123")
        err2 = ErrResponse("invalid_client", "Client is invalid", "req-123")
        assert hash(err1) != hash(err2)

    def test_hash_consistent(self):
        """Test __hash__ method returns consistent hash"""
        err = ErrResponse("invalid_request", "The request is invalid", "req-123")
        hash1 = hash(err)
        hash2 = hash(err)
        assert hash1 == hash2

    def test_hash_with_none_values(self):
        """Test __hash__ method with None values"""
        err1 = ErrResponse(None, None, None)
        err2 = ErrResponse(None, None, None)
        assert hash(err1) == hash(err2)

    def test_can_use_in_set(self):
        """Test that ErrResponse can be used in a set"""
        err1 = ErrResponse("invalid_request", "The request is invalid", "req-123")
        err2 = ErrResponse("invalid_request", "The request is invalid", "req-123")
        err3 = ErrResponse("invalid_client", "Client is invalid", "req-123")

        err_set = {err1, err2, err3}
        assert len(err_set) == 2  # err1 and err2 are equal

    def test_can_use_as_dict_key(self):
        """Test that ErrResponse can be used as dict key"""
        err1 = ErrResponse("invalid_request", "The request is invalid", "req-123")
        err2 = ErrResponse("invalid_request", "The request is invalid", "req-123")
        err3 = ErrResponse("invalid_client", "Client is invalid", "req-123")

        err_dict = {}
        err_dict[err1] = "value1"
        err_dict[err2] = "value2"
        err_dict[err3] = "value3"

        assert len(err_dict) == 2  # err1 and err2 are the same key
        assert err_dict[err1] == "value2"  # value was overwritten
        assert err_dict[err3] == "value3"


class TestDeviceCodeResponse:
    """Test cases for DeviceCodeResponse"""

    def test_init_default(self):
        """Test default initialization"""
        response = DeviceCodeResponse()
        assert response._device_code is None
        assert response._user_code is None
        assert response._verification_uri is None
        assert response._verification_uri_complete is None
        assert response._expires_in is None
        assert response._expires_at is None
        assert response._interval is None

    def test_device_code_property(self):
        """Test device_code property getter and setter"""
        response = DeviceCodeResponse()
        assert response.device_code is None

        response.device_code = "device-123"
        assert response.device_code == "device-123"

    def test_user_code_property(self):
        """Test user_code property getter and setter"""
        response = DeviceCodeResponse()
        assert response.user_code is None

        response.user_code = "ABCD-1234"
        assert response.user_code == "ABCD-1234"

    def test_verification_uri_property(self):
        """Test verification_uri property getter and setter"""
        response = DeviceCodeResponse()
        assert response.verification_uri is None

        response.verification_uri = "https://example.com/verify"
        assert response.verification_uri == "https://example.com/verify"

    def test_verification_uri_complete_property(self):
        """Test verification_uri_complete property getter and setter"""
        response = DeviceCodeResponse()
        assert response.verification_uri_complete is None

        response.verification_uri_complete = "https://example.com/verify?code=ABCD-1234"
        assert response.verification_uri_complete == "https://example.com/verify?code=ABCD-1234"

    def test_expires_in_property(self):
        """Test expires_in property getter and setter"""
        response = DeviceCodeResponse()
        assert response.expires_in is None

        response.expires_in = 1800
        assert response.expires_in == 1800

    def test_expires_at_property(self):
        """Test expires_at property getter and setter"""
        response = DeviceCodeResponse()
        assert response.expires_at is None

        response.expires_at = 1234567890
        assert response.expires_at == 1234567890

    def test_interval_property(self):
        """Test interval property getter and setter"""
        response = DeviceCodeResponse()
        assert response.interval is None

        response.interval = 5
        assert response.interval == 5

    def test_to_dict_empty(self):
        """Test to_dict with empty response"""
        response = DeviceCodeResponse()
        result = response.to_dict()
        assert result == {}

    def test_to_dict_partial(self):
        """Test to_dict with partial data"""
        response = DeviceCodeResponse()
        response.device_code = "device-123"
        response.user_code = "ABCD-1234"

        result = response.to_dict()
        assert result["device_code"] == "device-123"
        assert result["user_code"] == "ABCD-1234"
        assert "verification_uri" not in result

    def test_to_dict_full(self):
        """Test to_dict with full data"""
        response = DeviceCodeResponse()
        response.device_code = "device-123"
        response.user_code = "ABCD-1234"
        response.verification_uri = "https://example.com/verify"
        response.verification_uri_complete = "https://example.com/verify?code=ABCD-1234"
        response.expires_in = 1800
        response.expires_at = 1234567890
        response.interval = 5

        result = response.to_dict()
        assert result["device_code"] == "device-123"
        assert result["user_code"] == "ABCD-1234"
        assert result["verification_uri"] == "https://example.com/verify"
        assert result["verification_uri_complete"] == "https://example.com/verify?code=ABCD-1234"
        assert result["expires_in"] == 1800
        assert result["expires_at"] == 1234567890
        assert result["interval"] == 5

    def test_from_dict_full(self):
        """Test from_dict with full data"""
        data = {
            "device_code": "device-123",
            "user_code": "ABCD-1234",
            "verification_uri": "https://example.com/verify",
            "verification_uri_complete": "https://example.com/verify?code=ABCD-1234",
            "expires_in": 1800,
            "expires_at": 1234567890,
            "interval": 5,
        }

        response = DeviceCodeResponse.from_dict(data)
        assert response.device_code == "device-123"
        assert response.user_code == "ABCD-1234"
        assert response.verification_uri == "https://example.com/verify"
        assert response.verification_uri_complete == "https://example.com/verify?code=ABCD-1234"
        assert response.expires_in == 1800
        assert response.expires_at == 1234567890
        assert response.interval == 5

    def test_from_dict_partial(self):
        """Test from_dict with partial data"""
        data = {"device_code": "device-123", "user_code": "ABCD-1234"}

        response = DeviceCodeResponse.from_dict(data)
        assert response.device_code == "device-123"
        assert response.user_code == "ABCD-1234"
        assert response.verification_uri is None
        assert response.expires_in is None

    def test_from_dict_empty(self):
        """Test from_dict with empty data"""
        response = DeviceCodeResponse.from_dict({})
        assert response.device_code is None
        assert response.user_code is None
        assert response.verification_uri is None
        assert response.expires_in is None
        assert response.expires_at is None
        assert response.interval is None

    def test_round_trip_dict_conversion(self):
        """Test round-trip conversion to/from dict"""
        original = DeviceCodeResponse()
        original.device_code = "device-123"
        original.user_code = "ABCD-1234"
        original.verification_uri = "https://example.com/verify"
        original.verification_uri_complete = "https://example.com/verify?code=ABCD-1234"
        original.expires_in = 1800
        original.expires_at = 1234567890
        original.interval = 5

        dict_data = original.to_dict()
        restored = DeviceCodeResponse.from_dict(dict_data)

        assert restored.device_code == original.device_code
        assert restored.user_code == original.user_code
        assert restored.verification_uri == original.verification_uri
        assert restored.verification_uri_complete == original.verification_uri_complete
        assert restored.expires_in == original.expires_in
        assert restored.expires_at == original.expires_at
        assert restored.interval == original.interval

    def test_repr(self):
        """Test __repr__ method"""
        response = DeviceCodeResponse()
        response.device_code = "device-123"
        response.user_code = "ABCD-1234"
        response.verification_uri = "https://example.com/verify"
        response.verification_uri_complete = "https://example.com/verify?code=ABCD-1234"
        response.expires_in = 1800
        response.expires_at = 1234567890
        response.interval = 5

        repr_str = repr(response)
        assert "DeviceCodeResponse" in repr_str
        assert "device-123" in repr_str
        assert "ABCD-1234" in repr_str
        assert "https://example.com/verify" in repr_str
        assert "1800" in repr_str
        assert "1234567890" in repr_str
        assert "5" in repr_str

    def test_repr_empty(self):
        """Test __repr__ method with empty response"""
        response = DeviceCodeResponse()
        repr_str = repr(response)
        assert "DeviceCodeResponse" in repr_str
        assert "None" in repr_str

    def test_eq_equal(self):
        """Test __eq__ method with equal responses"""
        response1 = DeviceCodeResponse()
        response1.device_code = "device-123"
        response1.user_code = "ABCD-1234"
        response1.verification_uri = "https://example.com/verify"
        response1.verification_uri_complete = "https://example.com/verify?code=ABCD-1234"
        response1.expires_in = 1800
        response1.expires_at = 1234567890
        response1.interval = 5

        response2 = DeviceCodeResponse()
        response2.device_code = "device-123"
        response2.user_code = "ABCD-1234"
        response2.verification_uri = "https://example.com/verify"
        response2.verification_uri_complete = "https://example.com/verify?code=ABCD-1234"
        response2.expires_in = 1800
        response2.expires_at = 1234567890
        response2.interval = 5

        assert response1 == response2

    def test_eq_not_equal_device_code(self):
        """Test __eq__ method with different device_code"""
        response1 = DeviceCodeResponse()
        response1.device_code = "device-123"
        response1.user_code = "ABCD-1234"
        response1.expires_in = 1800

        response2 = DeviceCodeResponse()
        response2.device_code = "device-456"
        response2.user_code = "ABCD-1234"
        response2.expires_in = 1800

        assert response1 != response2

    def test_eq_not_equal_user_code(self):
        """Test __eq__ method with different user_code"""
        response1 = DeviceCodeResponse()
        response1.device_code = "device-123"
        response1.user_code = "ABCD-1234"
        response1.expires_in = 1800

        response2 = DeviceCodeResponse()
        response2.device_code = "device-123"
        response2.user_code = "WXYZ-5678"
        response2.expires_in = 1800

        assert response1 != response2

    def test_eq_not_equal_verification_uri(self):
        """Test __eq__ method with different verification_uri"""
        response1 = DeviceCodeResponse()
        response1.device_code = "device-123"
        response1.verification_uri = "https://example.com/verify1"
        response1.expires_in = 1800

        response2 = DeviceCodeResponse()
        response2.device_code = "device-123"
        response2.verification_uri = "https://example.com/verify2"
        response2.expires_in = 1800

        assert response1 != response2

    def test_eq_not_equal_verification_uri_complete(self):
        """Test __eq__ method with different verification_uri_complete"""
        response1 = DeviceCodeResponse()
        response1.device_code = "device-123"
        response1.verification_uri_complete = "https://example.com/verify?code=ABCD-1234"
        response1.expires_in = 1800

        response2 = DeviceCodeResponse()
        response2.device_code = "device-123"
        response2.verification_uri_complete = "https://example.com/verify?code=WXYZ-5678"
        response2.expires_in = 1800

        assert response1 != response2

    def test_eq_not_equal_expires_in(self):
        """Test __eq__ method with different expires_in"""
        response1 = DeviceCodeResponse()
        response1.device_code = "device-123"
        response1.expires_in = 1800

        response2 = DeviceCodeResponse()
        response2.device_code = "device-123"
        response2.expires_in = 3600

        assert response1 != response2

    def test_eq_not_equal_expires_at(self):
        """Test __eq__ method with different expires_at"""
        response1 = DeviceCodeResponse()
        response1.device_code = "device-123"
        response1.expires_at = 1234567890

        response2 = DeviceCodeResponse()
        response2.device_code = "device-123"
        response2.expires_at = 1234567891

        assert response1 != response2

    def test_eq_not_equal_interval(self):
        """Test __eq__ method with different interval"""
        response1 = DeviceCodeResponse()
        response1.device_code = "device-123"
        response1.interval = 5

        response2 = DeviceCodeResponse()
        response2.device_code = "device-123"
        response2.interval = 10

        assert response1 != response2

    def test_eq_with_none_values(self):
        """Test __eq__ method with None values"""
        response1 = DeviceCodeResponse()
        response2 = DeviceCodeResponse()
        assert response1 == response2

    def test_eq_different_type(self):
        """Test __eq__ method with different type"""
        response = DeviceCodeResponse()
        response.device_code = "device-123"
        response.user_code = "ABCD-1234"

        assert response != "device-123"
        assert response != 123
        assert response != None

    def test_hash_equal(self):
        """Test __hash__ method with equal responses"""
        response1 = DeviceCodeResponse()
        response1.device_code = "device-123"
        response1.user_code = "ABCD-1234"
        response1.expires_in = 1800

        response2 = DeviceCodeResponse()
        response2.device_code = "device-123"
        response2.user_code = "ABCD-1234"
        response2.expires_in = 1800

        assert hash(response1) == hash(response2)

    def test_hash_not_equal(self):
        """Test __hash__ method with different responses"""
        response1 = DeviceCodeResponse()
        response1.device_code = "device-123"
        response1.user_code = "ABCD-1234"
        response1.expires_in = 1800

        response2 = DeviceCodeResponse()
        response2.device_code = "device-456"
        response2.user_code = "ABCD-1234"
        response2.expires_in = 1800

        assert hash(response1) != hash(response2)

    def test_hash_consistent(self):
        """Test __hash__ method returns consistent hash"""
        response = DeviceCodeResponse()
        response.device_code = "device-123"
        response.user_code = "ABCD-1234"
        response.expires_in = 1800

        hash1 = hash(response)
        hash2 = hash(response)
        assert hash1 == hash2

    def test_hash_with_none_values(self):
        """Test __hash__ method with None values"""
        response1 = DeviceCodeResponse()
        response2 = DeviceCodeResponse()
        assert hash(response1) == hash(response2)

    def test_can_use_in_set(self):
        """Test that DeviceCodeResponse can be used in a set"""
        response1 = DeviceCodeResponse()
        response1.device_code = "device-123"
        response1.user_code = "ABCD-1234"
        response1.expires_in = 1800

        response2 = DeviceCodeResponse()
        response2.device_code = "device-123"
        response2.user_code = "ABCD-1234"
        response2.expires_in = 1800

        response3 = DeviceCodeResponse()
        response3.device_code = "device-456"
        response3.user_code = "WXYZ-5678"
        response3.expires_in = 1800

        response_set = {response1, response2, response3}
        assert len(response_set) == 2  # response1 and response2 are equal

    def test_can_use_as_dict_key(self):
        """Test that DeviceCodeResponse can be used as dict key"""
        response1 = DeviceCodeResponse()
        response1.device_code = "device-123"
        response1.user_code = "ABCD-1234"
        response1.expires_in = 1800

        response2 = DeviceCodeResponse()
        response2.device_code = "device-123"
        response2.user_code = "ABCD-1234"
        response2.expires_in = 1800

        response3 = DeviceCodeResponse()
        response3.device_code = "device-456"
        response3.user_code = "WXYZ-5678"
        response3.expires_in = 1800

        response_dict = {}
        response_dict[response1] = "value1"
        response_dict[response2] = "value2"
        response_dict[response3] = "value3"

        assert len(response_dict) == 2  # response1 and response2 are the same key
        assert response_dict[response1] == "value2"  # value was overwritten
        assert response_dict[response3] == "value3"
