# cloud-idaas-core

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Development Status](https://img.shields.io/badge/status-Beta-orange)](https://pypi.org/project/cloud-idaas-core/)

[简体中文](README_zh.md)

Python SDK for IDaaS (Identity as a Service) M2M product, providing developers with convenient machine-to-machine authentication capabilities.

## Features

- **Multiple Authentication Methods**: Supports JWT Client Secret, JWT Private Key, OIDC Token, PKCS7 Attested Document, and other M2M authentication methods
- **Intelligent Caching Mechanism**: Built-in credential caching strategy with prefetch and stale value handling to reduce unnecessary network requests
- **Flexible Configuration**: Supports configuration files, environment variables, and programmatic configuration
- **Plugin Extensions**: Supports custom credential providers for special scenarios
- **Cloud-Native Support**: Built-in attested document support for Alibaba Cloud ECS and Alibaba cloud ACK
- **Token Exchange (RFC 8693)**: Exchange tokens for different scopes or audiences, supporting token downscoping and service-to-service access scenarios

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
```

## Quick Start

> **Important**: Before using any SDK features, you must call `IDaaSCredentialProviderFactory.init()` to initialize the SDK. This step is **required** and should be done once at application startup.

### 1. Configuration File

Create a configuration file `~/.cloud_idaas/client_config.json`:

```json
{
    "idaasInstanceId": "your-idaas-instance-id",
    "clientId": "your-client-id",
    "issuer": "your-idaas-issuer-url",
    "tokenEndpoint": "your-idaas-token-endpoint",
    "scope": "your-requested-scope",
    "developerApiEndpoint": "your-developer-api-endpoint",
    "authnConfiguration": {
        "authenticationSubject": "CLIENT",
        "authnMethod": "CLIENT_SECRET_POST",
        "clientSecretEnvVarName": "IDAAS_CLIENT_SECRET"
    }
}
```

### 2. Environment Variables

Set environment variables:

```bash
export IDAAS_CLIENT_SECRET="your-client-secret"
```

### 3. Use in code

```python
from cloud_idaas.core import IDaaSCredentialProviderFactory

# Initialize (automatically loads configuration file)
IDaaSCredentialProviderFactory.init()

# Get credential provider
credential_provider = IDaaSCredentialProviderFactory.get_idaas_credential_provider()

# Get access token
access_token = credential_provider.get_bearer_token()
print(f"Access Token: {access_token}")
```

## Configuration Details

### Configuration File Paths

The SDK searches for configuration files in the following order:

1. Pass path during initialization: `IDaaSCredentialProviderFactory.init("/.../client-config.json")`
2. Environment variable path: `CLOUD_IDAAS_CONFIG_PATH=/.../client-config.json`
3. Default path: `~/.cloud_idaas/client-config.json`

### Complete Configuration Example

```json
{
    "idaasInstanceId": "idaas_ue2jvisn35ea5lmthk267xxxxx"
    "clientId": "app_mkv7rgt4d7i4u7zqtzev2mxxxx"
    "issuer":"https://xxx/api/v2/iauths_system/oauth2",               
    "tokenEndpoint": "https://xxx/api/v2/iauths_system/oauth2/token",
    "scope": "api.example.com|read:file",
    "openApiEndpoint":"eiam.[region_id].aliyuncs.com",
    "developerApiEndpoint":"eiam-developerapi.[region_id].aliyuncs.com",
    "authnConfiguration": {
        "authenticationSubject": "CLIENT",
        "authnMethod": "CLIENT_SECRET_POST",
        "clientSecretEnvVarName": "IDAAS_CLIENT_SECRET"
    },
    "httpConfiguration": {
        "connectTimeout": 5000,
        "readTimeout": 10000
    }
}
```

### Configuration Items

| Configuration Item | Type | Required | Description |
|-------------------|------|----------|-------------|
| idaasInstanceId | string | Yes | IDaaS instance ID |
| clientId | string | Yes | Client ID for authentication |
| issuer | string | Yes | OAuth2 issuer URL |
| tokenEndpoint | string | Yes | OAuth2 token endpoint URL |
| scope | string | No | Requested scope  |
| openApiEndpoint | string | No | OpenAPI endpoint |
| developerApiEndpoint | string | No | Developer API endpoint |
| authnConfiguration | object | Yes | Authentication configuration |
| httpConfiguration | object | No | HTTP client configuration |

### Scope Format

The SDK uses a specific scope format with audience and scope values separated by `|`:

```
audience|scope_value
```

Examples:
- `api.example.com|read:file`
- `api.example.com|write:file`
- `resource.server|admin`

Multiple scope values for the same audience can be requested:
```
api.example.com|read:file api.example.com|write:file
```

**Note**: Multiple audiences in a single request are not supported.

## Authentication Methods

### Client Secret Authentication

Use Client Secret for authentication. Supports `CLIENT_SECRET_BASIC`, `CLIENT_SECRET_POST`, and `CLIENT_SECRET_JWT` methods.

```json
{
    "idaasInstanceId": "idaas_ue2jvisn35ea5lmthk267xxxxx"
    "clientId": "app_mkv7rgt4d7i4u7zqtzev2mxxxx"
    "issuer": "your-idaas-issuer-url",
    "tokenEndpoint": "your-idaas-token-endpoint",
    "scope": "your-requested-scope",
    "openApiEndpoint": "eiam.[region_id].aliyuncs.com",
    "developerApiEndpoint": "eiam-developerapi.[region_id].aliyuncs.com",
    "authnConfiguration": {
        "authenticationSubject": "CLIENT",
        "authnMethod": "CLIENT_SECRET_POST",
        "clientSecretEnvVarName": "IDAAS_CLIENT_SECRET"
    },
    "httpConfiguration": {
        "connectTimeout": 5000,
        "readTimeout": 10000
    }
}
```

### Private Key Authentication

Use private key for authentication, offering higher security.

```json
{
    "idaasInstanceId": "idaas_ue2jvisn35ea5lmthk267xxxxx"
    "clientId": "app_mkv7rgt4d7i4u7zqtzev2mxxxx"
    "issuer": "your-idaas-issuer-url",
    "tokenEndpoint": "your-idaas-token-endpoint",
    "scope": "your-requested-scope",
    "openApiEndpoint": "eiam.[region_id].aliyuncs.com",
    "developerApiEndpoint": "eiam-developerapi.[region_id].aliyuncs.com",
    "authnConfiguration": {
        "authenticationSubject": "CLIENT",
        "authnMethod": "PRIVATE_KEY_JWT",
        "privateKeyEnvVarName": "IDAAS_PRIVATE_KEY"
    },
    "httpConfiguration": {
        "connectTimeout": 5000,
        "readTimeout": 10000
    }
}
```

### PKCS7 Federated Authentication

Use PKCS7 attested document for authentication in cloud environments.

```json
{
    "idaasInstanceId": "idaas_ue2jvisn35ea5lmthk267xxxxx"
    "clientId": "app_mkv7rgt4d7i4u7zqtzev2mxxxx"
    "issuer": "your-idaas-issuer-url",
    "tokenEndpoint": "your-idaas-token-endpoint",
    "scope": "your-requested-scope",
    "openApiEndpoint": "eiam.[region_id].aliyuncs.com",
    "developerApiEndpoint": "eiam-developerapi.[region_id].aliyuncs.com",
    "authnConfiguration": {
        "authenticationSubject": "CLIENT",
        "authnMethod": "PKCS7",
        "applicationFederatedCredentialName": "your-pkcs7-credential-name",
        "clientDeployEnvironment": "ALIBABA_CLOUD_ECS"
    },
    "httpConfiguration": {
        "connectTimeout": 5000,
        "readTimeout": 10000
    }
}
```

### OIDC Federated Authentication

Use OIDC token for authentication.

```json
{
    "idaasInstanceId": "idaas_ue2jvisn35ea5lmthk267xxxxx"
    "clientId": "app_mkv7rgt4d7i4u7zqtzev2mxxxx"
    "issuer": "your-idaas-issuer-url",
    "tokenEndpoint": "your-idaas-token-endpoint",
    "scope": "your-requested-scope",
    "openApiEndpoint": "eiam.[region_id].aliyuncs.com",
    "developerApiEndpoint": "eiam-developerapi.[region_id].aliyuncs.com",
    "authnConfiguration": {
        "authenticationSubject": "CLIENT",
        "authnMethod": "OIDC",
        "applicationFederatedCredentialName": "your-oidc-credential-name",
        "clientDeployEnvironment": "KUBERNETES"
    },
    "httpConfiguration": {
        "connectTimeout": 5000,
        "readTimeout": 10000
    }
}
```

### PCA (X.509 Certificate) Authentication

Use X.509 certificate for authentication.

```json
{
    "idaasInstanceId": "idaas_ue2jvisn35ea5lmthk267xxxxx"
    "clientId": "app_mkv7rgt4d7i4u7zqtzev2mxxxx"
    "issuer": "your-idaas-issuer-url",
    "tokenEndpoint": "your-idaas-token-endpoint",
    "scope": "your-requested-scope",
    "openApiEndpoint": "eiam.[region_id].aliyuncs.com",
    "developerApiEndpoint": "eiam-developerapi.[region_id].aliyuncs.com",
    "authnConfiguration": {
        "authenticationSubject": "CLIENT",
        "authnMethod": "PCA",
        "clientX509Certificate": "-----BEGIN CERTIFICATE-----\nxxx\n-----END CERTIFICATE-----",
        "x509CertChains": "-----BEGIN CERTIFICATE-----\nxxx\n-----END CERTIFICATE-----",
        "privateKeyEnvVarName": "IDAAS_PRIVATE_KEY"
    },
    "httpConfiguration": {
        "connectTimeout": 5000,
        "readTimeout": 10000
    }
}
```

### Plugin Authentication

Use plugin-based credential provider for authentication.

```json
{
    "idaasInstanceId": "idaas_ue2jvisn35ea5lmthk267xxxxx"
    "clientId": "app_mkv7rgt4d7i4u7zqtzev2mxxxx"
    "issuer": "your-idaas-issuer-url",
    "tokenEndpoint": "your-idaas-token-endpoint",
    "scope": "your-requested-scope",
    "openApiEndpoint": "eiam.[region_id].aliyuncs.com",
    "developerApiEndpoint": "eiam-developerapi.[region_id].aliyuncs.com",
    "authnConfiguration": {
        "authenticationSubject": "CLIENT",
        "authnMethod": "PLUGIN",
        "pluginName": "alibabacloudPluginCredentialProvider"
    },
    "httpConfiguration": {
        "connectTimeout": 5000,
        "readTimeout": 10000
    }
}
```


## Token Exchange

Token Exchange (RFC 8693) allows you to exchange a subject token for a new access token with different scope or audience. This is useful for token downscoping and service-to-service access scenarios.

### Basic Token Exchange

For working examples, see the `samples/` directory:

- `samples/token_exchange_with_client_secret_authentication.py` - Token Exchange with client secret authentication

```python
from cloud_idaas.core import IDaaSCredentialProviderFactory, OAuth2Constants

# Initialize the factory
IDaaSCredentialProviderFactory.init()

# Get Token Exchange credential provider (scope from config file)
token_exchange_provider = IDaaSCredentialProviderFactory.get_token_exchange_credential_provider()

# Or get with specific scope
# token_exchange_provider = IDaaSCredentialProviderFactory.get_token_exchange_credential_provider_by_scope("api://target-service|read api://target-service|write")

# Exchange subject token for access token
access_token = token_exchange_provider.get_issued_token(
    subject_token="your_subject_token",
    subject_token_type=OAuth2Constants.ACCESS_TOKEN_TYPE_VALUE,
)
```

### Token Exchange Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| subject_token | string | Yes | The token to be exchanged |
| subject_token_type | string | Yes | Type of the subject token (e.g., `urn:ietf:params:oauth:token-type:access_token`) |
| requested_token_type | string | No | Type of token requested (defaults to access token) |

### Use Cases

1. **Token Downscoping**: Exchange a token with broader permissions for one with limited scope
2. **Service-to-Service Access**: Transfer the same user identity across services to obtain the required access token

### Supported Authentication Methods

Token Exchange supports the following authentication methods:

- `CLIENT_SECRET_BASIC` - Client secret in HTTP Basic Auth header
- `CLIENT_SECRET_POST` - Client secret in request body
- `CLIENT_SECRET_JWT` - JWT assertion signed with client secret
- `PRIVATE_KEY_JWT` - JWT assertion signed with private key
- `PKCS7` - PKCS7 attested document
- `OIDC` - OIDC token
- `PCA` - X.509 certificate authentication

**Note**: `PLUGIN` authentication method is currently not supported for Token Exchange.

## Support and Feedback

- **Email**: cloudidaas@list.alibaba-inc.com
- **Issues**: Please submit an Issue for questions or suggestions

## License

This project is licensed under the [Apache License 2.0](LICENSE).