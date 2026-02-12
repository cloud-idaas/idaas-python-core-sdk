"""
IDaaS Python SDK - Identity Authentication Configuration
"""

from typing import Optional

from cloud_idaas.core.constants import AuthenticationIdentityEnum, ClientDeployEnvironmentEnum, TokenAuthnMethod


class IdentityAuthenticationConfiguration:
    """
    Identity authentication configuration class.
    """

    def __init__(self):
        self._identity_type: AuthenticationIdentityEnum = AuthenticationIdentityEnum.CLIENT
        self._authn_method: TokenAuthnMethod = TokenAuthnMethod.NONE
        self._client_secret_env_var_name: Optional[str] = None
        self._private_key_env_var_name: Optional[str] = None
        self._application_federated_credential_name: Optional[str] = None
        self._client_deploy_environment: Optional[ClientDeployEnvironmentEnum] = None
        self._oidc_token_file_path_env_var_name: Optional[str] = None
        self._oidc_token_file_path: Optional[str] = None
        self._client_x509_certificate: Optional[str] = None
        self._x509_cert_chains: Optional[str] = None
        self._human_authenticate_client_id: str = "iap_developer"

    @property
    def identity_type(self) -> AuthenticationIdentityEnum:
        return self._identity_type

    @identity_type.setter
    def identity_type(self, value: AuthenticationIdentityEnum):
        self._identity_type = value

    @property
    def authn_method(self) -> TokenAuthnMethod:
        return self._authn_method

    @authn_method.setter
    def authn_method(self, value: TokenAuthnMethod):
        self._authn_method = value

    @property
    def client_secret_env_var_name(self) -> Optional[str]:
        return self._client_secret_env_var_name

    @client_secret_env_var_name.setter
    def client_secret_env_var_name(self, value: str):
        self._client_secret_env_var_name = value

    @property
    def private_key_env_var_name(self) -> Optional[str]:
        return self._private_key_env_var_name

    @private_key_env_var_name.setter
    def private_key_env_var_name(self, value: str):
        self._private_key_env_var_name = value

    @property
    def application_federated_credential_name(self) -> Optional[str]:
        return self._application_federated_credential_name

    @application_federated_credential_name.setter
    def application_federated_credential_name(self, value: str):
        self._application_federated_credential_name = value

    @property
    def client_deploy_environment(self) -> Optional[ClientDeployEnvironmentEnum]:
        return self._client_deploy_environment

    @client_deploy_environment.setter
    def client_deploy_environment(self, value: ClientDeployEnvironmentEnum):
        self._client_deploy_environment = value

    @property
    def oidc_token_file_path_env_var_name(self) -> Optional[str]:
        return self._oidc_token_file_path_env_var_name

    @oidc_token_file_path_env_var_name.setter
    def oidc_token_file_path_env_var_name(self, value: str):
        self._oidc_token_file_path_env_var_name = value

    @property
    def oidc_token_file_path(self) -> Optional[str]:
        return self._oidc_token_file_path

    @oidc_token_file_path.setter
    def oidc_token_file_path(self, value: str):
        self._oidc_token_file_path = value

    @property
    def client_x509_certificate(self) -> Optional[str]:
        return self._client_x509_certificate

    @client_x509_certificate.setter
    def client_x509_certificate(self, value: str):
        self._client_x509_certificate = value

    @property
    def x509_cert_chains(self) -> Optional[str]:
        return self._x509_cert_chains

    @x509_cert_chains.setter
    def x509_cert_chains(self, value: str):
        self._x509_cert_chains = value

    @property
    def human_authenticate_client_id(self) -> str:
        return self._human_authenticate_client_id

    @human_authenticate_client_id.setter
    def human_authenticate_client_id(self, value: str):
        self._human_authenticate_client_id = value

    def __repr__(self) -> str:
        """
        Return a string representation of the identity authentication configuration.

        Returns:
            String representation of the configuration.
        """
        return (
            f"IdentityAuthenticationConfiguration(identity_type={self._identity_type}, "
            f"authn_method={self._authn_method}, "
            f"client_secret_env_var_name={self._client_secret_env_var_name!r}, "
            f"private_key_env_var_name={self._private_key_env_var_name!r}, "
            f"application_federated_credential_name={self._application_federated_credential_name!r}, "
            f"client_deploy_environment={self._client_deploy_environment}, "
            f"oidc_token_file_path_env_var_name={self._oidc_token_file_path_env_var_name!r}, "
            f"oidc_token_file_path={self._oidc_token_file_path!r}, "
            f"client_x509_certificate={self._client_x509_certificate!r}, "
            f"x509_cert_chains={self._x509_cert_chains!r}, "
            f"human_authenticate_client_id={self._human_authenticate_client_id!r})"
        )

    def __eq__(self, other) -> bool:
        """
        Check if two IdentityAuthenticationConfiguration objects are equal.

        Args:
            other: Another object to compare with.

        Returns:
            True if equal, False otherwise.
        """
        if not isinstance(other, IdentityAuthenticationConfiguration):
            return NotImplemented
        return (
            self._identity_type == other._identity_type
            and self._authn_method == other._authn_method
            and self._client_secret_env_var_name == other._client_secret_env_var_name
            and self._private_key_env_var_name == other._private_key_env_var_name
            and self._application_federated_credential_name == other._application_federated_credential_name
            and self._client_deploy_environment == other._client_deploy_environment
            and self._oidc_token_file_path_env_var_name == other._oidc_token_file_path_env_var_name
            and self._oidc_token_file_path == other._oidc_token_file_path
            and self._client_x509_certificate == other._client_x509_certificate
            and self._x509_cert_chains == other._x509_cert_chains
            and self._human_authenticate_client_id == other._human_authenticate_client_id
        )

    def __hash__(self) -> int:
        """
        Return a hash value for the IdentityAuthenticationConfiguration object.

        Returns:
            Hash value.
        """
        return hash(
            (
                self._identity_type,
                self._authn_method,
                self._client_secret_env_var_name,
                self._private_key_env_var_name,
                self._application_federated_credential_name,
                self._client_deploy_environment,
                self._oidc_token_file_path_env_var_name,
                self._oidc_token_file_path,
                self._client_x509_certificate,
                self._x509_cert_chains,
                self._human_authenticate_client_id,
            )
        )

    @staticmethod
    def copy(source: "IdentityAuthenticationConfiguration") -> Optional["IdentityAuthenticationConfiguration"]:
        """
        Create a copy of the identity authentication configuration.

        Args:
            source: The source configuration to copy.

        Returns:
            A new IdentityAuthenticationConfiguration instance with copied values.
        """
        if source is None:
            return None

        target = IdentityAuthenticationConfiguration()
        target._authn_method = source._authn_method
        target._identity_type = source._identity_type
        target._client_secret_env_var_name = source._client_secret_env_var_name
        target._private_key_env_var_name = source._private_key_env_var_name
        target._application_federated_credential_name = source._application_federated_credential_name
        target._client_deploy_environment = source._client_deploy_environment
        target._oidc_token_file_path_env_var_name = source._oidc_token_file_path_env_var_name
        target._oidc_token_file_path = source._oidc_token_file_path
        target._client_x509_certificate = source._client_x509_certificate
        target._x509_cert_chains = source._x509_cert_chains
        target._human_authenticate_client_id = source._human_authenticate_client_id
        return target

    @classmethod
    def from_dict(cls, data: dict) -> "IdentityAuthenticationConfiguration":
        """
        Create an IdentityAuthenticationConfiguration instance from a dictionary.

        Supports both camelCase (JSON config style) and snake_case (Python style) keys.
        Also supports legacy key names for backward compatibility.

        Args:
            data: Dictionary containing IdentityAuthenticationConfiguration properties.

        Returns:
            An IdentityAuthenticationConfiguration instance with values from the dictionary.
        """
        from cloud_idaas.core.constants import AuthenticationIdentityEnum, ClientDeployEnvironmentEnum, TokenAuthnMethod
        from cloud_idaas.core.util.string_util import StringUtil

        authn_config = cls()
        if data is not None:
            # Normalize keys: convert camelCase to snake_case for lookup
            normalized_data = {}
            for key, value in data.items():
                normalized_key = StringUtil.camel_to_snake(key)
                normalized_data[normalized_key] = value

            # Handle identity_type (also supports legacy key: authentication_subject)
            identity_value = normalized_data.get("identity_type") or normalized_data.get("authentication_subject")
            if identity_value and isinstance(identity_value, str):
                if identity_value == AuthenticationIdentityEnum.HUMAN.value:
                    authn_config.identity_type = AuthenticationIdentityEnum.HUMAN
                elif identity_value == AuthenticationIdentityEnum.CLIENT.value:
                    authn_config.identity_type = AuthenticationIdentityEnum.CLIENT

            # Handle authn_method
            authn_method_str = normalized_data.get("authn_method")
            if authn_method_str and isinstance(authn_method_str, str):
                for method in [
                    TokenAuthnMethod.NONE,
                    TokenAuthnMethod.CLIENT_SECRET_POST,
                    TokenAuthnMethod.CLIENT_SECRET_BASIC,
                    TokenAuthnMethod.CLIENT_SECRET_JWT,
                    TokenAuthnMethod.PRIVATE_KEY_JWT,
                    TokenAuthnMethod.PKCS7,
                    TokenAuthnMethod.PCA,
                    TokenAuthnMethod.OIDC,
                ]:
                    if authn_method_str == method.value:
                        authn_config.authn_method = method
                        break

            if "client_secret_env_var_name" in normalized_data:
                authn_config.client_secret_env_var_name = normalized_data["client_secret_env_var_name"]
            if "private_key_env_var_name" in normalized_data:
                authn_config.private_key_env_var_name = normalized_data["private_key_env_var_name"]
            if "application_federated_credential_name" in normalized_data:
                authn_config.application_federated_credential_name = normalized_data[
                    "application_federated_credential_name"
                ]

            # Handle client_deploy_environment
            client_deploy_env_str = normalized_data.get("client_deploy_environment")
            if client_deploy_env_str and isinstance(client_deploy_env_str, str):
                for env in [
                    ClientDeployEnvironmentEnum.COMMON,
                    ClientDeployEnvironmentEnum.COMPUTER,
                    ClientDeployEnvironmentEnum.KUBERNETES,
                    ClientDeployEnvironmentEnum.ALIBABA_CLOUD_ECS,
                    ClientDeployEnvironmentEnum.ALIBABA_CLOUD_ECI,
                    ClientDeployEnvironmentEnum.ALIBABA_CLOUD_ACK,
                    ClientDeployEnvironmentEnum.AWS_EC2,
                    ClientDeployEnvironmentEnum.AWS_ESK,
                    ClientDeployEnvironmentEnum.GOOGLE_VM,
                    ClientDeployEnvironmentEnum.HUAWEI_CLOUD_ECS,
                    ClientDeployEnvironmentEnum.CUSTOM,
                ]:
                    if client_deploy_env_str == env.value:
                        authn_config.client_deploy_environment = env
                        break

            if "oidc_token_file_path_env_var_name" in normalized_data:
                authn_config.oidc_token_file_path_env_var_name = normalized_data["oidc_token_file_path_env_var_name"]
            if "oidc_token_file_path" in normalized_data:
                authn_config.oidc_token_file_path = normalized_data["oidc_token_file_path"]
            if "client_x509_certificate" in normalized_data:
                authn_config.client_x509_certificate = normalized_data["client_x509_certificate"]
            if "x509_cert_chains" in normalized_data:
                authn_config.x509_cert_chains = normalized_data["x509_cert_chains"]
            if "human_authenticate_client_id" in normalized_data:
                authn_config.human_authenticate_client_id = normalized_data["human_authenticate_client_id"]
        return authn_config
