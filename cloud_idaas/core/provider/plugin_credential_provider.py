from abc import ABC, abstractmethod

from cloud_idaas.core.credential import IDaaSTokenResponse


class PluginCredentialProvider(ABC):
    @abstractmethod
    def get_idaas_credential(self, scope: str) -> IDaaSTokenResponse:
        pass
