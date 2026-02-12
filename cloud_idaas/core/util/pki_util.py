"""
IDaaS Python SDK - PKI Utility

This module provides utilities for handling PEM format keys and PKI operations.
"""

import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class PkiUtil:
    """
    Utility class for PKI operations.
    """

    @staticmethod
    def parse_private_key_from_pem(pem_content: str):
        """
        Parse PEM format private key, supporting multiple formats of RSA and ECC private keys.

        Supported formats:
        1. -----BEGIN PRIVATE KEY----- (PKCS#8 generic format)
        2. -----BEGIN RSA PRIVATE KEY----- (PKCS#1 RSA format)
        3. -----BEGIN EC PRIVATE KEY----- (PKCS#8 ECC format)
        4. -----BEGIN DSA PRIVATE KEY----- (PKCS#8 DSA format)

        Args:
            pem_content: PEM formatted private key string.

        Returns:
            PrivateKey object.

        Raises:
            ValueError: If the PEM format is not supported.
        """
        pem_content = pem_content.strip()

        if pem_content.startswith("-----BEGIN RSA PRIVATE KEY-----"):
            # Process PKCS#1 RSA private key format
            return PkiUtil._parse_pkcs1_rsa_private_key(pem_content)
        elif pem_content.startswith("-----BEGIN EC PRIVATE KEY-----"):
            # Process PKCS#8 ECC private key format
            return PkiUtil._parse_pkcs8_ecc_private_key(pem_content)
        elif pem_content.startswith("-----BEGIN DSA PRIVATE KEY-----"):
            # Process PKCS#8 DSA private key format
            return PkiUtil._parse_pkcs8_dsa_private_key(pem_content)
        elif pem_content.startswith("-----BEGIN PRIVATE KEY-----"):
            # Handle standard PKCS#8 private key format
            return PkiUtil._parse_pkcs8_private_key(pem_content)
        else:
            raise ValueError("Unsupported private key PEM content.")

    @staticmethod
    def _parse_pkcs8_private_key(pem_content: str):
        """
        Parse standard PKCS#8 format private key.
        """
        private_key_pem = (
            pem_content.replace("-----BEGIN PRIVATE KEY-----", "")
            .replace("-----END PRIVATE KEY-----", "")
            .replace(" ", "")
            .replace("\n", "")
            .replace("\r", "")
        )

        encoded = base64.b64decode(private_key_pem)

        # Try different algorithms
        try:
            return serialization.load_der_private_key(encoded, password=None, backend=default_backend())
        except ValueError:
            # Try with RSA specifically
            try:
                return serialization.load_der_private_key(
                    PkiUtil._wrap_rsa_in_pkcs8(encoded), password=None, backend=default_backend()
                )
            except Exception:
                raise ValueError("Failed to parse PKCS#8 private key")

    @staticmethod
    def _parse_pkcs1_rsa_private_key(pem_content: str):
        """
        Parse PKCS#1 RSA private key format.
        """
        private_key_pem = (
            pem_content.replace("-----BEGIN RSA PRIVATE KEY-----", "")
            .replace("-----END RSA PRIVATE KEY-----", "")
            .replace(" ", "")
            .replace("\n", "")
            .replace("\r", "")
        )

        pkcs1_bytes = base64.b64decode(private_key_pem)

        # Convert PKCS#1 to PKCS#8
        pkcs8_bytes = PkiUtil._wrap_pkcs1_in_pkcs8(pkcs1_bytes, "RSA")

        return serialization.load_der_private_key(pkcs8_bytes, password=None, backend=default_backend())

    @staticmethod
    def _parse_pkcs8_ecc_private_key(pem_content: str):
        """
        Parse PKCS#8 ECC private key format.
        """
        private_key_pem = (
            pem_content.replace("-----BEGIN EC PRIVATE KEY-----", "")
            .replace("-----END EC PRIVATE KEY-----", "")
            .replace(" ", "")
            .replace("\n", "")
            .replace("\r", "")
        )

        encoded = base64.b64decode(private_key_pem)
        return serialization.load_der_private_key(encoded, password=None, backend=default_backend())

    @staticmethod
    def _parse_pkcs8_dsa_private_key(pem_content: str):
        """
        Parse PKCS#8 DSA private key format.
        """
        private_key_pem = (
            pem_content.replace("-----BEGIN DSA PRIVATE KEY-----", "")
            .replace("-----END DSA PRIVATE KEY-----", "")
            .replace(" ", "")
            .replace("\n", "")
            .replace("\r", "")
        )

        encoded = base64.b64decode(private_key_pem)
        return serialization.load_der_private_key(encoded, password=None, backend=default_backend())

    @staticmethod
    def _wrap_pkcs1_in_pkcs8(pkcs1_bytes: bytes, algorithm: str) -> bytes:
        """
        Wrap PKCS#1 format as PKCS#8 format.

        This is a simplified version for RSA keys.
        """
        # For RSA, we need to add the proper PKCS#8 wrapper
        # This is the OID for RSA encryption
        rsa_oid = bytes([0x30, 0x0D, 0x06, 0x09, 0x2A, 0x86, 0x48, 0x86, 0xF7, 0x0D, 0x01, 0x01, 0x01, 0x05, 0x00])

        # Build the PKCS#8 structure
        # SEQUENCE {
        #   INTEGER 0 (version)
        #   SEQUENCE { OID (rsaEncryption) NULL }
        #   OCTET STRING (the PKCS#1 key)
        # }
        total_length = len(pkcs1_bytes) + 26

        result = bytearray()
        # SEQUENCE tag and length
        result.extend([0x30, 0x82])
        result.extend([(total_length >> 8) & 0xFF, total_length & 0xFF])
        # Version INTEGER 0
        result.extend([0x02, 0x01, 0x00])
        # Algorithm identifier SEQUENCE
        result.extend([0x30, 0x0D])
        result.extend(rsa_oid)
        # OCTET STRING tag and length
        result.extend([0x04, 0x82])
        result.extend([(len(pkcs1_bytes) >> 8) & 0xFF, len(pkcs1_bytes) & 0xFF])
        # The PKCS#1 key data
        result.extend(pkcs1_bytes)

        return bytes(result)

    @staticmethod
    def _wrap_rsa_in_pkcs8(encoded: bytes) -> bytes:
        """
        Try to wrap raw key data in PKCS#8 format.
        """
        return PkiUtil._wrap_pkcs1_in_pkcs8(encoded, "RSA")
