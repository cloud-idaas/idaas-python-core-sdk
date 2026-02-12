"""
Unit tests for IDaaSCredentialProviderFactory class
"""

import os
import unittest
from unittest.mock import Mock, patch

from cloud_idaas import ConfigException, HttpConfiguration, IDaaSClientConfig, IdentityAuthenticationConfiguration
from cloud_idaas.core import AuthenticationIdentityEnum, ErrorCode, TokenAuthnMethod
from cloud_idaas.core.factory.idaas_credential_provider_factory import IDaaSCredentialProviderFactory
from cloud_idaas.core.provider import IDaaSCredentialProvider


class MockCredentialProvider(IDaaSCredentialProvider):
    """Mock implementation of IDaaSCredentialProvider for testing."""

    def get_credential(self):
        pass


class TestIDaaSCredentialProviderFactory(unittest.TestCase):
    """Test cases for IDaaSCredentialProviderFactory class"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        IDaaSCredentialProviderFactory.reset()

    def tearDown(self):
        """Clean up after each test method."""
        IDaaSCredentialProviderFactory.reset()

    def test_init_when_already_initialized(self):
        """Test init method when factory is already initialized."""
        # First initialization
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

        # Second initialization should just log and return
        with patch(
            "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._logger"
        ) as mock_logger:
            IDaaSCredentialProviderFactory.init()
            mock_logger.info.assert_called_once()

    @patch("cloud_idaas.core.factory.idaas_credential_provider_factory.ConfigReader")
    @patch("cloud_idaas.core.factory.idaas_credential_provider_factory.JSONUtil")
    @patch(
        "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._validate_client_config"
    )
    @patch(
        "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._validate_http_config"
    )
    @patch(
        "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._init_credential_provider"
    )
    def test_init_success(
        self, mock_init_credential, mock_validate_http, mock_validate_client, mock_json_util, mock_config_reader
    ):
        """Test init method with successful configuration loading."""
        mock_config_reader.get_config_as_string.return_value = '{"idaas_instance_id": "test", "client_id": "client"}'
        mock_json_util.parse_object.return_value = IDaaSClientConfig()

        # Mock the validation methods
        mock_validate_client.return_value = None
        mock_validate_http.return_value = None

        IDaaSCredentialProviderFactory.init()

        mock_config_reader.get_config_as_string.assert_called_once()
        mock_json_util.parse_object.assert_called_once()
        self.assertTrue(IDaaSCredentialProviderFactory._initialized)

    @patch("cloud_idaas.core.factory.idaas_credential_provider_factory.ConfigReader")
    @patch(
        "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._init_credential_provider"
    )
    def test_init_failure_raises_config_exception(self, mock_init_credential, mock_config_reader):
        """Test init method raises ConfigException when initialization fails."""
        mock_config_reader.get_config_as_string.side_effect = Exception("Config load failed")

        with self.assertRaises(ConfigException) as context:
            IDaaSCredentialProviderFactory.init()

        self.assertEqual(context.exception.error_code, ErrorCode.IDAAS_CREDENTIAL_PROVIDER_FACTORY_NOT_INIT)

    @patch("cloud_idaas.core.factory.idaas_credential_provider_factory.ConfigReader")
    @patch("cloud_idaas.core.factory.idaas_credential_provider_factory.JSONUtil")
    @patch(
        "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._validate_client_config"
    )
    @patch(
        "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._validate_http_config"
    )
    @patch(
        "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._init_credential_provider"
    )
    def test_init_with_custom_config_path(
        self, mock_init_credential, mock_validate_http, mock_validate_client, mock_json_util, mock_config_reader
    ):
        """Test init method with custom config path parameter."""
        custom_path = "/custom/path/to/config.json"
        mock_config_reader.get_config_as_string.return_value = '{"idaas_instance_id": "test", "client_id": "client"}'
        mock_json_util.parse_object.return_value = IDaaSClientConfig()

        # Mock the validation methods
        mock_validate_client.return_value = None
        mock_validate_http.return_value = None

        IDaaSCredentialProviderFactory.init(config_path=custom_path)

        # Verify that get_config_as_string was called with the custom path
        mock_config_reader.get_config_as_string.assert_called_once_with(custom_path)
        mock_json_util.parse_object.assert_called_once()
        self.assertTrue(IDaaSCredentialProviderFactory._initialized)

    def test_init_with_config_success(self):
        """Test init_with_config method with valid configuration."""
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

        with patch(
            "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._validate_client_config"
        ):
            IDaaSCredentialProviderFactory.init_with_config(config)

        self.assertTrue(IDaaSCredentialProviderFactory._initialized)

    def test_init_with_config_when_already_initialized(self):
        """Test init_with_config method when already initialized."""
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

        # First initialization
        with patch(
            "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._validate_client_config"
        ):
            IDaaSCredentialProviderFactory.init_with_config(config)

        # Second initialization should just log and return
        with patch(
            "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._logger"
        ) as mock_logger:
            IDaaSCredentialProviderFactory.init_with_config(config)
            mock_logger.info.assert_called_once()

    def test_get_idaas_credential_provider_before_init_raises_exception(self):
        """Test get_idaas_credential_provider raises exception when factory not initialized."""
        with self.assertRaises(ConfigException) as context:
            IDaaSCredentialProviderFactory.get_idaas_credential_provider()

        self.assertEqual(context.exception.error_code, ErrorCode.IDAAS_CREDENTIAL_PROVIDER_FACTORY_NOT_INIT)

    def test_get_idaas_credential_provider_by_scope_before_init_raises_exception(self):
        """Test get_idaas_credential_provider_by_scope raises exception when factory not initialized."""
        with self.assertRaises(ConfigException) as context:
            IDaaSCredentialProviderFactory.get_idaas_credential_provider_by_scope("test-scope")

        self.assertEqual(context.exception.error_code, ErrorCode.IDAAS_CREDENTIAL_PROVIDER_FACTORY_NOT_INIT)

    def test_get_developer_api_endpoint_before_init_raises_exception(self):
        """Test get_developer_api_endpoint raises exception when factory not initialized."""
        with self.assertRaises(ConfigException) as context:
            IDaaSCredentialProviderFactory.get_developer_api_endpoint()

        self.assertEqual(context.exception.error_code, ErrorCode.IDAAS_CREDENTIAL_PROVIDER_FACTORY_NOT_INIT)

    def test_get_idaas_instance_id_before_init_raises_exception(self):
        """Test get_idaas_instance_id raises exception when factory not initialized."""
        with self.assertRaises(ConfigException) as context:
            IDaaSCredentialProviderFactory.get_idaas_instance_id()

        self.assertEqual(context.exception.error_code, ErrorCode.IDAAS_CREDENTIAL_PROVIDER_FACTORY_NOT_INIT)

    def test_get_http_config_before_init_raises_exception(self):
        """Test get_http_config raises exception when factory not initialized."""
        with self.assertRaises(ConfigException) as context:
            IDaaSCredentialProviderFactory.get_http_config()

        self.assertEqual(context.exception.error_code, ErrorCode.IDAAS_CREDENTIAL_PROVIDER_FACTORY_NOT_INIT)

    def test_reset_clears_state(self):
        """Test reset method clears the factory state."""
        # Set up some state
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

        with patch(
            "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._validate_client_config"
        ):
            IDaaSCredentialProviderFactory.init_with_config(config)

        # Add a credential provider to the cache
        IDaaSCredentialProviderFactory._credential_providers["test-scope"] = MockCredentialProvider()

        # Reset the factory
        IDaaSCredentialProviderFactory.reset()

        self.assertFalse(IDaaSCredentialProviderFactory._initialized)
        self.assertEqual(len(IDaaSCredentialProviderFactory._credential_providers), 0)

    def test_get_idaas_credential_provider_after_init(self):
        """Test get_idaas_credential_provider returns credential provider after initialization."""
        config = IDaaSClientConfig()
        config.idaas_instance_id = "test-instance"
        config.client_id = "test-client"
        config.issuer = "https://example.com"
        config.token_endpoint = "https://example.com/token"
        config.developer_api_endpoint = "https://example.com/api"
        config.scope = "test-scope"

        authn_config = IdentityAuthenticationConfiguration()
        authn_config.identity_type = AuthenticationIdentityEnum.CLIENT
        authn_config.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC
        authn_config.client_secret_env_var_name = "TEST_SECRET"
        config.authn_configuration = authn_config

        with patch(
            "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._validate_client_config"
        ):
            IDaaSCredentialProviderFactory.init_with_config(config)

        # Mock the credential provider creation
        with patch(
            "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._create_credential_provider"
        ) as mock_create:
            mock_provider = Mock()
            mock_create.return_value = mock_provider

            provider = IDaaSCredentialProviderFactory.get_idaas_credential_provider()

            self.assertEqual(provider, mock_provider)
            mock_create.assert_called_once_with("test-scope")

    def test_get_idaas_credential_provider_by_scope_after_init(self):
        """Test get_idaas_credential_provider_by_scope returns credential provider after initialization."""
        config = IDaaSClientConfig()
        config.idaas_instance_id = "test-instance"
        config.client_id = "test-client"
        config.issuer = "https://example.com"
        config.token_endpoint = "https://example.com/token"
        config.developer_api_endpoint = "https://example.com/api"
        config.scope = "default-scope"

        authn_config = IdentityAuthenticationConfiguration()
        authn_config.identity_type = AuthenticationIdentityEnum.CLIENT
        authn_config.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC
        authn_config.client_secret_env_var_name = "TEST_SECRET"
        config.authn_configuration = authn_config

        with patch(
            "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._validate_client_config"
        ):
            IDaaSCredentialProviderFactory.init_with_config(config)

        # Mock the credential provider creation
        with patch(
            "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._create_credential_provider"
        ) as mock_create:
            mock_provider = Mock()
            mock_create.return_value = mock_provider

            provider = IDaaSCredentialProviderFactory.get_idaas_credential_provider_by_scope("test-scope")

            self.assertEqual(provider, mock_provider)
            mock_create.assert_called_once_with("test-scope")

    def test_get_developer_api_endpoint_after_init(self):
        """Test get_developer_api_endpoint returns correct value after initialization."""
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

        with patch(
            "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._validate_client_config"
        ):
            IDaaSCredentialProviderFactory.init_with_config(config)

        endpoint = IDaaSCredentialProviderFactory.get_developer_api_endpoint()

        self.assertEqual(endpoint, "https://example.com/api")

    def test_get_idaas_instance_id_after_init(self):
        """Test get_idaas_instance_id returns correct value after initialization."""
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

        with patch(
            "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._validate_client_config"
        ):
            IDaaSCredentialProviderFactory.init_with_config(config)

        instance_id = IDaaSCredentialProviderFactory.get_idaas_instance_id()

        self.assertEqual(instance_id, "test-instance")

    def test_get_http_config_after_init(self):
        """Test get_http_config returns correct value after initialization."""
        config = IDaaSClientConfig()
        config.idaas_instance_id = "test-instance"
        config.client_id = "test-client"
        config.issuer = "https://example.com"
        config.token_endpoint = "https://example.com/token"
        config.developer_api_endpoint = "https://example.com/api"
        http_config = HttpConfiguration()
        http_config.connect_timeout = 10000
        config.http_configuration = http_config

        authn_config = IdentityAuthenticationConfiguration()
        authn_config.identity_type = AuthenticationIdentityEnum.CLIENT
        authn_config.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC
        authn_config.client_secret_env_var_name = "TEST_SECRET"
        config.authn_configuration = authn_config

        with patch(
            "cloud_idaas.core.factory.idaas_credential_provider_factory.IDaaSCredentialProviderFactory._validate_client_config"
        ):
            IDaaSCredentialProviderFactory.init_with_config(config)

        returned_http_config = IDaaSCredentialProviderFactory.get_http_config()

        self.assertEqual(returned_http_config.connect_timeout, 10000)

    @patch("cloud_idaas.core.implementation.idaas_machine_credential_provider.IDaaSMachineCredentialProviderBuilder")
    def test_create_credential_provider_client_secret_basic(self, mock_builder_class):
        """Test _create_credential_provider with CLIENT_SECRET_BASIC method."""
        # Setup configuration
        config = IDaaSClientConfig()
        config.client_id = "test-client"
        config.token_endpoint = "https://example.com/token"

        authn_config = IdentityAuthenticationConfiguration()
        authn_config.authn_method = TokenAuthnMethod.CLIENT_SECRET_BASIC
        authn_config.client_secret_env_var_name = "TEST_CLIENT_SECRET"
        config.authn_configuration = authn_config

        # Mock environment variable
        with patch.dict(os.environ, {"TEST_CLIENT_SECRET": "secret-value"}):
            # Replace the factory's config with our test config
            IDaaSCredentialProviderFactory._idaas_client_config = config
            IDaaSCredentialProviderFactory._initialized = True

            mock_builder = Mock()
            mock_builder_class.return_value = mock_builder
            mock_builder.client_id.return_value = mock_builder
            mock_builder.scope.return_value = mock_builder
            mock_builder.token_endpoint.return_value = mock_builder
            mock_builder.authn_method.return_value = mock_builder
            mock_builder.client_secret_supplier.return_value = mock_builder
            mock_builder.build.return_value = Mock()

            provider = IDaaSCredentialProviderFactory._create_credential_provider("test-scope")

            # Verify the builder was called with correct parameters
            mock_builder_class.assert_called_once()
            mock_builder.client_id.assert_called_once_with("test-client")
            mock_builder.scope.assert_called_once_with("test-scope")
            mock_builder.token_endpoint.assert_called_once_with("https://example.com/token")
            mock_builder.authn_method.assert_called_once_with(TokenAuthnMethod.CLIENT_SECRET_BASIC)
            mock_builder.client_secret_supplier.assert_called_once()
            mock_builder.build.assert_called_once()

    @patch("cloud_idaas.core.implementation.idaas_machine_credential_provider.IDaaSMachineCredentialProviderBuilder")
    def test_create_credential_provider_client_secret_post(self, mock_builder_class):
        """Test _create_credential_provider with CLIENT_SECRET_POST method."""
        # Setup configuration
        config = IDaaSClientConfig()
        config.client_id = "test-client"
        config.token_endpoint = "https://example.com/token"

        authn_config = IdentityAuthenticationConfiguration()
        authn_config.authn_method = TokenAuthnMethod.CLIENT_SECRET_POST
        authn_config.client_secret_env_var_name = "TEST_CLIENT_SECRET"
        config.authn_configuration = authn_config

        # Mock environment variable
        with patch.dict(os.environ, {"TEST_CLIENT_SECRET": "secret-value"}):
            # Replace the factory's config with our test config
            IDaaSCredentialProviderFactory._idaas_client_config = config
            IDaaSCredentialProviderFactory._initialized = True

            mock_builder = Mock()
            mock_builder_class.return_value = mock_builder
            mock_builder.client_id.return_value = mock_builder
            mock_builder.scope.return_value = mock_builder
            mock_builder.token_endpoint.return_value = mock_builder
            mock_builder.authn_method.return_value = mock_builder
            mock_builder.client_secret_supplier.return_value = mock_builder
            mock_builder.build.return_value = Mock()

            provider = IDaaSCredentialProviderFactory._create_credential_provider("test-scope")

            # Verify the builder was called with correct parameters
            mock_builder_class.assert_called_once()
            mock_builder.client_id.assert_called_once_with("test-client")
            mock_builder.scope.assert_called_once_with("test-scope")
            mock_builder.token_endpoint.assert_called_once_with("https://example.com/token")
            mock_builder.authn_method.assert_called_once_with(TokenAuthnMethod.CLIENT_SECRET_POST)
            mock_builder.client_secret_supplier.assert_called_once()
            mock_builder.build.assert_called_once()

    @patch("cloud_idaas.core.implementation.idaas_machine_credential_provider.IDaaSMachineCredentialProviderBuilder")
    def test_create_credential_provider_unsupported_method_raises_exception(self, mock_builder_class):
        """Test _create_credential_provider raises exception for unsupported authentication method."""
        # Setup configuration
        config = IDaaSClientConfig()
        config.client_id = "test-client"
        config.token_endpoint = "https://example.com/token"

        authn_config = IdentityAuthenticationConfiguration()
        authn_config.authn_method = TokenAuthnMethod.NONE  # Unsupported method for machine auth
        config.authn_configuration = authn_config

        # Replace the factory's config with our test config
        IDaaSCredentialProviderFactory._idaas_client_config = config
        IDaaSCredentialProviderFactory._initialized = True

        with self.assertRaises(ConfigException) as context:
            IDaaSCredentialProviderFactory._create_credential_provider("test-scope")

        self.assertEqual(context.exception.error_code, ErrorCode.UNSUPPORTED_AUTHENTICATION_METHOD)


if __name__ == "__main__":
    unittest.main()
