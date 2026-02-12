"""
Unit tests for IDaaS Python SDK credential classes
"""

import time

from cloud_idaas import (
    IDaaSCredential,
    IDaaSTokenResponse,
)


class TestIDaaSCredential:
    """Test cases for IDaaSCredential interface"""

    def test_interface_methods_exist(self):
        """Verify that IDaaSCredential defines the required methods"""
        required_methods = ["get_access_token", "get_id_token", "get_refresh_token", "get_token_type"]
        for method in required_methods:
            assert hasattr(IDaaSCredential, method), f"IDaaSCredential should have {method} method"


class TestIDaaSTokenResponse:
    """Test cases for IDaaSTokenResponse"""

    def test_init_default(self):
        """Test default initialization"""
        token = IDaaSTokenResponse()
        assert token._access_token is None
        assert token._id_token is None
        assert token._refresh_token is None
        assert token._token_type is None
        assert token._expires_in == 0
        assert token._expires_at == 0

    def test_access_token_property(self):
        """Test access_token property getter and setter"""
        token = IDaaSTokenResponse()
        assert token.access_token is None
        assert token.get_access_token() is None

        token.access_token = "test_access_token"
        assert token.access_token == "test_access_token"
        assert token.get_access_token() == "test_access_token"

    def test_id_token_property(self):
        """Test id_token property getter and setter"""
        token = IDaaSTokenResponse()
        assert token.id_token is None
        assert token.get_id_token() is None

        token.id_token = "test_id_token"
        assert token.id_token == "test_id_token"
        assert token.get_id_token() == "test_id_token"

    def test_refresh_token_property(self):
        """Test refresh_token property getter and setter"""
        token = IDaaSTokenResponse()
        assert token.refresh_token is None
        assert token.get_refresh_token() is None

        token.refresh_token = "test_refresh_token"
        assert token.refresh_token == "test_refresh_token"
        assert token.get_refresh_token() == "test_refresh_token"

    def test_token_type_property(self):
        """Test token_type property getter and setter"""
        token = IDaaSTokenResponse()
        assert token.token_type is None
        assert token.get_token_type() is None

        token.token_type = "Bearer"
        assert token.token_type == "Bearer"
        assert token.get_token_type() == "Bearer"

    def test_expires_in_property(self):
        """Test expires_in property getter and setter"""
        token = IDaaSTokenResponse()
        assert token.expires_in == 0

        token.expires_in = 3600
        assert token.expires_in == 3600

    def test_expires_at_property(self):
        """Test expires_at property getter and setter"""
        token = IDaaSTokenResponse()
        assert token.expires_at == 0

        token.expires_at = 1234567890
        assert token.expires_at == 1234567890

    def test_will_soon_expire_not_expired(self):
        """Test will_soon_expire when token is not expired"""
        token = IDaaSTokenResponse()
        now = int(time.time())
        token.expires_in = 3600  # 1 hour
        token.expires_at = now + 3600

        assert not token.will_soon_expire()

    def test_will_soon_expire_expired(self):
        """Test will_soon_expire when token is about to expire"""
        token = IDaaSTokenResponse()
        now = int(time.time())
        token.expires_in = 3600  # 1 hour
        # Set expires_at such that only 10% of time remains
        token.expires_at = now + int(3600 * 0.1)

        assert token.will_soon_expire()

    def test_will_soon_expire_already_expired(self):
        """Test will_soon_expire when token is already expired"""
        token = IDaaSTokenResponse()
        now = int(time.time())
        token.expires_in = 3600
        token.expires_at = now - 100  # Expired 100 seconds ago

        assert token.will_soon_expire()

    def test_to_dict(self):
        """Test to_dict method"""
        token = IDaaSTokenResponse()
        token.access_token = "test_access_token"
        token.id_token = "test_id_token"
        token.refresh_token = "test_refresh_token"
        token.token_type = "Bearer"
        token.expires_in = 3600
        token.expires_at = 1234567890

        result = token.to_dict()
        assert result["access_token"] == "test_access_token"
        assert result["id_token"] == "test_id_token"
        assert result["refresh_token"] == "test_refresh_token"
        assert result["token_type"] == "Bearer"
        assert result["expires_in"] == 3600
        assert result["expires_at"] == 1234567890

    def test_from_dict(self):
        """Test from_dict class method"""
        data = {
            "access_token": "test_access_token",
            "id_token": "test_id_token",
            "refresh_token": "test_refresh_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "expires_at": 1234567890,
        }

        token = IDaaSTokenResponse.from_dict(data)
        assert token.access_token == "test_access_token"
        assert token.id_token == "test_id_token"
        assert token.refresh_token == "test_refresh_token"
        assert token.token_type == "Bearer"
        assert token.expires_in == 3600
        assert token.expires_at == 1234567890

    def test_from_dict_partial_data(self):
        """Test from_dict with partial data"""
        data = {
            "access_token": "test_access_token",
            "token_type": "Bearer",
        }

        token = IDaaSTokenResponse.from_dict(data)
        assert token.access_token == "test_access_token"
        assert token.token_type == "Bearer"
        assert token.id_token is None
        assert token.refresh_token is None
        assert token.expires_in == 0
        assert token.expires_at == 0

    def test_round_trip_dict_conversion(self):
        """Test round-trip conversion to/from dict"""
        original = IDaaSTokenResponse()
        original.access_token = "test_access_token"
        original.id_token = "test_id_token"
        original.refresh_token = "test_refresh_token"
        original.token_type = "Bearer"
        original.expires_in = 3600
        original.expires_at = 1234567890

        dict_data = original.to_dict()
        restored = IDaaSTokenResponse.from_dict(dict_data)

        assert restored.access_token == original.access_token
        assert restored.id_token == original.id_token
        assert restored.refresh_token == original.refresh_token
        assert restored.token_type == original.token_type
        assert restored.expires_in == original.expires_in
        assert restored.expires_at == original.expires_at

    def test_repr(self):
        """Test __repr__ method"""
        token = IDaaSTokenResponse()
        token.access_token = "test_access_token"
        token.id_token = "test_id_token"
        token.refresh_token = "test_refresh_token"
        token.token_type = "Bearer"
        token.expires_in = 3600
        token.expires_at = 1234567890

        repr_str = repr(token)
        assert "IDaaSTokenResponse" in repr_str
        assert "test_access_token" in repr_str
        assert "test_id_token" in repr_str
        assert "test_refresh_token" in repr_str
        assert "Bearer" in repr_str
        assert "3600" in repr_str
        assert "1234567890" in repr_str

    def test_repr_empty(self):
        """Test __repr__ method with empty token"""
        token = IDaaSTokenResponse()
        repr_str = repr(token)
        assert "IDaaSTokenResponse" in repr_str
        assert "None" in repr_str

    def test_eq_equal(self):
        """Test __eq__ method with equal tokens"""
        token1 = IDaaSTokenResponse()
        token1.access_token = "test_access_token"
        token1.id_token = "test_id_token"
        token1.refresh_token = "test_refresh_token"
        token1.token_type = "Bearer"
        token1.expires_in = 3600
        token1.expires_at = 1234567890

        token2 = IDaaSTokenResponse()
        token2.access_token = "test_access_token"
        token2.id_token = "test_id_token"
        token2.refresh_token = "test_refresh_token"
        token2.token_type = "Bearer"
        token2.expires_in = 3600
        token2.expires_at = 1234567890

        assert token1 == token2

    def test_eq_not_equal_access_token(self):
        """Test __eq__ method with different access_token"""
        token1 = IDaaSTokenResponse()
        token1.access_token = "token1"
        token1.token_type = "Bearer"
        token1.expires_in = 3600
        token1.expires_at = 1234567890

        token2 = IDaaSTokenResponse()
        token2.access_token = "token2"
        token2.token_type = "Bearer"
        token2.expires_in = 3600
        token2.expires_at = 1234567890

        assert token1 != token2

    def test_eq_not_equal_id_token(self):
        """Test __eq__ method with different id_token"""
        token1 = IDaaSTokenResponse()
        token1.access_token = "test_access_token"
        token1.id_token = "id1"
        token1.token_type = "Bearer"
        token1.expires_in = 3600
        token1.expires_at = 1234567890

        token2 = IDaaSTokenResponse()
        token2.access_token = "test_access_token"
        token2.id_token = "id2"
        token2.token_type = "Bearer"
        token2.expires_in = 3600
        token2.expires_at = 1234567890

        assert token1 != token2

    def test_eq_not_equal_refresh_token(self):
        """Test __eq__ method with different refresh_token"""
        token1 = IDaaSTokenResponse()
        token1.access_token = "test_access_token"
        token1.refresh_token = "refresh1"
        token1.token_type = "Bearer"
        token1.expires_in = 3600
        token1.expires_at = 1234567890

        token2 = IDaaSTokenResponse()
        token2.access_token = "test_access_token"
        token2.refresh_token = "refresh2"
        token2.token_type = "Bearer"
        token2.expires_in = 3600
        token2.expires_at = 1234567890

        assert token1 != token2

    def test_eq_not_equal_token_type(self):
        """Test __eq__ method with different token_type"""
        token1 = IDaaSTokenResponse()
        token1.access_token = "test_access_token"
        token1.token_type = "Bearer"
        token1.expires_in = 3600
        token1.expires_at = 1234567890

        token2 = IDaaSTokenResponse()
        token2.access_token = "test_access_token"
        token2.token_type = "Basic"
        token2.expires_in = 3600
        token2.expires_at = 1234567890

        assert token1 != token2

    def test_eq_not_equal_expires_in(self):
        """Test __eq__ method with different expires_in"""
        token1 = IDaaSTokenResponse()
        token1.access_token = "test_access_token"
        token1.token_type = "Bearer"
        token1.expires_in = 3600
        token1.expires_at = 1234567890

        token2 = IDaaSTokenResponse()
        token2.access_token = "test_access_token"
        token2.token_type = "Bearer"
        token2.expires_in = 7200
        token2.expires_at = 1234567890

        assert token1 != token2

    def test_eq_not_equal_expires_at(self):
        """Test __eq__ method with different expires_at"""
        token1 = IDaaSTokenResponse()
        token1.access_token = "test_access_token"
        token1.token_type = "Bearer"
        token1.expires_in = 3600
        token1.expires_at = 1234567890

        token2 = IDaaSTokenResponse()
        token2.access_token = "test_access_token"
        token2.token_type = "Bearer"
        token2.expires_in = 3600
        token2.expires_at = 1234567891

        assert token1 != token2

    def test_eq_different_type(self):
        """Test __eq__ method with different type"""
        token = IDaaSTokenResponse()
        token.access_token = "test_access_token"
        token.token_type = "Bearer"
        token.expires_in = 3600
        token.expires_at = 1234567890

        assert token != "test_access_token"
        assert token != 123
        assert token != None

    def test_hash_equal(self):
        """Test __hash__ method with equal tokens"""
        token1 = IDaaSTokenResponse()
        token1.access_token = "test_access_token"
        token1.id_token = "test_id_token"
        token1.refresh_token = "test_refresh_token"
        token1.token_type = "Bearer"
        token1.expires_in = 3600
        token1.expires_at = 1234567890

        token2 = IDaaSTokenResponse()
        token2.access_token = "test_access_token"
        token2.id_token = "test_id_token"
        token2.refresh_token = "test_refresh_token"
        token2.token_type = "Bearer"
        token2.expires_in = 3600
        token2.expires_at = 1234567890

        assert hash(token1) == hash(token2)

    def test_hash_not_equal(self):
        """Test __hash__ method with different tokens"""
        token1 = IDaaSTokenResponse()
        token1.access_token = "token1"
        token1.token_type = "Bearer"
        token1.expires_in = 3600
        token1.expires_at = 1234567890

        token2 = IDaaSTokenResponse()
        token2.access_token = "token2"
        token2.token_type = "Bearer"
        token2.expires_in = 3600
        token2.expires_at = 1234567890

        assert hash(token1) != hash(token2)

    def test_hash_consistent(self):
        """Test __hash__ method returns consistent hash"""
        token = IDaaSTokenResponse()
        token.access_token = "test_access_token"
        token.token_type = "Bearer"
        token.expires_in = 3600
        token.expires_at = 1234567890

        hash1 = hash(token)
        hash2 = hash(token)
        assert hash1 == hash2

    def test_hash_with_none_values(self):
        """Test __hash__ method with None values"""
        token1 = IDaaSTokenResponse()
        token1.access_token = None
        token1.id_token = None
        token1.refresh_token = None
        token1.token_type = None
        token1.expires_in = 0
        token1.expires_at = 0

        token2 = IDaaSTokenResponse()
        token2.access_token = None
        token2.id_token = None
        token2.refresh_token = None
        token2.token_type = None
        token2.expires_in = 0
        token2.expires_at = 0

        assert hash(token1) == hash(token2)

    def test_can_use_in_set(self):
        """Test that IDaaSTokenResponse can be used in a set"""
        token1 = IDaaSTokenResponse()
        token1.access_token = "test_access_token"
        token1.token_type = "Bearer"
        token1.expires_in = 3600
        token1.expires_at = 1234567890

        token2 = IDaaSTokenResponse()
        token2.access_token = "test_access_token"
        token2.token_type = "Bearer"
        token2.expires_in = 3600
        token2.expires_at = 1234567890

        token3 = IDaaSTokenResponse()
        token3.access_token = "different_token"
        token3.token_type = "Bearer"
        token3.expires_in = 3600
        token3.expires_at = 1234567890

        token_set = {token1, token2, token3}
        assert len(token_set) == 2  # token1 and token2 are equal

    def test_can_use_as_dict_key(self):
        """Test that IDaaSTokenResponse can be used as dict key"""
        token1 = IDaaSTokenResponse()
        token1.access_token = "test_access_token"
        token1.token_type = "Bearer"
        token1.expires_in = 3600
        token1.expires_at = 1234567890

        token2 = IDaaSTokenResponse()
        token2.access_token = "test_access_token"
        token2.token_type = "Bearer"
        token2.expires_in = 3600
        token2.expires_at = 1234567890

        token_dict = {}
        token_dict[token1] = "value1"
        token_dict[token2] = "value2"

        assert len(token_dict) == 1  # token1 and token2 are the same key
        assert token_dict[token1] == "value2"  # value was overwritten
