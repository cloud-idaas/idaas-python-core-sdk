"""
Test script to verify IDaaSClientConfig.from_dict method works correctly.
"""

from cloud_idaas.core.config.idaas_client_config import IDaaSClientConfig

# Sample configuration data
sample_config = {
    "idaas_instance_id": "test-instance-id",
    "client_id": "test-client-id",
    "scope": "test-scope",
    "issuer": "https://test-issuer.example.com",
    "token_endpoint": "https://test-token.example.com/token",
    "device_authorization_endpoint": "https://test-device-auth.example.com/device",
    "developer_api_endpoint": "https://test-api.example.com",
    "authn_configuration": {
        "identity_type": "CLIENT",
        "authn_method": "CLIENT_SECRET_POST",
        "client_secret_env_var_name": "TEST_CLIENT_SECRET",
        "private_key_env_var_name": "TEST_PRIVATE_KEY",
    },
    "http_configuration": {"connect_timeout": 10000, "read_timeout": 20000, "unsafe_ignore_ssl_cert": True},
}


def test_from_dict():
    print("Testing IDaaSClientConfig.from_dict method...")

    # Convert dict to IDaaSClientConfig
    config = IDaaSClientConfig.from_dict(sample_config)

    # Verify basic properties
    assert config.idaas_instance_id == "test-instance-id", (
        f"Expected 'test-instance-id', got {config.idaas_instance_id}"
    )
    assert config.client_id == "test-client-id", f"Expected 'test-client-id', got {config.client_id}"
    assert config.scope == "test-scope", f"Expected 'test-scope', got {config.scope}"
    assert config.issuer == "https://test-issuer.example.com", (
        f"Expected 'https://test-issuer.example.com', got {config.issuer}"
    )
    assert config.token_endpoint == "https://test-token.example.com/token", (
        f"Expected 'https://test-token.example.com/token', got {config.token_endpoint}"
    )

    # Verify nested authn_configuration
    authn_config = config.authn_configuration
    assert authn_config is not None, "authn_configuration should not be None"
    assert authn_config.identity_type.value == "CLIENT", f"Expected 'CLIENT', got {authn_config.identity_type}"
    assert authn_config.authn_method.value == "CLIENT_SECRET_POST", (
        f"Expected 'CLIENT_SECRET_POST', got {authn_config.authn_method}"
    )
    assert authn_config.client_secret_env_var_name == "TEST_CLIENT_SECRET", (
        f"Expected 'TEST_CLIENT_SECRET', got {authn_config.client_secret_env_var_name}"
    )

    # Verify nested http_configuration
    http_config = config.http_configuration
    assert http_config is not None, "http_configuration should not be None"
    assert http_config.connect_timeout == 10000, f"Expected 10000, got {http_config.connect_timeout}"
    assert http_config.read_timeout == 20000, f"Expected 20000, got {http_config.read_timeout}"
    assert http_config.unsafe_ignore_ssl_cert is True, f"Expected True, got {http_config.unsafe_ignore_ssl_cert}"

    print("✓ All assertions passed!")
    print(f"IDaaS Instance ID: {config.idaas_instance_id}")
    print(f"Client ID: {config.client_id}")
    print(f"Authn Method: {config.authn_configuration.authn_method}")
    print(f"Connect Timeout: {config.http_configuration.connect_timeout}")


if __name__ == "__main__":
    test_from_dict()
    print("\n✅ IDaaSClientConfig.from_dict method works correctly!")
