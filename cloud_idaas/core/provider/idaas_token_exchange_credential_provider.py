from abc import ABC, abstractmethod
from typing import Optional

from cloud_idaas.core.credential import IDaaSCredential


class IDaaSTokenExchangeCredentialProvider(ABC):
    @abstractmethod
    def get_credential(
        self,
        subject_token: str,
        subject_token_type: str,
        requested_token_type: Optional[str] = None,
    ) -> IDaaSCredential:
        raise NotImplementedError

    def get_issued_token(
        self,
        subject_token: str,
        subject_token_type: str,
        requested_token_type: Optional[str] = None,
    ) -> str:
        credential = self.get_credential(
            subject_token=subject_token,
            subject_token_type=subject_token_type,
            requested_token_type=requested_token_type,
        )
        return credential.get_access_token()
