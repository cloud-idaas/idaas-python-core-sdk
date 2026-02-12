"""
Unit tests for IDaaS Python SDK constants
"""

from cloud_idaas.core import (
    AuthenticationConstants,
    AuthenticationIdentityEnum,
    ClientAssertionType,
    ClientDeployEnvironmentEnum,
    ConfigPathConstants,
    ErrorCode,
    HttpConstants,
    OAuth2Constants,
    TokenAuthnMethod,
)


class TestAuthenticationConstants:
    """Test cases for AuthenticationConstants"""

    def test_kubernetes_service_account_token_path(self):
        assert (
            AuthenticationConstants.KUBERNETES_SERVICE_ACCOUNT_TOKEN_PATH
            == "/var/run/secrets/kubernetes.io/serviceaccount/token"
        )

    def test_alibaba_cloud_ecs_metadata_service_url(self):
        assert (
            AuthenticationConstants.ALIBABA_CLOUD_ECS_METADATA_SERVICE_URL == "http://100.100.100.200/latest/meta-data/"
        )

    def test_alibaba_cloud_ack_oidc_token_path_env(self):
        assert AuthenticationConstants.ALIBABA_CLOUD_ACK_OIDC_TOKEN_PATH_ENV == "ALIBABA_CLOUD_OIDC_TOKEN_FILE"

    def test_default_client_id_environment_variable_name(self):
        assert AuthenticationConstants.DEFAULT_CLIENT_ID_ENVIRONMENT_VARIABLE_NAME == "CLOUD_IDAAS_CLIENT_ID"

    def test_default_client_secret_environment_variable_name(self):
        assert AuthenticationConstants.DEFAULT_CLIENT_SECRET_ENVIRONMENT_VARIABLE_NAME == "CLOUD_IDAAS_CLIENT_SECRET"


class TestConfigPathConstants:
    """Test cases for ConfigPathConstants"""

    def test_env_config_path_key(self):
        assert ConfigPathConstants.ENV_CONFIG_PATH_KEY == "CLOUD_IDAAS_CONFIG_PATH"

    def test_default_config_path(self):
        assert ConfigPathConstants.DEFAULT_CONFIG_PATH.startswith("~/.cloud_idaas/client-config.json")

    def test_env_human_credential_cache_path_key(self):
        assert ConfigPathConstants.ENV_HUMAN_CREDENTIAL_CACHE_PATH_KEY == "CLOUD_IDAAS_HUMAN_CREDENTIAL_CACHE_PATH"

    def test_default_human_credential_cache_path_template(self):
        assert ConfigPathConstants.DEFAULT_HUMAN_CREDENTIAL_CACHE_PATH_TEMPLATE.startswith("~/.cloud_idaas/")


class TestOAuth2Constants:
    """Test cases for OAuth2Constants"""

    def test_client_id(self):
        assert OAuth2Constants.CLIENT_ID == "client_id"

    def test_client_secret(self):
        assert OAuth2Constants.CLIENT_SECRET == "client_secret"

    def test_scope(self):
        assert OAuth2Constants.SCOPE == "scope"

    def test_device_code(self):
        assert OAuth2Constants.DEVICE_CODE == "device_code"

    def test_grant_type(self):
        assert OAuth2Constants.GRANT_TYPE == "grant_type"

    def test_client_credentials_grant_type_value(self):
        assert OAuth2Constants.CLIENT_CREDENTIALS_GRANT_TYPE_VALUE == "client_credentials"

    def test_token_exchange_grant_type_value(self):
        assert OAuth2Constants.TOKEN_EXCHANGE_GRANT_TYPE_VALUE == "urn:ietf:params:oauth:grant-type:token-exchange"

    def test_device_code_grant_type_value(self):
        assert OAuth2Constants.DEVICE_CODE_GRANT_TYPE_VALUE == "urn:ietf:params:oauth:grant-type:device_code"

    def test_refresh_token_grant_type_value(self):
        assert OAuth2Constants.REFRESH_TOKEN_GRANT_TYPE_VALUE == "refresh_token"

    def test_client_assertion_type(self):
        assert OAuth2Constants.CLIENT_ASSERTION_TYPE == "client_assertion_type"

    def test_client_assertion(self):
        assert OAuth2Constants.CLIENT_ASSERTION == "client_assertion"

    def test_application_federated_credential_name(self):
        assert OAuth2Constants.APPLICATION_FEDERATED_CREDENTIAL_NAME == "application_federated_credential_name"

    def test_refresh_token_parameter(self):
        assert OAuth2Constants.REFRESH_TOKEN_PARAMETER == "refresh_token"

    def test_client_x509_certificate(self):
        assert OAuth2Constants.CLIENT_X509_CERTIFICATE == "client_x509"

    def test_x509_cert_chains(self):
        assert OAuth2Constants.X509_CERT_CHAINS == "client_x509_chain"

    def test_subject_token(self):
        assert OAuth2Constants.SUBJECT_TOKEN == "subject_token"

    def test_subject_token_type(self):
        assert OAuth2Constants.SUBJECT_TOKEN_TYPE == "subject_token_type"

    def test_subject_token_type_value(self):
        assert OAuth2Constants.SUBJECT_TOKEN_TYPE_VALUE == "urn:ietf:params:oauth:token-type:jwt"

    def test_requested_token_type(self):
        assert OAuth2Constants.REQUESTED_TOKEN_TYPE == "requested_token_type"

    def test_requested_token_type_value(self):
        assert OAuth2Constants.REQUESTED_TOKEN_TYPE_VALUE == "urn:ietf:params:oauth:token-type:access_token"

    def test_audience(self):
        assert OAuth2Constants.AUDIENCE == "audience"


class TestHttpConstants:
    """Test cases for HttpConstants"""

    def test_https(self):
        assert HttpConstants.HTTPS == "https"

    def test_authorization_header(self):
        assert HttpConstants.AUTHORIZATION_HEADER == "Authorization"

    def test_content_type_header(self):
        assert HttpConstants.CONTENT_TYPE_HEADER == "Content-Type"

    def test_bearer(self):
        assert HttpConstants.BEARER == "Bearer"

    def test_basic(self):
        assert HttpConstants.BASIC == "Basic"

    def test_user_agent(self):
        assert HttpConstants.USER_AGENT == "User-Agent"

    def test_location(self):
        assert HttpConstants.LOCATION == "Location"

    def test_redirect_to(self):
        assert HttpConstants.REDIRECT_TO == "Redirect to: "

    def test_x_aliyun_ecs_metadata_token_ttl_seconds(self):
        assert HttpConstants.X_ALIYUN_ECS_METADATA_TOKEN_TTL_SECONDS == "X-aliyun-ecs-metadata-token-ttl-seconds"

    def test_x_aliyun_ecs_metadata_token(self):
        assert HttpConstants.X_ALIYUN_ECS_METADATA_TOKEN == "X-aliyun-ecs-metadata-token"

    def test_colon(self):
        assert HttpConstants.COLON == ":"

    def test_space(self):
        assert HttpConstants.SPACE == " "


class TestClientAssertionType:
    """Test cases for ClientAssertionType"""

    def test_oauth_jwt_bearer(self):
        assert ClientAssertionType.OAUTH_JWT_BEARER == "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"

    def test_private_ca_jwt_bearer(self):
        assert (
            ClientAssertionType.PRIVATE_CA_JWT_BEARER
            == "urn:cloud:idaas:params:oauth:client-assertion-type:x509-jwt-bearer"
        )

    def test_pkcs7_bearer(self):
        assert ClientAssertionType.PKCS7_BEARER == "urn:cloud:idaas:params:oauth:client-assertion-type:pkcs7-bearer"

    def test_oidc_bearer(self):
        assert ClientAssertionType.OIDC_BEARER == "urn:cloud:idaas:params:oauth:client-assertion-type:id-token-bearer"


class TestAuthenticationIdentityEnum:
    """Test cases for AuthenticationIdentityEnum"""

    def test_human(self):
        assert AuthenticationIdentityEnum.HUMAN.value == "HUMAN"

    def test_client(self):
        assert AuthenticationIdentityEnum.CLIENT.value == "CLIENT"

    def test_human_str(self):
        assert str(AuthenticationIdentityEnum.HUMAN) == "HUMAN"

    def test_client_str(self):
        assert str(AuthenticationIdentityEnum.CLIENT) == "CLIENT"


class TestClientDeployEnvironmentEnum:
    """Test cases for ClientDeployEnvironmentEnum"""

    def test_common(self):
        assert ClientDeployEnvironmentEnum.COMMON.value == "COMMON"

    def test_computer(self):
        assert ClientDeployEnvironmentEnum.COMPUTER.value == "COMPUTER"

    def test_kubernetes(self):
        assert ClientDeployEnvironmentEnum.KUBERNETES.value == "KUBERNETES"

    def test_alibaba_cloud_ecs(self):
        assert ClientDeployEnvironmentEnum.ALIBABA_CLOUD_ECS.value == "ALIBABA_CLOUD_ECS"

    def test_alibaba_cloud_eci(self):
        assert ClientDeployEnvironmentEnum.ALIBABA_CLOUD_ECI.value == "ALIBABA_CLOUD_ECI"

    def test_alibaba_cloud_ack(self):
        assert ClientDeployEnvironmentEnum.ALIBABA_CLOUD_ACK.value == "ALIBABA_CLOUD_ACK"

    def test_aws_ec2(self):
        assert ClientDeployEnvironmentEnum.AWS_EC2.value == "AWS_EC2"

    def test_aws_esk(self):
        assert ClientDeployEnvironmentEnum.AWS_ESK.value == "AWS_ESK"

    def test_google_vm(self):
        assert ClientDeployEnvironmentEnum.GOOGLE_VM.value == "GOOGLE_VM"

    def test_huawei_cloud_ecs(self):
        assert ClientDeployEnvironmentEnum.HUAWEI_CLOUD_ECS.value == "HUAWEI_CLOUD_ECS"

    def test_custom(self):
        assert ClientDeployEnvironmentEnum.CUSTOM.value == "CUSTOM"

    def test_common_str(self):
        assert str(ClientDeployEnvironmentEnum.COMMON) == "COMMON"

    def test_computer_str(self):
        assert str(ClientDeployEnvironmentEnum.COMPUTER) == "COMPUTER"

    def test_kubernetes_str(self):
        assert str(ClientDeployEnvironmentEnum.KUBERNETES) == "KUBERNETES"

    def test_custom_str(self):
        assert str(ClientDeployEnvironmentEnum.CUSTOM) == "CUSTOM"


class TestErrorCode:
    """Test cases for ErrorCode"""

    def test_idaas_instance_id_not_found(self):
        assert ErrorCode.IDAAS_INSTANCE_ID_NOT_FOUND == "IDaaSInstanceIdNotFound"

    def test_client_id_not_found(self):
        assert ErrorCode.CLIENT_ID_NOT_FOUND == "ClientIdNotFound"

    def test_issuer_endpoint_not_found(self):
        assert ErrorCode.ISSUER_ENDPOINT_NOT_FOUND == "IssuerEndpointNotFound"

    def test_token_endpoint_not_found(self):
        assert ErrorCode.TOKEN_ENDPOINT_NOT_FOUND == "TokenEndpointNotFound"

    def test_human_authenticate_client_id_not_found(self):
        assert ErrorCode.HUMAN_AUTHENTICATE_CLIENT_ID_NOT_FOUND == "HumanAuthenticateClientIdNotFound"

    def test_human_authenticate_scope_not_found(self):
        assert ErrorCode.HUMAN_AUTHENTICATE_SCOPE_NOT_FOUND == "HumanAuthenticateScopeNotFound"

    def test_device_authorization_endpoint_not_found(self):
        assert ErrorCode.DEVICE_AUTHORIZATION_ENDPOINT_NOT_FOUND == "DeviceAuthorizationEndpointNotFound"

    def test_authn_configuration_not_found(self):
        assert ErrorCode.AUTHN_CONFIGURATION_NOT_FOUND == "AuthnConfigurationNotFound"

    def test_client_secret_env_var_name_not_found(self):
        assert ErrorCode.CLIENT_SECRET_ENV_VAR_NAME_NOT_FOUND == "ClientSecretEnvVarNameNotFound"

    def test_private_key_env_var_name_not_found(self):
        assert ErrorCode.PRIVATE_KEY_ENV_VAR_NAME_NOT_FOUND == "PrivateKeyEnvVarNameNotFound"

    def test_application_federated_credential_name_not_found(self):
        assert ErrorCode.APPLICATION_FEDERATED_CREDENTIAL_NAME_NOT_FOUND == "ApplicationFederatedCredentialNameNotFound"

    def test_client_deploy_environment_not_found(self):
        assert ErrorCode.CLIENT_DEPLOY_ENVIRONMENT_NOT_FOUND == "ClientDeployEnvironmentNotFound"

    def test_client_x509_certificate_not_found(self):
        assert ErrorCode.CLIENT_X509_CERTIFICATE_NOT_FOUND == "ClientX509CertificateNotFound"

    def test_x509_cert_chains_not_found(self):
        assert ErrorCode.X509_CERT_CHAINS_NOT_FOUND == "X509CertChainsNotFound"

    def test_unsupported_client_deploy_environment(self):
        assert ErrorCode.UNSUPPORTED_CLIENT_DEPLOY_ENVIRONMENT == "UnsupportedClientDeployEnvironment"

    def test_unsupported_authentication_method(self):
        assert ErrorCode.UNSUPPORTED_AUTHENTICATION_METHOD == "UnsupportedAuthenticationMethod"

    def test_connect_timeout_not_valid(self):
        assert ErrorCode.CONNECT_TIMEOUT_NOT_VALID == "ConnectTimeoutNotValid"

    def test_read_timeout_not_valid(self):
        assert ErrorCode.READ_TIMEOUT_NOT_VALID == "ReadTimeoutNotValid"

    def test_idaas_credential_provider_factory_not_init(self):
        assert ErrorCode.IDAAS_CREDENTIAL_PROVIDER_FACTORY_NOT_INIT == "IDaaSCredentialProviderFactoryNotInit"

    def test_not_supported_web_key(self):
        assert ErrorCode.NOT_SUPPORTED_WEB_KEY == "NotSupportedWebKey"

    def test_refresh_token_empty(self):
        assert ErrorCode.REFRESH_TOKEN_EMPTY == "RefreshTokenEmpty"

    def test_developer_api_endpoint_not_found(self):
        assert ErrorCode.DEVELOPER_API_ENDPOINT_NOT_FOUND == "DeveloperApiEndpointNotFound"

    def test_load_config_file_failed(self):
        assert ErrorCode.LOAD_CONFIG_FILE_FAILED == "LoadConfigFileFailed"

    def test_invalid_request(self):
        assert ErrorCode.INVALID_REQUEST == "InvalidRequest"

    def test_connect_time_out(self):
        assert ErrorCode.CONNECT_TIME_OUT == "ConnectTimeOut"

    def test_read_time_out(self):
        assert ErrorCode.READ_TIME_OUT == "ReadTimeOut"

    def test_client_error(self):
        assert ErrorCode.CLIENT_ERROR == "ClientError"

    def test_server_error(self):
        assert ErrorCode.SERVER_ERROR == "ServerError"

    def test_invalid_token_type(self):
        assert ErrorCode.INVALID_TOKEN_TYPE == "InvalidTokenType"

    def test_access_token_not_found(self):
        assert ErrorCode.ACCESS_TOKEN_NOT_FOUND == "AccessTokenNotFound"

    def test_id_token_not_found(self):
        assert ErrorCode.ID_TOKEN_NOT_FOUND == "IdTokenNotFound"

    def test_refresh_token_not_found(self):
        assert ErrorCode.REFRESH_TOKEN_NOT_FOUND == "RefreshTokenNotFound"


class TestTokenAuthnMethod:
    """Test cases for TokenAuthnMethod"""

    def test_none(self):
        assert TokenAuthnMethod.NONE.value == "NONE"

    def test_client_secret_post(self):
        assert TokenAuthnMethod.CLIENT_SECRET_POST.value == "CLIENT_SECRET_POST"

    def test_client_secret_basic(self):
        assert TokenAuthnMethod.CLIENT_SECRET_BASIC.value == "CLIENT_SECRET_BASIC"

    def test_client_secret_jwt(self):
        assert TokenAuthnMethod.CLIENT_SECRET_JWT.value == "CLIENT_SECRET_JWT"

    def test_private_key_jwt(self):
        assert TokenAuthnMethod.PRIVATE_KEY_JWT.value == "PRIVATE_KEY_JWT"

    def test_pkcs7(self):
        assert TokenAuthnMethod.PKCS7.value == "PKCS7"

    def test_pca(self):
        assert TokenAuthnMethod.PCA.value == "PCA"

    def test_oidc(self):
        assert TokenAuthnMethod.OIDC.value == "OIDC"
