import time

from cloud_idaas.core.factory import IDaaSCredentialProviderFactory


def loop_sample():
    while True:
        print("loopSample")
        time.sleep(1)


if __name__ == "__main__":
    IDaaSCredentialProviderFactory.init()
    loop_sample()
