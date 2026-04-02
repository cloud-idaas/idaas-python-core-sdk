from cloud_idaas.core.config.idaas_client_config import IDaaSClientConfig
from cloud_idaas.core.constants import HttpConstants


class NormalizeUtil:
    """
    Utility class for normalizing configuration values.
    """

    @staticmethod
    def normalize_endpoints(config: IDaaSClientConfig) -> None:
        """
        Normalize all endpoints in the configuration to use HTTPS.

        This method converts HTTP endpoints to HTTPS and adds the HTTPS scheme
        to endpoints that don't have any scheme.

        Args:
            config: The IDaaS client configuration to normalize.
        """
        config.issuer = NormalizeUtil._convert_to_https(config.issuer)
        config.token_endpoint = NormalizeUtil._convert_to_https(config.token_endpoint)
        config.device_authorization_endpoint = NormalizeUtil._convert_to_https(config.device_authorization_endpoint)
        config.developer_api_endpoint = NormalizeUtil._convert_to_https(config.developer_api_endpoint)
        config.openapi_endpoint = NormalizeUtil._convert_to_https(config.openapi_endpoint)

    @staticmethod
    def _convert_to_https(endpoint: str) -> str:
        """
        Convert an endpoint URL to use HTTPS scheme.

        Args:
            endpoint: The endpoint URL to convert.

        Returns:
            The endpoint URL with HTTPS scheme, or the original value if empty.
        """
        if not endpoint:
            return endpoint

        https_prefix = f"{HttpConstants.HTTPS}{HttpConstants.SCHEME_SEPARATOR}"
        http_prefix = f"{HttpConstants.HTTP}{HttpConstants.SCHEME_SEPARATOR}"

        # Already HTTPS
        if endpoint.startswith(https_prefix):
            return endpoint

        # HTTP -> HTTPS
        if endpoint.startswith(http_prefix):
            return f"{https_prefix}{endpoint[len(http_prefix) :]}"

        # No scheme -> Add HTTPS
        return f"{https_prefix}{endpoint}"
