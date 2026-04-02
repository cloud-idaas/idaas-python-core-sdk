from cloud_idaas.core.credential import IDaaSTokenResponse
from cloud_idaas.core.implementation.static_idaas_credential_provider import (
    StaticIDaaSCredentialProvider,
    StaticIDaaSCredentialProviderBuilder,
)


class TestStaticIDaaSCredentialProvider:
    """Tests for StaticIDaaSCredentialProvider."""

    def test_create_with_credential(self):
        """Test creating provider with credential."""
        token = IDaaSTokenResponse()
        token.access_token = "test-access-token"
        token.token_type = "Bearer"

        provider = StaticIDaaSCredentialProvider(credential=token)

        assert provider.get_credential() == token
        assert provider.get_bearer_token() == "test-access-token"
        assert provider.get_oidc_token() == "test-access-token"

    def test_create_without_credential(self):
        """Test creating provider without credential."""
        provider = StaticIDaaSCredentialProvider()

        assert provider.get_credential() is None
        assert provider.get_bearer_token() is None
        assert provider.get_oidc_token() is None

    def test_builder_creates_provider(self):
        """Test that builder creates a provider."""
        token = IDaaSTokenResponse()
        token.access_token = "test-access-token"

        provider = StaticIDaaSCredentialProvider.builder().credential(token).build()

        assert provider.get_credential() == token

    def test_builder_returns_builder_instance(self):
        """Test that builder() returns a builder instance."""
        builder = StaticIDaaSCredentialProvider.builder()

        assert isinstance(builder, StaticIDaaSCredentialProviderBuilder)

    def test_builder_credential_returns_builder(self):
        """Test that credential() returns builder for chaining."""
        builder = StaticIDaaSCredentialProviderBuilder()

        result = builder.credential(IDaaSTokenResponse())

        assert result is builder

    def test_get_bearer_token_returns_access_token(self):
        """Test that get_bearer_token returns access token."""
        token = IDaaSTokenResponse()
        token.access_token = "my-access-token"

        provider = StaticIDaaSCredentialProvider(credential=token)

        assert provider.get_bearer_token() == "my-access-token"

    def test_get_oidc_token_same_as_bearer_token(self):
        """Test that get_oidc_token returns same as bearer token."""
        token = IDaaSTokenResponse()
        token.access_token = "my-access-token"

        provider = StaticIDaaSCredentialProvider(credential=token)

        assert provider.get_oidc_token() == provider.get_bearer_token()

    def test_multiple_builds_independent(self):
        """Test that multiple builds create independent providers."""
        token1 = IDaaSTokenResponse()
        token1.access_token = "token1"

        token2 = IDaaSTokenResponse()
        token2.access_token = "token2"

        builder = StaticIDaaSCredentialProvider.builder()
        provider1 = builder.credential(token1).build()
        provider2 = builder.credential(token2).build()

        assert provider1.get_bearer_token() == "token1"
        assert provider2.get_bearer_token() == "token2"

    def test_with_full_token_response(self):
        """Test with full token response."""
        token = IDaaSTokenResponse()
        token.access_token = "access-token"
        token.id_token = "id-token"
        token.refresh_token = "refresh-token"
        token.token_type = "Bearer"
        token.expires_in = 3600
        token.expires_at = 1234567890

        provider = StaticIDaaSCredentialProvider(credential=token)
        credential = provider.get_credential()

        assert credential.access_token == "access-token"
        assert credential.id_token == "id-token"
        assert credential.refresh_token == "refresh-token"
        assert credential.token_type == "Bearer"
        assert credential.expires_in == 3600
        assert credential.expires_at == 1234567890

    def test_none_credential_returns_none_token(self):
        """Test that None credential returns None for all token methods."""
        provider = StaticIDaaSCredentialProvider()

        assert provider.get_credential() is None
        assert provider.get_bearer_token() is None
        assert provider.get_oidc_token() is None
