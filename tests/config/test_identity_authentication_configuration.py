"""
Tests for IdentityAuthenticationConfiguration class
"""

import unittest

from cloud_idaas.core.config.identity_authentication_configuration import IdentityAuthenticationConfiguration
from cloud_idaas.core.constants import AuthenticationIdentityEnum, ClientDeployEnvironmentEnum, TokenAuthnMethod


class TestIdentityAuthenticationConfiguration(unittest.TestCase):
    """Test cases for IdentityAuthenticationConfiguration class"""

    def test_default_values(self):
        """Test default values"""
        config = IdentityAuthenticationConfiguration()
        self.assertEqual(config.identity_type, AuthenticationIdentityEnum.CLIENT)
        self.assertEqual(config.authn_method, TokenAuthnMethod.NONE)
        self.assertIsNone(config.client_deploy_environment)

    def test_set_client_deploy_environment(self):
        """Test setting client_deploy_environment"""
        config = IdentityAuthenticationConfiguration()
        config.client_deploy_environment = ClientDeployEnvironmentEnum.KUBERNETES
        self.assertEqual(config.client_deploy_environment, ClientDeployEnvironmentEnum.KUBERNETES)

    def test_set_authn_method(self):
        """Test setting authn_method"""
        config = IdentityAuthenticationConfiguration()
        config.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC
        self.assertEqual(config.authn_method, TokenAuthnMethod.CLIENT_SECRET_BASIC)

    def test_from_dict_with_all_fields(self):
        """Test from_dict with all fields"""
        data = {
            "clientDeployEnvironment": "KUBERNETES",
            "authnMethod": "CLIENT_SECRET_BASIC",
            "clientSecretEnvVarName": "MY_SECRET",
            "privateKeyEnvVarName": "MY_KEY",
            "applicationFederatedCredentialName": "my-credential",
            "client_x509_certificate": "cert-data",  # Use snake_case directly
            "x509_cert_chains": "chain-data",  # Use snake_case directly
        }

        config = IdentityAuthenticationConfiguration.from_dict(data)
        self.assertEqual(config.client_deploy_environment, ClientDeployEnvironmentEnum.KUBERNETES)
        self.assertEqual(config.authn_method, TokenAuthnMethod.CLIENT_SECRET_BASIC)
        self.assertEqual(config.client_secret_env_var_name, "MY_SECRET")
        self.assertEqual(config.private_key_env_var_name, "MY_KEY")
        self.assertEqual(config.application_federated_credential_name, "my-credential")
        self.assertEqual(config.client_x509_certificate, "cert-data")
        self.assertEqual(config.x509_cert_chains, "chain-data")

    def test_from_dict_with_snake_case(self):
        """Test from_dict with snake_case keys"""
        data = {
            "client_deploy_environment": "KUBERNETES",
            "authn_method": "CLIENT_SECRET_BASIC",
            "client_secret_env_var_name": "MY_SECRET",
        }

        config = IdentityAuthenticationConfiguration.from_dict(data)
        self.assertEqual(config.client_deploy_environment, ClientDeployEnvironmentEnum.KUBERNETES)
        self.assertEqual(config.authn_method, TokenAuthnMethod.CLIENT_SECRET_BASIC)
        self.assertEqual(config.client_secret_env_var_name, "MY_SECRET")

    def test_from_dict_empty(self):
        """Test from_dict with empty data"""
        config = IdentityAuthenticationConfiguration.from_dict({})
        self.assertEqual(config.authn_method, TokenAuthnMethod.NONE)
        self.assertIsNone(config.client_deploy_environment)

    def test_copy(self):
        """Test copy method"""
        source = IdentityAuthenticationConfiguration()
        source.client_deploy_environment = ClientDeployEnvironmentEnum.KUBERNETES
        source.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC
        source.client_secret_env_var_name = "MY_SECRET"

        target = IdentityAuthenticationConfiguration.copy(source)
        self.assertEqual(target.client_deploy_environment, ClientDeployEnvironmentEnum.KUBERNETES)
        self.assertEqual(target.authn_method, TokenAuthnMethod.CLIENT_SECRET_BASIC)
        self.assertEqual(target.client_secret_env_var_name, "MY_SECRET")

    def test_copy_none(self):
        """Test copy method with None"""
        result = IdentityAuthenticationConfiguration.copy(None)
        self.assertIsNone(result)

    def test_copy_creates_new_instance(self):
        """Test that copy creates a new instance"""
        source = IdentityAuthenticationConfiguration()
        target = IdentityAuthenticationConfiguration.copy(source)
        self.assertIsNot(source, target)

    def test_repr(self):
        """Test __repr__ method"""
        config = IdentityAuthenticationConfiguration()
        config.client_deploy_environment = ClientDeployEnvironmentEnum.KUBERNETES
        config.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC
        config.client_secret_env_var_name = "MY_SECRET"

        repr_str = repr(config)
        self.assertIn("IdentityAuthenticationConfiguration", repr_str)
        self.assertIn("KUBERNETES", repr_str)
        self.assertIn("CLIENT_SECRET_BASIC", repr_str)

    def test_repr_empty(self):
        """Test __repr__ method with empty config"""
        config = IdentityAuthenticationConfiguration()
        repr_str = repr(config)
        self.assertIn("IdentityAuthenticationConfiguration", repr_str)

    def test_eq_equal(self):
        """Test __eq__ method with equal configs"""
        config1 = IdentityAuthenticationConfiguration()
        config1.client_deploy_environment = ClientDeployEnvironmentEnum.KUBERNETES
        config1.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC

        config2 = IdentityAuthenticationConfiguration()
        config2.client_deploy_environment = ClientDeployEnvironmentEnum.KUBERNETES
        config2.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC

        self.assertEqual(config1, config2)

    def test_eq_not_equal_client_deploy_environment(self):
        """Test __eq__ method with different client_deploy_environment"""
        config1 = IdentityAuthenticationConfiguration()
        config1.client_deploy_environment = ClientDeployEnvironmentEnum.KUBERNETES

        config2 = IdentityAuthenticationConfiguration()
        config2.client_deploy_environment = ClientDeployEnvironmentEnum.AWS_EC2

        self.assertNotEqual(config1, config2)

    def test_eq_not_equal_authn_method(self):
        """Test __eq__ method with different authn_method"""
        config1 = IdentityAuthenticationConfiguration()
        config1.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC

        config2 = IdentityAuthenticationConfiguration()
        config2.authn_method = TokenAuthnMethod.CLIENT_SECRET_POST

        self.assertNotEqual(config1, config2)

    def test_eq_with_none_values(self):
        """Test __eq__ method with None values"""
        config1 = IdentityAuthenticationConfiguration()
        config2 = IdentityAuthenticationConfiguration()
        self.assertEqual(config1, config2)

    def test_eq_different_type(self):
        """Test __eq__ method with different type"""
        config = IdentityAuthenticationConfiguration()
        self.assertNotEqual(config, "config")
        self.assertNotEqual(config, 123)
        self.assertNotEqual(config, None)

    def test_hash_equal(self):
        """Test __hash__ method with equal configs"""
        config1 = IdentityAuthenticationConfiguration()
        config1.client_deploy_environment = ClientDeployEnvironmentEnum.KUBERNETES
        config1.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC

        config2 = IdentityAuthenticationConfiguration()
        config2.client_deploy_environment = ClientDeployEnvironmentEnum.KUBERNETES
        config2.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC

        self.assertEqual(hash(config1), hash(config2))

    def test_hash_not_equal(self):
        """Test __hash__ method with different configs"""
        config1 = IdentityAuthenticationConfiguration()
        config1.client_deploy_environment = ClientDeployEnvironmentEnum.KUBERNETES

        config2 = IdentityAuthenticationConfiguration()
        config2.client_deploy_environment = ClientDeployEnvironmentEnum.AWS_EC2

        self.assertNotEqual(hash(config1), hash(config2))

    def test_hash_consistent(self):
        """Test __hash__ method returns consistent hash"""
        config = IdentityAuthenticationConfiguration()
        config.client_deploy_environment = ClientDeployEnvironmentEnum.KUBERNETES
        config.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC

        hash1 = hash(config)
        hash2 = hash(config)
        self.assertEqual(hash1, hash2)

    def test_hash_with_none_values(self):
        """Test __hash__ method with None values"""
        config1 = IdentityAuthenticationConfiguration()
        config2 = IdentityAuthenticationConfiguration()
        self.assertEqual(hash(config1), hash(config2))

    def test_can_use_in_set(self):
        """Test that IdentityAuthenticationConfiguration can be used in a set"""
        config1 = IdentityAuthenticationConfiguration()
        config1.client_deploy_environment = ClientDeployEnvironmentEnum.KUBERNETES
        config1.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC

        config2 = IdentityAuthenticationConfiguration()
        config2.client_deploy_environment = ClientDeployEnvironmentEnum.KUBERNETES
        config2.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC

        config3 = IdentityAuthenticationConfiguration()
        config3.client_deploy_environment = ClientDeployEnvironmentEnum.AWS_EC2

        config_set = {config1, config2, config3}
        self.assertEqual(len(config_set), 2)  # config1 and config2 are equal


if __name__ == "__main__":
    unittest.main()
