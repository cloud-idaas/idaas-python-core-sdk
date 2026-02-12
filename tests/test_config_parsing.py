"""
Test script for verifying config parsing with camelCase keys.
"""

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cloud_idaas import StringUtil
from cloud_idaas.core.config.idaas_client_config import IDaaSClientConfig


def test_camel_to_snake_conversion():
    """Test camelCase to snake_case conversion."""
    print("Testing camelCase to snake_case conversion...")
    test_cases = [
        ("idaasInstanceId", "idaas_instance_id"),
        ("clientId", "client_id"),
        ("tokenEndpoint", "token_endpoint"),
        ("clientSecretEnvVarName", "client_secret_env_var_name"),
        ("connectTimeout", "connect_timeout"),
        ("unsafeIgnoreSslCert", "unsafe_ignore_ssl_cert"),
    ]

    for camel, expected_snake in test_cases:
        result = StringUtil.camel_to_snake(camel)
        assert result == expected_snake, f"Failed: {camel} -> {result}, expected {expected_snake}"
        print(f"  {camel} -> {result}")

    print("  All camelCase to snake_case tests passed!\n")


def test_idaas_client_config_from_dict():
    """Test IDaaSClientConfig parsing from camelCase dictionary."""
    print("Testing IDaaSClientConfig.from_dict with camelCase keys...")

    config_data = {
        "idaasInstanceId": "idaas_xzzcg5t3eip7e7uf4tnobb7jm4",
        "clientId": "app_nfznxxhyvf2l7qhx752e6pcbze",
        "issuer": "https://nr3ks4cn.dev.aliyunidaas.com/api/v2/iauths_system/oauth2",
        "tokenEndpoint": "https://nr3ks4cn.dev.aliyunidaas.com/api/v2/iauths_system/oauth2/token",
        "scope": "urn:cloud:idaas:pam|cloud_account_role:obtain_access_credential",
        "developerApiEndpoint": "eiam-developerapi.cn-hangzhou.aliyuncs.com",
        "authnConfiguration": {
            "authenticationSubject": "CLIENT",
            "authnMethod": "CLIENT_SECRET_POST",
            "clientSecretEnvVarName": "IDAAS_CLIENT_SECRET",
        },
        "httpConfiguration": {"connectTimeout": 5000, "readTimeout": 10000, "unsafeIgnoreSslCert": False},
    }

    config = IDaaSClientConfig.from_dict(config_data)

    assert config.idaas_instance_id == "idaas_xzzcg5t3eip7e7uf4tnobb7jm4", "Failed: idaas_instance_id"
    assert config.client_id == "app_nfznxxhyvf2l7qhx752e6pcbze", "Failed: client_id"
    assert config.issuer == "https://nr3ks4cn.dev.aliyunidaas.com/api/v2/iauths_system/oauth2", "Failed: issuer"
    assert config.token_endpoint == "https://nr3ks4cn.dev.aliyunidaas.com/api/v2/iauths_system/oauth2/token", (
        "Failed: token_endpoint"
    )
    assert config.scope == "urn:cloud:idaas:pam|cloud_account_role:obtain_access_credential", "Failed: scope"
    assert config.developer_api_endpoint == "eiam-developerapi.cn-hangzhou.aliyuncs.com", (
        "Failed: developer_api_endpoint"
    )

    # Check authn configuration
    assert config.authn_configuration is not None, "Failed: authn_configuration is None"
    assert config.authn_configuration.identity_type.value == "CLIENT", "Failed: identity_type"
    assert config.authn_configuration.authn_method.value == "CLIENT_SECRET_POST", "Failed: authn_method"
    assert config.authn_configuration.client_secret_env_var_name == "IDAAS_CLIENT_SECRET", (
        "Failed: client_secret_env_var_name"
    )

    # Check http configuration
    assert config.http_configuration is not None, "Failed: http_configuration is None"
    assert config.http_configuration.connect_timeout == 5000, "Failed: connect_timeout"
    assert config.http_configuration.read_timeout == 10000, "Failed: read_timeout"
    assert config.http_configuration.unsafe_ignore_ssl_cert == False, "Failed: unsafe_ignore_ssl_cert"

    print("  All IDaaSClientConfig parsing tests passed!\n")


def test_snake_case_compatibility():
    """Test that snake_case keys still work."""
    print("Testing backward compatibility with snake_case keys...")

    config_data = {
        "idaas_instance_id": "idaas_test123",
        "client_id": "app_test123",
        "issuer": "https://test.example.com/oauth2",
        "token_endpoint": "https://test.example.com/token",
        "scope": "test_scope",
        "developer_api_endpoint": "api.example.com",
    }

    config = IDaaSClientConfig.from_dict(config_data)

    assert config.idaas_instance_id == "idaas_test123", "Failed: idaas_instance_id"
    assert config.client_id == "app_test123", "Failed: client_id"
    assert config.issuer == "https://test.example.com/oauth2", "Failed: issuer"
    assert config.token_endpoint == "https://test.example.com/token", "Failed: token_endpoint"
    assert config.scope == "test_scope", "Failed: scope"
    assert config.developer_api_endpoint == "api.example.com", "Failed: developer_api_endpoint"

    print("  All snake_case compatibility tests passed!\n")


def test_mixed_case_keys():
    """Test that mixed camelCase and snake_case keys work."""
    print("Testing mixed camelCase and snake_case keys...")

    config_data = {
        "idaasInstanceId": "idaas_mixed123",
        "client_id": "app_mixed123",
        "issuer": "https://mixed.example.com/oauth2",
        "token_endpoint": "https://mixed.example.com/token",
    }

    config = IDaaSClientConfig.from_dict(config_data)

    assert config.idaas_instance_id == "idaas_mixed123", "Failed: idaas_instance_id"
    assert config.client_id == "app_mixed123", "Failed: client_id"
    assert config.issuer == "https://mixed.example.com/oauth2", "Failed: issuer"
    assert config.token_endpoint == "https://mixed.example.com/token", "Failed: token_endpoint"

    print("  All mixed case keys tests passed!\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Running IDaaS SDK Config Parsing Tests")
    print("=" * 60)
    print()

    try:
        test_camel_to_snake_conversion()
        test_idaas_client_config_from_dict()
        test_snake_case_compatibility()
        test_mixed_case_keys()

        print("=" * 60)
        print("All tests passed successfully!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
