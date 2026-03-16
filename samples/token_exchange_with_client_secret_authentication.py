from cloud_idaas.core.constants import OAuth2Constants
from cloud_idaas.core.factory import IDaaSCredentialProviderFactory


def token_exchange_sample():
    # Initialize the factory with configuration
    IDaaSCredentialProviderFactory.init()

    # Option 1: Get Token Exchange credential provider with scope from config file
    token_exchange_provider = IDaaSCredentialProviderFactory.get_token_exchange_credential_provider()

    # Option 2: Get Token Exchange credential provider with scope specified by parameter
    # token_exchange_provider = IDaaSCredentialProviderFactory.get_token_exchange_credential_provider_by_scope("api://test|scope")


    # The subject token to exchange (obtained from another identity provider)
    subject_token = ""

    # Perform token exchange
    # scope format: <audience>|<scope>
    access_token = token_exchange_provider.get_issued_token(
        subject_token=subject_token,
        subject_token_type=OAuth2Constants.ACCESS_TOKEN_TYPE_VALUE,
    )

    print(f"Exchanged access token: {access_token}")
    return access_token


if __name__ == "__main__":
    print("=== Token Exchange Sample ===")
    token_exchange_sample()
