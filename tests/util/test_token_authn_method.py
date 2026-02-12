"""
Tests for TokenAuthnMethod enum
"""

import unittest

from cloud_idaas.core.util import TokenAuthnMethod


class TestTokenAuthnMethod(unittest.TestCase):
    """Test cases for TokenAuthnMethod enum"""

    def test_none_value(self):
        """Test NONE value"""
        self.assertEqual(TokenAuthnMethod.NONE.value, "NONE")

    def test_client_secret_post_value(self):
        """Test CLIENT_SECRET_POST value"""
        self.assertEqual(TokenAuthnMethod.CLIENT_SECRET_POST.value, "CLIENT_SECRET_POST")

    def test_client_secret_basic_value(self):
        """Test CLIENT_SECRET_BASIC value"""
        self.assertEqual(TokenAuthnMethod.CLIENT_SECRET_BASIC.value, "CLIENT_SECRET_BASIC")

    def test_client_secret_jwt_value(self):
        """Test CLIENT_SECRET_JWT value"""
        self.assertEqual(TokenAuthnMethod.CLIENT_SECRET_JWT.value, "CLIENT_SECRET_JWT")

    def test_private_key_jwt_value(self):
        """Test PRIVATE_KEY_JWT value"""
        self.assertEqual(TokenAuthnMethod.PRIVATE_KEY_JWT.value, "PRIVATE_KEY_JWT")

    def test_pkcs7_value(self):
        """Test PKCS7 value"""
        self.assertEqual(TokenAuthnMethod.PKCS7.value, "PKCS7")

    def test_pca_value(self):
        """Test PCA value"""
        self.assertEqual(TokenAuthnMethod.PCA.value, "PCA")

    def test_oidc_value(self):
        """Test OIDC value"""
        self.assertEqual(TokenAuthnMethod.OIDC.value, "OIDC")

    def test_equals_with_none_values(self):
        """Test equals with both None values"""
        self.assertTrue(TokenAuthnMethod.equals(None, None))

    def test_equals_with_one_none(self):
        """Test equals with one None value"""
        self.assertFalse(TokenAuthnMethod.equals("test", None))
        self.assertFalse(TokenAuthnMethod.equals(None, "test"))

    def test_equals_with_same_strings(self):
        """Test equals with same strings"""
        self.assertTrue(TokenAuthnMethod.equals("test", "test"))

    def test_equals_with_different_strings(self):
        """Test equals with different strings"""
        self.assertFalse(TokenAuthnMethod.equals("test", "other"))


if __name__ == "__main__":
    unittest.main()
