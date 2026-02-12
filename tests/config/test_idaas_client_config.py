"""
Tests for IDaaSClientConfig class
"""

import unittest

from cloud_idaas.core.config.http_configuration import HttpConfiguration
from cloud_idaas.core.config.idaas_client_config import IDaaSClientConfig
from cloud_idaas.core.config.identity_authentication_configuration import (
    ClientDeployEnvironmentEnum,
    IdentityAuthenticationConfiguration,
    TokenAuthnMethod,
)


class TestIDaaSClientConfig(unittest.TestCase):
    """Test cases for IDaaSClientConfig class"""

    def test_default_values(self):
        """Test default values"""
        config = IDaaSClientConfig()
        self.assertIsNone(config.idaas_instance_id)
        self.assertIsNone(config.client_id)
        self.assertEqual(config.scope, "urn:cloud:idaas:pam|cloud_account:obtain_access_credential")
        self.assertIsNone(config.issuer)
        self.assertIsNone(config.token_endpoint)
        self.assertIsNone(config.device_authorization_endpoint)
        self.assertIsNone(config.developer_api_endpoint)
        self.assertIsInstance(config.http_configuration, HttpConfiguration)

    def test_set_properties(self):
        """Test setting properties"""
        config = IDaaSClientConfig()
        config.idaas_instance_id = "test-instance"
        config.client_id = "test-client"
        config.scope = "test-scope"
        config.issuer = "https://example.com"
        config.token_endpoint = "https://example.com/token"
        config.device_authorization_endpoint = "https://example.com/device"
        config.developer_api_endpoint = "https://example.com/api"

        self.assertEqual(config.idaas_instance_id, "test-instance")
        self.assertEqual(config.client_id, "test-client")
        self.assertEqual(config.scope, "test-scope")
        self.assertEqual(config.issuer, "https://example.com")
        self.assertEqual(config.token_endpoint, "https://example.com/token")
        self.assertEqual(config.device_authorization_endpoint, "https://example.com/device")
        self.assertEqual(config.developer_api_endpoint, "https://example.com/api")

    def test_from_dict_with_all_fields(self):
        """Test from_dict with all fields"""
        data = {
            "idaasInstanceId": "test-instance",
            "clientId": "test-client",
            "scope": "test-scope",
            "issuer": "https://example.com",
            "tokenEndpoint": "https://example.com/token",
            "deviceAuthorizationEndpoint": "https://example.com/device",
            "developerApiEndpoint": "https://example.com/api",
            "authnConfiguration": {
                "clientDeployEnvironment": "KUBERNETES",
                "authnMethod": "CLIENT_SECRET_BASIC",
            },
            "httpConfiguration": {
                "connectTimeout": 3000,
                "readTimeout": 5000,
                "unsafeIgnoreSslCert": True,
            },
        }

        config = IDaaSClientConfig.from_dict(data)
        self.assertEqual(config.idaas_instance_id, "test-instance")
        self.assertEqual(config.client_id, "test-client")
        self.assertEqual(config.scope, "test-scope")
        self.assertEqual(config.issuer, "https://example.com")
        self.assertEqual(config.token_endpoint, "https://example.com/token")
        self.assertEqual(config.device_authorization_endpoint, "https://example.com/device")
        self.assertEqual(config.developer_api_endpoint, "https://example.com/api")
        self.assertIsNotNone(config.authn_configuration)
        self.assertEqual(config.authn_configuration.client_deploy_environment, ClientDeployEnvironmentEnum.KUBERNETES)
        self.assertEqual(config.authn_configuration.authn_method, TokenAuthnMethod.CLIENT_SECRET_BASIC)
        self.assertEqual(config.http_configuration.connect_timeout, 3000)
        self.assertEqual(config.http_configuration.read_timeout, 5000)
        self.assertTrue(config.http_configuration.unsafe_ignore_ssl_cert)

    def test_from_dict_with_snake_case(self):
        """Test from_dict with snake_case keys"""
        data = {
            "idaas_instance_id": "test-instance",
            "client_id": "test-client",
            "scope": "test-scope",
        }

        config = IDaaSClientConfig.from_dict(data)
        self.assertEqual(config.idaas_instance_id, "test-instance")
        self.assertEqual(config.client_id, "test-client")
        self.assertEqual(config.scope, "test-scope")

    def test_from_dict_empty(self):
        """Test from_dict with empty data"""
        config = IDaaSClientConfig.from_dict({})
        self.assertIsNone(config.idaas_instance_id)
        self.assertIsNone(config.client_id)
        self.assertEqual(config.scope, "urn:cloud:idaas:pam|cloud_account:obtain_access_credential")

    def test_from_dict_none(self):
        """Test from_dict with None"""
        config = IDaaSClientConfig.from_dict(None)
        self.assertIsNone(config.idaas_instance_id)
        self.assertIsNone(config.client_id)

    def test_assign(self):
        """Test assign method"""
        source = IDaaSClientConfig()
        source.idaas_instance_id = "test-instance"
        source.client_id = "test-client"
        source.scope = "test-scope"

        target = IDaaSClientConfig()
        target.assign(source)

        self.assertEqual(target.idaas_instance_id, "test-instance")
        self.assertEqual(target.client_id, "test-client")
        self.assertEqual(target.scope, "test-scope")

    def test_assign_none(self):
        """Test assign method with None"""
        target = IDaaSClientConfig()
        target.idaas_instance_id = "test-instance"
        target.assign(None)
        self.assertEqual(target.idaas_instance_id, "test-instance")

    def test_assign_with_authn_configuration(self):
        """Test assign method with authn_configuration"""
        source = IDaaSClientConfig()
        source.authn_configuration = IdentityAuthenticationConfiguration()
        source.authn_configuration.client_deploy_environment = ClientDeployEnvironmentEnum.KUBERNETES

        target = IDaaSClientConfig()
        target.assign(source)

        self.assertIsNotNone(target.authn_configuration)
        self.assertEqual(target.authn_configuration.client_deploy_environment, ClientDeployEnvironmentEnum.KUBERNETES)
        self.assertIsNot(source.authn_configuration, target.authn_configuration)

    def test_assign_with_http_configuration(self):
        """Test assign method with http_configuration"""
        source = IDaaSClientConfig()
        source.http_configuration.connect_timeout = 3000

        target = IDaaSClientConfig()
        target.assign(source)

        self.assertEqual(target.http_configuration.connect_timeout, 3000)
        self.assertIsNot(source.http_configuration, target.http_configuration)

    def test_repr(self):
        """Test __repr__ method"""
        config = IDaaSClientConfig()
        config.idaas_instance_id = "test-instance"
        config.client_id = "test-client"
        config.issuer = "https://example.com"

        repr_str = repr(config)
        self.assertIn("IDaaSClientConfig", repr_str)
        self.assertIn("test-instance", repr_str)
        self.assertIn("test-client", repr_str)
        self.assertIn("https://example.com", repr_str)

    def test_repr_empty(self):
        """Test __repr__ method with empty config"""
        config = IDaaSClientConfig()
        repr_str = repr(config)
        self.assertIn("IDaaSClientConfig", repr_str)

    def test_eq_equal(self):
        """Test __eq__ method with equal configs"""
        config1 = IDaaSClientConfig()
        config1.idaas_instance_id = "test-instance"
        config1.client_id = "test-client"
        config1.scope = "test-scope"

        config2 = IDaaSClientConfig()
        config2.idaas_instance_id = "test-instance"
        config2.client_id = "test-client"
        config2.scope = "test-scope"

        self.assertEqual(config1, config2)

    def test_eq_not_equal_idaas_instance_id(self):
        """Test __eq__ method with different idaas_instance_id"""
        config1 = IDaaSClientConfig()
        config1.idaas_instance_id = "instance1"
        config1.client_id = "test-client"

        config2 = IDaaSClientConfig()
        config2.idaas_instance_id = "instance2"
        config2.client_id = "test-client"

        self.assertNotEqual(config1, config2)

    def test_eq_not_equal_client_id(self):
        """Test __eq__ method with different client_id"""
        config1 = IDaaSClientConfig()
        config1.idaas_instance_id = "test-instance"
        config1.client_id = "client1"

        config2 = IDaaSClientConfig()
        config2.idaas_instance_id = "test-instance"
        config2.client_id = "client2"

        self.assertNotEqual(config1, config2)

    def test_eq_with_nested_config(self):
        """Test __eq__ method with nested configs"""
        config1 = IDaaSClientConfig()
        config1.idaas_instance_id = "test-instance"
        config1.client_id = "test-client"
        config1.http_configuration.connect_timeout = 3000

        config2 = IDaaSClientConfig()
        config2.idaas_instance_id = "test-instance"
        config2.client_id = "test-client"
        config2.http_configuration.connect_timeout = 3000

        self.assertEqual(config1, config2)

    def test_eq_not_equal_nested_config(self):
        """Test __eq__ method with different nested configs"""
        config1 = IDaaSClientConfig()
        config1.idaas_instance_id = "test-instance"
        config1.client_id = "test-client"
        config1.http_configuration.connect_timeout = 3000

        config2 = IDaaSClientConfig()
        config2.idaas_instance_id = "test-instance"
        config2.client_id = "test-client"
        config2.http_configuration.connect_timeout = 5000

        self.assertNotEqual(config1, config2)

    def test_eq_with_none_values(self):
        """Test __eq__ method with None values"""
        config1 = IDaaSClientConfig()
        config2 = IDaaSClientConfig()
        self.assertEqual(config1, config2)

    def test_eq_different_type(self):
        """Test __eq__ method with different type"""
        config = IDaaSClientConfig()
        self.assertNotEqual(config, "config")
        self.assertNotEqual(config, 123)
        self.assertNotEqual(config, None)

    def test_hash_equal(self):
        """Test __hash__ method with equal configs"""
        config1 = IDaaSClientConfig()
        config1.idaas_instance_id = "test-instance"
        config1.client_id = "test-client"
        config1.scope = "test-scope"

        config2 = IDaaSClientConfig()
        config2.idaas_instance_id = "test-instance"
        config2.client_id = "test-client"
        config2.scope = "test-scope"

        self.assertEqual(hash(config1), hash(config2))

    def test_hash_not_equal(self):
        """Test __hash__ method with different configs"""
        config1 = IDaaSClientConfig()
        config1.idaas_instance_id = "instance1"
        config1.client_id = "test-client"

        config2 = IDaaSClientConfig()
        config2.idaas_instance_id = "instance2"
        config2.client_id = "test-client"

        self.assertNotEqual(hash(config1), hash(config2))

    def test_hash_consistent(self):
        """Test __hash__ method returns consistent hash"""
        config = IDaaSClientConfig()
        config.idaas_instance_id = "test-instance"
        config.client_id = "test-client"

        hash1 = hash(config)
        hash2 = hash(config)
        self.assertEqual(hash1, hash2)

    def test_hash_with_none_values(self):
        """Test __hash__ method with None values"""
        config1 = IDaaSClientConfig()
        config2 = IDaaSClientConfig()
        self.assertEqual(hash(config1), hash(config2))

    def test_can_use_in_set(self):
        """Test that IDaaSClientConfig can be used in a set"""
        config1 = IDaaSClientConfig()
        config1.idaas_instance_id = "test-instance"
        config1.client_id = "test-client"

        config2 = IDaaSClientConfig()
        config2.idaas_instance_id = "test-instance"
        config2.client_id = "test-client"

        config3 = IDaaSClientConfig()
        config3.idaas_instance_id = "instance2"
        config3.client_id = "test-client"

        config_set = {config1, config2, config3}
        self.assertEqual(len(config_set), 2)  # config1 and config2 are equal


if __name__ == "__main__":
    unittest.main()
