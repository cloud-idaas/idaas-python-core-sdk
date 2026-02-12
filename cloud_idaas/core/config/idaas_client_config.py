"""
IDaaS Python SDK - IDaaS Client Configuration
"""

from typing import Optional

from cloud_idaas.core.config.http_configuration import HttpConfiguration
from cloud_idaas.core.config.identity_authentication_configuration import IdentityAuthenticationConfiguration


class IDaaSClientConfig:
    """
    IDaaS client configuration class.
    """

    def __init__(self):
        self._idaas_instance_id: Optional[str] = None
        self._client_id: Optional[str] = None
        # Default value, using idaas pam resource server scope
        self._scope: str = "urn:cloud:idaas:pam|cloud_account:obtain_access_credential"
        self._issuer: Optional[str] = None
        self._token_endpoint: Optional[str] = None
        self._device_authorization_endpoint: Optional[str] = None
        self._developer_api_endpoint: Optional[str] = None
        self._authn_configuration: Optional[IdentityAuthenticationConfiguration] = None
        self._http_configuration: HttpConfiguration = HttpConfiguration()

    @property
    def idaas_instance_id(self) -> Optional[str]:
        return self._idaas_instance_id

    @idaas_instance_id.setter
    def idaas_instance_id(self, value: str):
        self._idaas_instance_id = value

    @property
    def client_id(self) -> Optional[str]:
        return self._client_id

    @client_id.setter
    def client_id(self, value: str):
        self._client_id = value

    @property
    def scope(self) -> str:
        return self._scope

    @scope.setter
    def scope(self, value: str):
        self._scope = value

    @property
    def issuer(self) -> Optional[str]:
        return self._issuer

    @issuer.setter
    def issuer(self, value: str):
        self._issuer = value

    @property
    def token_endpoint(self) -> Optional[str]:
        return self._token_endpoint

    @token_endpoint.setter
    def token_endpoint(self, value: str):
        self._token_endpoint = value

    @property
    def device_authorization_endpoint(self) -> Optional[str]:
        return self._device_authorization_endpoint

    @device_authorization_endpoint.setter
    def device_authorization_endpoint(self, value: str):
        self._device_authorization_endpoint = value

    @property
    def developer_api_endpoint(self) -> Optional[str]:
        return self._developer_api_endpoint

    @developer_api_endpoint.setter
    def developer_api_endpoint(self, value: str):
        self._developer_api_endpoint = value

    @property
    def authn_configuration(self) -> Optional[IdentityAuthenticationConfiguration]:
        return self._authn_configuration

    @authn_configuration.setter
    def authn_configuration(self, value: IdentityAuthenticationConfiguration):
        self._authn_configuration = value

    @property
    def http_configuration(self) -> HttpConfiguration:
        return self._http_configuration

    @http_configuration.setter
    def http_configuration(self, value: HttpConfiguration):
        self._http_configuration = value

    def __repr__(self) -> str:
        """
        Return a string representation of the IDaaS client configuration.

        Returns:
            String representation of the configuration.
        """
        return (
            f"IDaaSClientConfig(idaas_instance_id={self._idaas_instance_id!r}, "
            f"client_id={self._client_id!r}, scope={self._scope!r}, "
            f"issuer={self._issuer!r}, token_endpoint={self._token_endpoint!r}, "
            f"device_authorization_endpoint={self._device_authorization_endpoint!r}, "
            f"developer_api_endpoint={self._developer_api_endpoint!r}, "
            f"authn_configuration={self._authn_configuration}, "
            f"http_configuration={self._http_configuration})"
        )

    def __eq__(self, other) -> bool:
        """
        Check if two IDaaSClientConfig objects are equal.

        Args:
            other: Another object to compare with.

        Returns:
            True if equal, False otherwise.
        """
        if not isinstance(other, IDaaSClientConfig):
            return NotImplemented
        return (
            self._idaas_instance_id == other._idaas_instance_id
            and self._client_id == other._client_id
            and self._scope == other._scope
            and self._issuer == other._issuer
            and self._token_endpoint == other._token_endpoint
            and self._device_authorization_endpoint == other._device_authorization_endpoint
            and self._developer_api_endpoint == other._developer_api_endpoint
            and self._authn_configuration == other._authn_configuration
            and self._http_configuration == other._http_configuration
        )

    def __hash__(self) -> int:
        """
        Return a hash value for the IDaaSClientConfig object.

        Returns:
            Hash value.
        """
        return hash(
            (
                self._idaas_instance_id,
                self._client_id,
                self._scope,
                self._issuer,
                self._token_endpoint,
                self._device_authorization_endpoint,
                self._developer_api_endpoint,
                self._authn_configuration,
                self._http_configuration,
            )
        )

    def assign(self, other: "IDaaSClientConfig") -> None:
        """
        Assign values from another configuration.

        Args:
            other: The source configuration to copy from.
        """
        if other is None:
            return
        self._idaas_instance_id = other._idaas_instance_id
        self._client_id = other._client_id
        self._scope = other._scope
        self._issuer = other._issuer
        self._token_endpoint = other._token_endpoint
        self._device_authorization_endpoint = other._device_authorization_endpoint
        self._developer_api_endpoint = other._developer_api_endpoint
        if other._authn_configuration is not None:
            self._authn_configuration = IdentityAuthenticationConfiguration.copy(other._authn_configuration)
        else:
            self._authn_configuration = None
        if other._http_configuration is not None:
            self._http_configuration = HttpConfiguration.copy(other._http_configuration)
        else:
            self._http_configuration = None

    @classmethod
    def from_dict(cls, data: dict) -> "IDaaSClientConfig":
        """
        Create an IDaaSClientConfig instance from a dictionary.

        Supports both camelCase (JSON config style) and snake_case (Python style) keys.

        Args:
            data: Dictionary containing IDaaSClientConfig properties.

        Returns:
            An IDaaSClientConfig instance with values from the dictionary.
        """
        from cloud_idaas.core.config.http_configuration import HttpConfiguration
        from cloud_idaas.core.config.identity_authentication_configuration import IdentityAuthenticationConfiguration
        from cloud_idaas.core.util.string_util import StringUtil

        config = cls()
        if data is not None:
            # Normalize keys: convert camelCase to snake_case for lookup
            normalized_data = {}
            for key, value in data.items():
                normalized_key = StringUtil.camel_to_snake(key)
                normalized_data[normalized_key] = value

            if "idaas_instance_id" in normalized_data:
                config.idaas_instance_id = normalized_data["idaas_instance_id"]
            if "client_id" in normalized_data:
                config.client_id = normalized_data["client_id"]
            if "scope" in normalized_data:
                config.scope = normalized_data["scope"]
            if "issuer" in normalized_data:
                config.issuer = normalized_data["issuer"]
            if "token_endpoint" in normalized_data:
                config.token_endpoint = normalized_data["token_endpoint"]
            if "device_authorization_endpoint" in normalized_data:
                config.device_authorization_endpoint = normalized_data["device_authorization_endpoint"]
            if "developer_api_endpoint" in normalized_data:
                config.developer_api_endpoint = normalized_data["developer_api_endpoint"]
            if "authn_configuration" in normalized_data:
                if normalized_data["authn_configuration"] is not None:
                    config.authn_configuration = IdentityAuthenticationConfiguration.from_dict(
                        normalized_data["authn_configuration"]
                    )
            if "http_configuration" in normalized_data:
                if normalized_data["http_configuration"] is not None:
                    config.http_configuration = HttpConfiguration.from_dict(normalized_data["http_configuration"])
        return config
