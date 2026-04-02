# cloud-idaas-core

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Development Status](https://img.shields.io/badge/status-Beta-orange)](https://pypi.org/project/cloud-idaas-core/)

[简体中文](README_zh.md) | English

Python SDK for IDaaS (Identity as a Service) M2M products, providing convenient machine-to-machine authentication capabilities for developers.

## Features

- **Multiple Authentication Methods**: Supports various M2M authentication methods including JWT Client Secret, JWT Private Key, OIDC Token, PKCS7 Attested Document, etc.
- **Plugin Extension**: Supports custom credential providers to meet special scenario requirements
- **Intelligent Caching Mechanism**: Built-in credential caching strategy with prefetch and stale value handling to reduce unnecessary network requests
- **Flexible Configuration**: Supports configuration files, environment variables, and programmatic configuration
- **Token Exchange (RFC 8693)**: Supports token exchange to obtain access tokens with different scopes or audiences, suitable for token downgrading and service-to-service call scenarios

## Requirements

- Python >= 3.9
- Dependencies:
  - requests >= 2.31.0
  - cryptography >= 44.0.0
  - PyJWT >= 2.8.0
  - urllib3 >= 2.5.0

## Installation

```bash
pip install cloud-idaas-core

# or install a specific version
pip install cloud-idaas-core==x.x.x
```

[Latest SDK Version](https://pypi.org/project/cloud-idaas-core/)

## Specify Configuration File

The default path for the configuration file is: `~/.cloud_idaas/client-config.json`. If not explicitly specified, the configuration file will be loaded from this path by default.

You can specify the configuration file path via environment variable or initialization parameter:

- Environment variable name: `CLOUD_IDAAS_CONFIG_PATH`

### Environment variable example:

```
CLOUD_IDAAS_CONFIG_PATH=/.../client-config.json
```

### Initialization parameter example:

```python
IDaaSCredentialProviderFactory.init("/.../client-config.json")
```

## Configuration File Description

Configuration file example:

```json
{
    "idaasInstanceId": "idaas_ue2jvisn35ea5lmthk267xxxxx",
    "clientId": "app_mkv7rgt4d7i4u7zqtzev2mxxxx",
    "issuer": "https://xxx/api/v2/iauths_system/oauth2",
    "tokenEndpoint": "https://xxx/api/v2/iauths_system/oauth2/token",
    "scope": "api.example.com|read:file",
    "openApiEndpoint": "eiam.[region_id].aliyuncs.com",
    "developerApiEndpoint": "eiam-developerapi.[region_id].aliyuncs.com",
    "authnConfiguration": {
        "identityType": "CLIENT",
        "authnMethod": "CLIENT_SECRET_POST",
        "clientSecretEnvVarName": "IDAAS_CLIENT_SECRET"
    },
    "httpConfiguration": {
        "connectTimeout": 5000,
        "readTimeout": 10000
    }
}
```

### Parameter Description

| Field Name | Description |
|------------|-------------|
| idaasInstanceId | Required, IDaaS EIAM instance ID. |
| clientId | Required, IDaaS application ID, can be viewed in the corresponding IDaaS application. |
| issuer | Required, IDaaS EIAM instance Issuer endpoint, can be viewed in any M2M application under the IDaaS EIAM instance. |
| tokenEndpoint | Required, IDaaS EIAM instance token endpoint, can be viewed in any M2M application under the IDaaS EIAM instance. |
| scope | Required, specifies the audience identifier and permission identifier of the M2M server application to access, format is `audience\|scope`. <br>For scenarios of obtaining STS Token or credentials of RAM roles hosted in IDaaS, it is fixed to `urn:cloud:idaas:pam\|.all`, representing the built-in scope of IDaaS. |
| openApiEndpoint | Optional, IDaaS OpenAPI address, used when using OpenAPI authentication. Service address can be obtained from [IDaaS EIAM - Alibaba Cloud OpenAPI Developer Portal](https://api.aliyun.com/product/Eiam). <br>If the application is deployed in Alibaba Cloud VPC and in the same region as the IDaaS instance, it can be accessed via intranet VPC address, see VPC address in Alibaba Cloud OpenAPI Developer Portal. |
| developerApiEndpoint | Optional, IDaaS DeveloperAPI address, used when obtaining STS Token or credentials of RAM roles hosted in IDaaS. Service address can be obtained from [IDaaS EIAM - Alibaba Cloud OpenAPI Developer Portal](https://api.aliyun.com/product/Eiam). <br>If the application is deployed in Alibaba Cloud VPC and in the same region as the IDaaS instance, it can be accessed via intranet VPC address, see VPC address in Alibaba Cloud OpenAPI Developer Portal. |
| authnConfiguration | - identityType: Optional, default value is `CLIENT`, currently only supports `CLIENT`, meaning M2M client application authenticates with machine identity. <br>- authnMethod: Required, authentication method. Different authentication methods require different authnConfiguration fields, see **authnMethod Field Values and authnConfiguration Field Mapping** for details. |
| httpConfiguration | HTTP protocol related configuration, contains 2 fields: <br>- connectTimeout: Optional, maximum wait time for client to establish connection with server (milliseconds), default is 5000. <br>- readTimeout: Optional, maximum wait time for client to wait for server data after connection is established (milliseconds), default is 10000. |

### authnMethod Field Values and authnConfiguration Field Mapping

| authnMethod | Required authnConfiguration Field | authnConfiguration Field Description                                                                                                                                                                                                                                                                                     |
|-------------|-----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CLIENT_SECRET_BASIC | clientSecretEnvVarName | Field value is the environment variable name, through which the M2M client application's Client Secret is read.                                                                                                                                                                                                          |
| CLIENT_SECRET_POST | clientSecretEnvVarName | Field value is the environment variable name, through which the M2M client application's Client Secret is read.                                                                                                                                                                                                          |
| CLIENT_SECRET_JWT | clientSecretEnvVarName | Field value is the environment variable name, through which the M2M client application's Client Secret is read.                                                                                                                                                                                                          |
| PRIVATE_KEY_JWT | privateKeyEnvVarName | Field value is the environment variable name, through which the M2M client application's Private Key is read.                                                                                                                                                                                                            |
| PKCS7 | applicationFederatedCredentialName | PKCS7 federated credential name. Federated trust source needs to be created in advance, related configuration can be referenced: Create Federated Credential.                                                                                                                                                            |
| PKCS7 | clientDeployEnvironment | Deployment environment, currently only supports `ALIBABA_CLOUD_ECS`.                                                                                                                                                                                                                                                     |
| OIDC | applicationFederatedCredentialName | OIDC federated credential name. Federated trust source needs to be created in advance, related configuration can be referenced: Create Federated Credential.                                                                                                                                                             |
| OIDC | clientDeployEnvironment | Deployment environment, currently only supports `KUBERNETES`.                                                                                                                                                                                                                                                            |
| OIDC | oidcTokenFilePath | Optional, used to specify the Service Account Token file path. If not configured, it will try to read the path through the environment variable specified by oidcTokenFilePathEnvVarName; if both are not set, it will use the Kubernetes standard path by default: /var/run/secrets/kubernetes.io/serviceaccount/token. |
| OIDC | oidcTokenFilePathEnvVarName | Optional, takes effect when oidcTokenFilePath is not specified, field value is the environment variable name, through which the Service Account Token file path is read.                                                                                                                                                 |
| PCA | applicationFederatedCredentialName | PCA federated credential name. Federated trust source needs to be created in advance, related configuration can be referenced: Create Federated Credential.                                                                                                                                                              |
| PCA | clientX509Certificate | End certificate, format: <br>`-----BEGIN CERTIFICATE----- xxx -----END CERTIFICATE-----`                                                                                                                                                                                                                                 |
| PCA | x509CertChains | Intermediate certificate list, multiple certificates are concatenated with newlines, format: <br>`-----BEGIN CERTIFICATE----- xxx -----END CERTIFICATE----- -----BEGIN CERTIFICATE----- xxx -----END CERTIFICATE-----`                                                                                                   |
| PCA | privateKeyEnvVarName | Field value is the environment variable name, through which the M2M client application's Private Key is read.                                                                                                                                                                                                            |
| PLUGIN | pluginName | pluginName is the extension plugin name, currently only supports `alibabacloudPluginCredentialProvider`, which is Alibaba Cloud OpenAPI authentication method.<br> *Configure RAM permissions, refer to [Alibaba Cloud OpenAPI Authentication](https://help.aliyun.com/zh/idaas/eiam/developer-reference/alibaba-cloud-openapi-authentication).                                                                                                                                                     |

## Configuration Examples

Configuration examples for different authentication methods.

### Client Secret Credential Configuration Example

```json
{
    "idaasInstanceId": "idaas_ue2jvisn35ea5lmthk267xxxxx",
    "clientId": "app_mkv7rgt4d7i4u7zqtzev2mxxxx",
    "issuer": "https://xxx/api/v2/iauths_system/oauth2",
    "tokenEndpoint": "https://xxx/api/v2/iauths_system/oauth2/token",
    "scope": "api.example.com|read:file",
    "authnConfiguration": {
        "identityType": "CLIENT",
        "authnMethod": "CLIENT_SECRET_BASIC",
        "clientSecretEnvVarName": "IDAAS_CLIENT_SECRET"
    },
    "httpConfiguration": {
        "connectTimeout": 5000,
        "readTimeout": 10000
    }
}
```

### Private Key Credential Configuration Example

```json
{
    "idaasInstanceId": "idaas_ue2jvisn35ea5lmthk267xxxxx",
    "clientId": "app_mkv7rgt4d7i4u7zqtzev2mxxxx",
    "issuer": "https://xxx/api/v2/iauths_system/oauth2",
    "tokenEndpoint": "https://xxx/api/v2/iauths_system/oauth2/token",
    "scope": "api.example.com|read:file",
    "authnConfiguration": {
        "identityType": "CLIENT",
        "authnMethod": "PRIVATE_KEY_JWT",
        "privateKeyEnvVarName": "ENV_PRIVATE_KEY"
    },
    "httpConfiguration": {
        "connectTimeout": 5000,
        "readTimeout": 10000
    }
}
```

### PKCS7 Federated Credential Configuration Example

```json
{
    "idaasInstanceId": "idaas_ue2jvisn35ea5lmthk267xxxxx",
    "clientId": "app_mkv7rgt4d7i4u7zqtzev2mxxxx",
    "issuer": "https://xxx/api/v2/iauths_system/oauth2",
    "tokenEndpoint": "https://xxx/api/v2/iauths_system/oauth2/token",
    "scope": "api.example.com|read:file",
    "authnConfiguration": {
        "identityType": "CLIENT",
        "authnMethod": "PKCS7",
        "applicationFederatedCredentialName": "your_pkcs7_federated_credential_name",
        "clientDeployEnvironment": "ALIBABA_CLOUD_ECS"
    },
    "httpConfiguration": {
        "connectTimeout": 5000,
        "readTimeout": 10000
    }
}
```

### OIDC Federated Credential Configuration Example

```json
{
    "idaasInstanceId": "idaas_ue2jvisn35ea5lmthk267xxxxx",
    "clientId": "app_mkv7rgt4d7i4u7zqtzev2mxxxx",
    "issuer": "https://xxx/api/v2/iauths_system/oauth2",
    "tokenEndpoint": "https://xxx/api/v2/iauths_system/oauth2/token",
    "scope": "api.example.com|read:file",
    "authnConfiguration": {
        "identityType": "CLIENT",
        "authnMethod": "OIDC",
        "applicationFederatedCredentialName": "your_oidc_federated_credential_name",
        "clientDeployEnvironment": "KUBERNETES",
        "oidcTokenFilePath": "/var/run/secrets/.../token",
        "oidcTokenFilePathEnvVarName": "ENV_OIDC_TOKEN_FILE_PATH"
    },
    "httpConfiguration": {
        "connectTimeout": 5000,
        "readTimeout": 10000
    }
}
```

### PCA Federated Credential Configuration Example

```json
{
    "idaasInstanceId": "idaas_ue2jvisn35ea5lmthk267xxxxx",
    "clientId": "app_mkv7rgt4d7i4u7zqtzev2mxxxx",
    "issuer": "https://xxx/api/v2/iauths_system/oauth2",
    "tokenEndpoint": "https://xxx/api/v2/iauths_system/oauth2/token",
    "scope": "api.example.com|read:file",
    "authnConfiguration": {
        "identityType": "CLIENT",
        "authnMethod": "PCA",
        "applicationFederatedCredentialName": "your_pca_federated_credential_name",
        "clientX509Certificate": "-----BEGIN CERTIFICATE-----\nxxxxxx\n-----END CERTIFICATE-----",
        "x509CertChains": "-----BEGIN CERTIFICATE-----\nxxxxxx\n-----END CERTIFICATE-----\n-----BEGIN CERTIFICATE-----\nxxxxxx\n-----END CERTIFICATE-----",
        "privateKeyEnvVarName": "ENV_PRIVATE_KEY"
    },
    "httpConfiguration": {
        "connectTimeout": 5000,
        "readTimeout": 10000
    }
}
```

### OpenAPI Authentication Configuration Example

```json
{
    "idaasInstanceId": "idaas_ue2jvisn35ea5lmthk267xxxxx",
    "clientId": "app_mkv7rgt4d7i4u7zqtzev2mxxxx",
    "issuer": "https://xxx/api/v2/iauths_system/oauth2",
    "tokenEndpoint": "https://xxx/api/v2/iauths_system/oauth2/token",
    "scope": "api.example.com|read:file",
    "openApiEndpoint": "eiam.[region_id].aliyuncs.com",
    "authnConfiguration": {
        "identityType": "CLIENT",
        "authnMethod": "PLUGIN",
        "pluginName": "alibabacloudPluginCredentialProvider"
    },
    "httpConfiguration": {
        "connectTimeout": 5000,
        "readTimeout": 10000
    }
}
```

## Code Integration

### SDK Initialization

Read the configuration file specified during the environment setup phase and complete the IDaaS configuration initialization.

```python
from cloud_idaas.core import IDaaSCredentialProviderFactory

IDaaSCredentialProviderFactory.init()
```

> **Important**:
> - All SDK features depend on the `init()` initialization method, so the `init()` method must be completed first, otherwise getting `IDaaSCredentialProvider` will fail and cause business interruption.
> - Initialization will check the configuration and obtain the Access Token for the scope specified in the configuration file. If the configuration is missing or incorrect, causing the Access Token acquisition to fail, it will directly report an error and cause business interruption.

### Get Access Token

1. Get IDaaS credentialProvider to obtain Access Token.

   - Get IDaaS credentialProvider through no-argument constructor to obtain Access Token for the scope specified in the configuration file:

     ```python
     credential_provider = IDaaSCredentialProviderFactory.get_idaas_credential_provider()
     ```

   - Get IDaaS credentialProvider through parameterized constructor, scope can be specified to obtain Access Token for the specified scope. Format is `audience|scope`, corresponding to the audience identifier and permission identifier of the M2M server application to access:

     ```python
     credential_provider = IDaaSCredentialProviderFactory.get_idaas_credential_provider(scope)
     ```

2. Access Token is of Bearer type, obtained through the `get_bearer_token()` method of credentialProvider:

   ```python
   access_token = credential_provider.get_bearer_token()
   ```

### Code Example

For complete examples, see the `samples/` directory:

- `samples/client_secret_authentication.py` - Get Access Token example

```python
from cloud_idaas.core import IDaaSCredentialProviderFactory

def main():
    # Initialize the factory with configuration
    IDaaSCredentialProviderFactory.init()

    # Get credential provider with scope from config file
    # credential_provider = IDaaSCredentialProviderFactory.get_idaas_credential_provider()

    # scope format: <audience>|<scope>
    scope = "api.example.com|read:file"
    # Get credential provider with scope specified by parameter
    credential_provider = IDaaSCredentialProviderFactory.get_idaas_credential_provider(scope)

    access_token = credential_provider.get_bearer_token()

    print(access_token)

if __name__ == "__main__":
    main()
```

## Token Exchange

Token Exchange (RFC 8693) allows you to exchange a subject token for a new access token with different scopes or audiences. This is useful for token downgrading and service-to-service access scenarios.

### Basic Token Exchange

For complete examples, see the `samples/` directory:

- `samples/token_exchange_with_client_secret_authentication.py` - Token exchange example

```python
from cloud_idaas.core import IDaaSCredentialProviderFactory, OAuth2Constants

def main():
    # Initialize the factory with configuration
    IDaaSCredentialProviderFactory.init()

    # The subject token to exchange
    subject_token = ""

    # Get token exchange credential provider with scope from config file
    # token_exchange_provider = IDaaSCredentialProviderFactory.get_idaas_token_exchange_credential_provider()

    # scope format: <audience>|<scope>
    scope = "api.example.com|read:file"
    # Get token exchange credential provider with scope specified by parameter
    token_exchange_provider = IDaaSCredentialProviderFactory.get_idaas_token_exchange_credential_provider_by_scope(scope)

    # Perform token exchange
    access_token = token_exchange_provider.get_issued_token(
        subject_token,
        OAuth2Constants.ACCESS_TOKEN_TYPE_VALUE,
    )

    print(access_token)

if __name__ == "__main__":
    main()
```

### Token Exchange Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| subject_token | str | Yes | The token to exchange |
| subject_token_type | str | Yes | Subject token type (e.g., `urn:ietf:params:oauth:token-type:access_token`) |
| requested_token_type | str | No | Requested token type (default is access token) |

### Use Cases

1. **Token Downgrading**: Exchange a token with broader permissions for a token with limited scope
2. **Service-to-Service Access**: Pass the same user identity between services to obtain the required access token

## Support and Feedback

- **Email**: cloudidaas@list.alibaba-inc.com
- **Issues**: Please submit an Issue for questions or suggestions

## License

This project is licensed under the [Apache License 2.0](LICENSE).
