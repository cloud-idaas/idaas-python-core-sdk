import time

from cloud_idaas.core.factory import IDaaSCredentialProviderFactory


def loopSample():
    while True:
        print("access token:")
        credential_provider_pam = IDaaSCredentialProviderFactory.get_idaas_credential_provider()
        access_token_pam = credential_provider_pam.get_bearer_token()
        print(access_token_pam)
        time.sleep(10)


if __name__ == "__main__":
    IDaaSCredentialProviderFactory.init()
    loopSample()
