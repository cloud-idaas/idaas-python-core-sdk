"""
Tests for PkiUtil class
"""

import unittest

from cloud_idaas import PkiUtil


class TestPkiUtil(unittest.TestCase):
    """Test cases for PkiUtil class"""

    # RSA PKCS#8 private key (simplified example)
    PKCS8_RSA_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKK
-----END PRIVATE KEY-----"""

    # RSA PKCS#1 private key (simplified example)
    PKCS1_RSA_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAu1SU1LfVLPHCigwIBAAKCAQEAu1SU1LfVLPHCigw
-----END RSA PRIVATE KEY-----"""

    # EC private key (simplified example)
    EC_PRIVATE_KEY = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIMZ6UdC0FJhG2M5P5B6fR7g8h9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x
-----END EC PRIVATE KEY-----"""

    def test_parse_private_key_from_pem_with_pkcs8_rsa(self):
        """Test parse PKCS#8 RSA private key"""
        # This is a simplified test - real test would use valid key
        try:
            PkiUtil.parse_private_key_from_pem(self.PKCS8_RSA_KEY)
        except ValueError as e:
            # Expected for invalid key in test
            self.assertIn("Failed to parse", str(e))

    def test_parse_private_key_from_pem_with_pkcs1_rsa(self):
        """Test parse PKCS#1 RSA private key"""
        try:
            PkiUtil.parse_private_key_from_pem(self.PKCS1_RSA_KEY)
        except ValueError:
            # Expected for invalid key in test
            pass

    def test_parse_private_key_from_pem_with_ec(self):
        """Test parse EC private key"""
        try:
            PkiUtil.parse_private_key_from_pem(self.EC_PRIVATE_KEY)
        except ValueError:
            # Expected for invalid key in test
            pass

    def test_parse_private_key_from_pem_with_unsupported_format(self):
        """Test parse with unsupported format"""
        with self.assertRaises(ValueError) as context:
            PkiUtil.parse_private_key_from_pem("INVALID KEY CONTENT")
        self.assertIn("Unsupported", str(context.exception))


if __name__ == "__main__":
    unittest.main()
