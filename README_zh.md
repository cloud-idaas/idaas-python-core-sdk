# cloud-idaas-core

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Development Status](https://img.shields.io/badge/status-Beta-orange)](https://pypi.org/project/cloud-idaas-core/)

[English](README.md)

IDaaS（身份即服务）M2M 产品的 Python SDK，为开发者提供便捷的机器对机器认证能力。

## 功能特性

- **多种认证方式**：支持 JWT Client Secret、JWT Private Key、OIDC Token、PKCS7 可信文档等多种 M2M 认证方式
- **智能缓存机制**：内置凭证缓存策略，支持预取和过期值处理，减少不必要的网络请求
- **灵活配置**：支持配置文件、环境变量和编程方式配置
- **插件扩展**：支持自定义凭证提供者以应对特殊场景
- **云原生支持**：内置阿里云 ECS 和阿里云 ACK 的可信文档支持
- **令牌交换（RFC 8693）**：支持令牌交换以获取不同 scope 或 audience 的访问令牌，适用于令牌降权和服务间调用场景

## 环境要求

- Python >= 3.9
- 依赖：
  - requests >= 2.31.0
  - cryptography >= 44.0.0
  - PyJWT >= 2.8.0
  - urllib3 >= 2.5.0

## 安装

```bash
pip install cloud-idaas-core
```

## 快速开始

> **重要提示**：在使用任何 SDK 功能之前，必须调用 `IDaaSCredentialProviderFactory.init()` 初始化 SDK。此步骤是**必需的**，应在应用启动时执行一次。

### 1. 配置文件

创建配置文件 `~/.cloud_idaas/client_config.json`：

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

### 2. 环境变量

设置环境变量：

```bash
export IDAAS_CLIENT_SECRET="your-client-secret"
```

### 3. 代码中使用

```python
from cloud_idaas.core import IDaaSCredentialProviderFactory

# 初始化（自动加载配置文件）
IDaaSCredentialProviderFactory.init()

# 获取凭证提供者
credential_provider = IDaaSCredentialProviderFactory.get_idaas_credential_provider()

# 获取访问令牌
access_token = credential_provider.get_bearer_token()
print(f"Access Token: {access_token}")
```

## 配置详情

### 配置文件路径

SDK 按以下顺序查找配置文件：

1. 初始化时传入路径：`IDaaSCredentialProviderFactory.init("/.../client-config.json")`
2. 环境变量路径：`CLOUD_IDAAS_CONFIG_PATH=/.../client-config.json`
3. 默认路径：`~/.cloud_idaas/client-config.json`

### 完整配置示例

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

### 配置项说明

| 配置项 | 类型 | 必填 | 说明 |
|-------------------|------|----------|-------------|
| idaasInstanceId | string | 是 | IDaaS 实例 ID |
| clientId | string | 是 | 用于认证的客户端 ID |
| issuer | string | 是 | OAuth2 签发者 URL |
| tokenEndpoint | string | 是 | OAuth2 令牌端点 URL |
| scope | string | 否 | 请求的 scope |
| openApiEndpoint | string | 否 | OpenAPI 端点 |
| developerApiEndpoint | string | 否 | 开发者 API 端点 |
| authnConfiguration | object | 是 | 认证配置 |
| httpConfiguration | object | 否 | HTTP 客户端配置 |

### Scope 格式

SDK 使用特定的 scope 格式，audience 和 scope 值通过 `|` 分隔：

```
audience|scope_value
```

示例：
- `api.example.com|read:file`
- `api.example.com|write:file`
- `resource.server|admin`

可以请求同一 audience 的多个 scope 值：
```
api.example.com|read:file api.example.com|write:file
```

**注意**：不支持在单个请求中使用多个 audience。

## 认证方式

### 客户端密钥认证

使用客户端密钥进行认证。支持 `CLIENT_SECRET_BASIC`、`CLIENT_SECRET_POST` 和 `CLIENT_SECRET_JWT` 方式。

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

### 私钥认证

使用私钥进行认证，提供更高的安全性。

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

### PKCS7 联邦认证

在云环境中使用 PKCS7 可信文档进行认证。

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

### OIDC 联邦认证

使用 OIDC 令牌进行认证。

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

### PCA（X.509 证书）认证

使用 X.509 证书进行认证。

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

### 插件认证

使用基于插件的凭证提供者进行认证。

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


## 令牌交换

令牌交换（RFC 8693）允许您将主体令牌交换为具有不同 scope 或 audience 的新访问令牌。这适用于令牌降权和服务间调用场景。

### 基本令牌交换

完整示例请参考 `samples/` 目录：

- `samples/token_exchange_with_client_secret_authentication.py` - 使用客户端密钥认证的令牌交换

```python
from cloud_idaas.core import IDaaSCredentialProviderFactory, OAuth2Constants

# 初始化工厂
IDaaSCredentialProviderFactory.init()

# 获取令牌交换凭证提供者（scope 从配置文件读取）
token_exchange_provider = IDaaSCredentialProviderFactory.get_token_exchange_credential_provider()

# 或通过参数指定 scope
# token_exchange_provider = IDaaSCredentialProviderFactory.get_token_exchange_credential_provider_by_scope("api://target-service|read api://target-service|write")

# 交换主体令牌获取访问令牌
access_token = token_exchange_provider.get_issued_token(
    subject_token="your_subject_token",
    subject_token_type=OAuth2Constants.ACCESS_TOKEN_TYPE_VALUE,
)
```

### 令牌交换参数

| 参数 | 类型 | 必填 | 说明 |
|-----------|------|----------|-------------|
| subject_token | string | 是 | 待交换的令牌 |
| subject_token_type | string | 是 | 主体令牌类型（如 `urn:ietf:params:oauth:token-type:access_token`） |
| requested_token_type | string | 否 | 请求的令牌类型（默认为访问令牌） |

### 使用场景

1. **令牌降权**：将具有较大权限的令牌交换为具有较小权限（更窄 scope）的令牌
2. **服务间调用**：同一用户身份在不同服务间传递，换取目标服务所需的访问令牌

### 支持的认证方式

令牌交换支持以下认证方式：

- `CLIENT_SECRET_BASIC` - 客户端密钥通过 HTTP Basic Auth 头部发送
- `CLIENT_SECRET_POST` - 客户端密钥通过请求体发送
- `CLIENT_SECRET_JWT` - 使用客户端密钥签名的 JWT 断言
- `PRIVATE_KEY_JWT` - 使用私钥签名的 JWT 断言
- `PKCS7` - PKCS7 可信文档
- `OIDC` - OIDC 令牌
- `PCA` - X.509 证书认证

**注意**：`PLUGIN` 认证方式目前不支持令牌交换。

## 支持与反馈

- **邮箱**：cloudidaas@list.alibaba-inc.com
- **问题反馈**：请提交 Issue 进行问题反馈或建议

## 许可证

本项目基于 [Apache License 2.0](LICENSE) 许可证。
