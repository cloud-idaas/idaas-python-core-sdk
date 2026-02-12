"""
Tests for IDaaSCredentialProviderFactory class
"""

import unittest

from cloud_idaas import ConfigException, HttpConfiguration, IDaaSClientConfig, IdentityAuthenticationConfiguration
from cloud_idaas.core import AuthenticationIdentityEnum, ErrorCode, TokenAuthnMethod
from cloud_idaas.core.factory.idaas_credential_provider_factory import IDaaSCredentialProviderFactory


class TestIDaaSCredentialProviderFactory(unittest.TestCase):
    """Test cases for IDaaSCredentialProviderFactory class"""

    def setUp(self):
        """Set up test fixtures"""
        IDaaSCredentialProviderFactory.reset()

    def tearDown(self):
        """Clean up test fixtures"""
        IDaaSCredentialProviderFactory.reset()

    def test_factory_not_initialized(self):
        """Test factory throws exception when not initialized"""
        with self.assertRaises(ConfigException) as context:
            IDaaSCredentialProviderFactory.get_idaas_credential_provider()
        self.assertEqual(context.exception.error_code, ErrorCode.IDAAS_CREDENTIAL_PROVIDER_FACTORY_NOT_INIT)

    def test_init_with_config(self):
        """Test initialization with configuration"""
        config = IDaaSClientConfig()
        config.idaas_instance_id = "test-instance"
        config.client_id = "test-client"
        config.issuer = "https://example.com"
        config.token_endpoint = "https://example.com/token"
        config.developer_api_endpoint = "https://example.com/api"

        authn_config = IdentityAuthenticationConfiguration()
        authn_config.identity_type = AuthenticationIdentityEnum.CLIENT
        authn_config.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC
        authn_config.client_secret_env_var_name = "TEST_SECRET"
        config.authn_configuration = authn_config

        # This should not raise an exception
        IDaaSCredentialProviderFactory.init_with_config(config)
        self.assertTrue(IDaaSCredentialProviderFactory._initialized)

    def test_reset(self):
        """Test factory reset"""
        config = IDaaSClientConfig()
        config.idaas_instance_id = "test-instance"
        config.client_id = "test-client"
        config.issuer = "https://example.com"
        config.token_endpoint = "https://example.com/token"
        config.developer_api_endpoint = "https://example.com/api"

        authn_config = IdentityAuthenticationConfiguration()
        authn_config.identity_type = AuthenticationIdentityEnum.CLIENT
        authn_config.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC
        authn_config.client_secret_env_var_name = "TEST_SECRET"
        config.authn_configuration = authn_config

        IDaaSCredentialProviderFactory.init_with_config(config)
        self.assertTrue(IDaaSCredentialProviderFactory._initialized)

        IDaaSCredentialProviderFactory.reset()
        self.assertFalse(IDaaSCredentialProviderFactory._initialized)

    def test_get_idaas_instance_id_after_init(self):
        """Test get_idaas_instance_id after initialization"""
        config = IDaaSClientConfig()
        config.idaas_instance_id = "test-instance"
        config.client_id = "test-client"
        config.issuer = "https://example.com"
        config.token_endpoint = "https://example.com/token"
        config.developer_api_endpoint = "https://example.com/api"

        authn_config = IdentityAuthenticationConfiguration()
        authn_config.identity_type = AuthenticationIdentityEnum.CLIENT
        authn_config.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC
        authn_config.client_secret_env_var_name = "TEST_SECRET"
        config.authn_configuration = authn_config

        IDaaSCredentialProviderFactory.init_with_config(config)
        self.assertEqual(IDaaSCredentialProviderFactory.get_idaas_instance_id(), "test-instance")

    def test_get_developer_api_endpoint_after_init(self):
        """Test get_developer_api_endpoint after initialization"""
        config = IDaaSClientConfig()
        config.idaas_instance_id = "test-instance"
        config.client_id = "test-client"
        config.issuer = "https://example.com"
        config.token_endpoint = "https://example.com/token"
        config.developer_api_endpoint = "https://example.com/api"

        authn_config = IdentityAuthenticationConfiguration()
        authn_config.identity_type = AuthenticationIdentityEnum.CLIENT
        authn_config.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC
        authn_config.client_secret_env_var_name = "TEST_SECRET"
        config.authn_configuration = authn_config

        IDaaSCredentialProviderFactory.init_with_config(config)
        self.assertEqual(IDaaSCredentialProviderFactory.get_developer_api_endpoint(), "https://example.com/api")

    def test_get_http_config_after_init(self):
        """Test get_http_config after initialization"""
        config = IDaaSClientConfig()
        config.idaas_instance_id = "test-instance"
        config.client_id = "test-client"
        config.issuer = "https://example.com"
        config.token_endpoint = "https://example.com/token"
        config.developer_api_endpoint = "https://example.com/api"
        config.http_configuration = HttpConfiguration()

        authn_config = IdentityAuthenticationConfiguration()
        authn_config.identity_type = AuthenticationIdentityEnum.CLIENT
        authn_config.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC
        authn_config.client_secret_env_var_name = "TEST_SECRET"
        config.authn_configuration = authn_config

        IDaaSCredentialProviderFactory.init_with_config(config)
        http_config = IDaaSCredentialProviderFactory.get_http_config()
        self.assertIsNotNone(http_config)
        self.assertEqual(http_config.connect_timeout, 5000)


if __name__ == "__main__":
    unittest.main()
