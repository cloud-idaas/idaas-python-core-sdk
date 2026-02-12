# IDaaS Python Core SDK 架构设计文档

## 1. 项目概览

**项目名称**: `cloud_idaas_core`
**版本**: 0.0.1
**Python版本要求**: >= 3.8
**许可证**: Apache-2.0
**维护团队**: Alibaba IDaaS Team

本SDK是IDaaS（Identity as a Service）M2M（Machine-to-Machine）产品的Python Core SDK，基于标准OAuth2/OIDC协议，提供从IDaaS服务获取AccessToken的核心能力。

### 核心依赖

| 依赖库 | 版本要求 | 用途 |
|---|---|---|
| `requests` | >= 2.31.0 | HTTP请求（声明依赖，实际使用urllib3） |
| `cryptography` | >= 42.0.0 | 密钥解析、加密操作 |
| `PyJWT` | >= 2.8.0 | JWT令牌签发与解析 |
| `urllib3` | >= 1.26.20 | 底层HTTP客户端实现 |

---

## 2. 项目目录结构

```
idaas-python-core-sdk/
├── cloud_idaas/                          # 顶层包
│   ├── __init__.py                       # 统一导出所有公开API
│   └── core/                             # 核心模块
│       ├── __init__.py                   # 核心模块导出(常量/异常/凭证/域对象)
│       ├── version.py                    # 版本信息
│       ├── constants.py                  # 常量与枚举定义
│       ├── credential.py                 # 凭证抽象接口与实现
│       ├── domain.py                     # 域对象(错误响应、设备码响应)
│       ├── exceptions.py                 # 异常体系
│       ├── config/                       # 配置管理模块
│       │   ├── idaas_client_config.py    # IDaaS客户端配置
│       │   ├── identity_authentication_configuration.py  # 认证配置
│       │   ├── http_configuration.py     # HTTP配置
│       │   └── user_agent_config.py      # User-Agent配置
│       ├── http/                         # HTTP通信模块
│       │   ├── http_client.py            # HTTP客户端抽象接口
│       │   ├── default_http_client.py    # 默认HTTP客户端实现(urllib3)
│       │   ├── http_request.py           # HTTP请求模型(Builder模式)
│       │   ├── http_response.py          # HTTP响应模型
│       │   ├── http_method.py            # HTTP方法枚举
│       │   ├── content_type.py           # Content-Type枚举
│       │   └── oauth2_token_util.py      # OAuth2令牌操作工具类
│       ├── provider/                     # Provider抽象接口层
│       │   ├── idaas_credential_provider.py        # 凭证Provider接口
│       │   ├── jwt_client_assertion_provider.py     # JWT断言Provider接口
│       │   ├── oidc_token_provider.py               # OIDC Token Provider接口
│       │   ├── pkcs7_attested_document_provider.py  # PKCS7文档Provider接口
│       │   └── refresh_credential_provider.py       # 刷新凭证Provider接口
│       ├── cache/                        # 缓存机制模块
│       │   ├── cached_result_supplier.py            # 缓存结果供应器(核心)
│       │   ├── refresh_result.py                    # 刷新结果封装
│       │   ├── stale_value_behavior.py              # 过期值行为策略枚举
│       │   ├── prefetch_strategy.py                 # 预取策略接口
│       │   └── strategy/                            # 具体预取策略
│       │       ├── one_caller_blocks_prefetch_strategy.py  # 单调用者阻塞策略
│       │       └── non_blocking_prefetch_strategy.py       # 非阻塞异步策略
│       ├── implementation/               # 具体实现层
│       │   ├── abstract_refreshed_credential_provider.py   # 自动刷新凭证基类
│       │   ├── idaas_machine_credential_provider.py        # M2M凭证Provider(核心实现)
│       │   └── authentication/           # 各认证方式具体实现
│       │       ├── jwt/
│       │       │   ├── static_client_secret_assertion_provider.py  # 客户端密钥JWT断言
│       │       │   └── static_private_key_assertion_provider.py   # 私钥JWT断言
│       │       ├── oidc/
│       │       │   ├── static_oidc_token_provider.py              # 静态OIDC令牌
│       │       │   └── file_oidc_token_provider.py                # 文件OIDC令牌
│       │       └── pkcs7/
│       │           ├── static_pkcs7_attested_document_provider.py        # 静态PKCS7文档
│       │           ├── alibaba_cloud_ecs_attested_document_provider.py   # 阿里云ECS PKCS7
│       │           └── aws_ec2_pkcs7_attested_document_provider.py       # AWS EC2 PKCS7(未实现)
│       ├── factory/                      # 工厂模块
│       │   └── idaas_credential_provider_factory.py  # 凭证Provider工厂
│       └── util/                         # 工具类模块
│           ├── string_util.py            # 字符串工具
│           ├── json_util.py              # JSON序列化/反序列化
│           ├── file_util.py              # 文件读写
│           ├── pki_util.py               # PKI/密钥解析
│           ├── config_reader.py          # 配置文件读取
│           ├── validator_util.py         # 配置校验
│           ├── request_util.py           # HTTP请求辅助工具
│           ├── browser_util.py           # 浏览器操作工具
│           └── exception_analyzer.py     # 异常分析工具
├── tests/                                # 测试目录(与源码结构镜像)
├── samples/                              # 示例代码
├── pyproject.toml                        # 项目构建配置
├── pytest.ini                            # 测试配置
└── requirements.txt                      # 依赖清单
```

---

## 3. 分层架构设计

SDK采用**四层分层架构**，从上到下依次为：

```
┌─────────────────────────────────────────────────────────┐
│                    用户调用层 (API Layer)                  │
│   IDaaSCredentialProviderFactory / Builder模式入口        │
├─────────────────────────────────────────────────────────┤
│                  抽象接口层 (Provider Layer)               │
│   IDaaSCredentialProvider / JwtClientAssertionProvider   │
│   OidcTokenProvider / Pkcs7AttestedDocumentProvider      │
├─────────────────────────────────────────────────────────┤
│                  实现层 (Implementation Layer)             │
│   IDaaSMachineCredentialProvider                         │
│   AbstractRefreshedCredentialProvider                    │
│   StaticClientSecretAssertionProvider / ...              │
├─────────────────────────────────────────────────────────┤
│                  基础设施层 (Infrastructure Layer)         │
│   HTTP Client / Cache / Config / Util / Exceptions      │
└─────────────────────────────────────────────────────────┘
```

### 3.1 用户调用层

`IDaaSCredentialProviderFactory` 是SDK的主入口，提供两种初始化方式：

- **`init()`**: 从配置文件自动加载（路径优先级：环境变量 `CLOUD_IDAAS_CONFIG_PATH` > 默认路径 `~/.cloud_idaas/client-config.json`）
- **`init_with_config(config)`**: 通过代码直接传入 `IDaaSClientConfig` 对象

初始化后，通过 `get_idaas_credential_provider()` 获取凭证Provider，按Scope缓存Provider实例。

### 3.2 抽象接口层

定义了四个核心Provider抽象接口，形成清晰的职责边界：

| 接口 | 职责 | 方法 |
|---|---|---|
| `IDaaSCredentialProvider` | 顶层凭证提供者 | `get_credential()`, `get_bearer_token()` |
| `JwtClientAssertionProvider` | JWT断言生成 | `get_client_assertion()` |
| `OidcTokenProvider` | OIDC令牌获取 | `get_oidc_token()` |
| `Pkcs7AttestedDocumentProvider` | PKCS7证明文档获取 | `get_attested_document()` |

**继承关系**: `IDaaSCredentialProvider` 继承自 `OidcTokenProvider`，其 `get_oidc_token()` 默认委托给 `get_bearer_token()`。

### 3.3 实现层

#### 3.3.1 IDaaSMachineCredentialProvider (核心)

这是SDK最核心的类，同时继承 `AbstractRefreshedCredentialProvider[IDaaSCredential]` 和 `IDaaSCredentialProvider`，支持7种认证方式：

| 认证方式 (TokenAuthnMethod) | 描述 | 令牌获取方式 |
|---|---|---|
| `CLIENT_SECRET_BASIC` | HTTP Basic认证 | Base64(clientId:clientSecret) 放入Authorization头 |
| `CLIENT_SECRET_POST` | 表单传递密钥 | client_secret 放入POST表单体 |
| `CLIENT_SECRET_JWT` | 客户端密钥签名JWT | HMAC-SHA256签名JWT作为client_assertion |
| `PRIVATE_KEY_JWT` | 私钥签名JWT | RSA/ECDSA签名JWT作为client_assertion |
| `PKCS7` | PKCS7证明文档 | 从云平台元数据服务获取PKCS7文档 |
| `OIDC` | OIDC联邦凭证 | 从文件或静态配置获取OIDC Token |
| `PCA` | 私有CA证书 | X509证书链 + 私钥签名JWT |

**Builder模式**: `IDaaSMachineCredentialProviderBuilder` 提供流式API构建Provider实例。

#### 3.3.2 认证方式具体实现

**JWT认证**:
- `StaticClientSecretAssertionProvider`: 使用客户端密钥(HS256)签发JWT断言，claims包含 aud/sub/iss/jti/iat/exp
- `StaticPrivateKeyAssertionProvider`: 使用私钥(RS256/ES256)签发JWT断言，通过 `PkiUtil` 解析PEM格式私钥

**OIDC认证**:
- `StaticOidcTokenProvider`: 持有预配置的静态OIDC Token
- `FileOidcTokenProvider`: 从文件系统读取OIDC Token，支持过期检测（10分钟阈值）和自动重新读取

**PKCS7认证**:
- `StaticPkcs7AttestedDocumentProvider`: 持有预配置的静态PKCS7文档
- `AlibabaCloudEcsAttestedDocumentProvider`: 从阿里云ECS元数据服务(`100.100.100.200`)获取PKCS7证明文档，继承 `AbstractRefreshedCredentialProvider` 实现自动刷新
- `AwsEc2Pkcs7AttestedDocumentProvider`: AWS EC2的PKCS7实现（尚未实现，调用时抛出异常）

---

## 4. 缓存与自动刷新机制

缓存是SDK的核心设计之一，确保令牌能在过期前自动刷新，避免频繁请求IDaaS服务。

### 4.1 架构图

```
┌──────────────────────────────────────────────────────────┐
│              CachedResultSupplier<T>                      │
│                                                          │
│  ┌─────────────┐   ┌────────────────┐   ┌─────────────┐ │
│  │ RefreshResult│   │ PrefetchStrategy│   │  StaleValue │ │
│  │ (value,      │   │                │   │  Behavior   │ │
│  │  stale_time, │   │  ┌───────────┐ │   │ ┌─────────┐ │ │
│  │  prefetch_   │   │  │OneCallerBl│ │   │ │ STRICT  │ │ │
│  │  time)       │   │  │ocks       │ │   │ │ ALLOW   │ │ │
│  │             │   │  ├───────────┤ │   │ └─────────┘ │ │
│  │             │   │  │NonBlocking│ │   │             │ │
│  └─────────────┘   │  └───────────┘ │   └─────────────┘ │
│                     └────────────────┘                    │
└──────────────────────────────────────────────────────────┘
```

### 4.2 核心类: CachedResultSupplier\<T\>

这是基于时间的缓存核心，管理缓存值的生命周期：

**三个关键时间点**:
- **当前时间**: 每次 `get()` 调用时获取
- **prefetch_time (预取时间)**: 到达此时间后触发异步/同步预取刷新
- **stale_time (过期时间)**: 到达此时间后缓存被视为过期，所有调用者阻塞等待刷新

**时间线**:
```
Token获取 ───── prefetch_time ───── stale_time ───── 令牌真正过期
   │                 │                   │
   │    正常返回缓存   │   触发预取刷新     │  强制阻塞刷新
```

**令牌刷新时间计算** (在 `IDaaSMachineCredentialProvider._refresh_credential` 中):
- `stale_time = expires_at - expires_in / 5` (令牌有效期的4/5处)
- `prefetch_time = expires_at - expires_in / 3` (令牌有效期的2/3处)

**Jitter机制**: 为避免多实例同时刷新造成的"惊群效应"，`CachedResultSupplier` 对 stale_time 和 prefetch_time 添加随机抖动（5~10分钟）。

**线程安全**: 使用 `threading.Lock` 保护刷新操作，最长等待5秒(`BLOCKING_REFRESH_MAX_WAIT`)。

### 4.3 预取策略

| 策略 | 类名 | 行为 | 适用场景 |
|---|---|---|---|
| 同步阻塞 | `OneCallerBlocksPrefetchStrategy` | 一个调用者阻塞执行刷新，其他调用者直接返回旧值 | 默认策略，低并发场景 |
| 异步非阻塞 | `NonBlockingPrefetchStrategy` | 后台线程池异步执行刷新，所有调用者立即返回旧值 | 高并发、对延迟敏感场景 |

`NonBlockingPrefetchStrategy` 使用全局 `ThreadPoolExecutor`（单线程）和 `Semaphore`（最大100并发）控制刷新并发度。

### 4.4 过期值行为策略

| 策略 | 行为 |
|---|---|
| `STRICT` | 刷新失败时抛出 `CacheException` |
| `ALLOW` | 刷新失败时返回旧的缓存值，打印警告日志 |

---

## 5. HTTP通信层

### 5.1 设计模式

- **抽象接口**: `HttpClient`（ABC）定义 `send(request) -> HttpResponse`
- **默认实现**: `DefaultHttpClient` 基于 `urllib3.PoolManager`
- **单例工厂**: `HttpClientFactory` 提供全局单例HTTP客户端
- **Builder模式**: `HttpRequest.builder()` 构建请求对象

### 5.2 DefaultHttpClient

- 基于 `urllib3.PoolManager`，支持连接池复用
- 超时配置：连接超时默认5秒，读超时默认10秒
- SSL验证：默认 `cert_reqs='CERT_REQUIRED'`
- 错误处理：4xx -> `ClientException`，5xx -> `ServerException`，超时 -> 特定错误码

### 5.3 OAuth2TokenUtil

封装了所有OAuth2令牌操作，是HTTP层的核心工具类：

| 方法 | OAuth2流程 | grant_type |
|---|---|---|
| `get_token_with_client_secret_basic` | Client Secret Basic认证 | `client_credentials` |
| `get_token_with_client_secret_post` | Client Secret POST认证 | `client_credentials` |
| `get_token_with_client_assertion` | JWT Bearer断言 | `client_credentials` |
| `get_token_with_pca` | 私有CA认证 | `client_credentials` |
| `get_token_with_pkcs7_attested_document` | PKCS7证明文档 | `client_credentials` |
| `get_token_with_oidc_federated_credential` | OIDC联邦凭证 | `client_credentials` |
| `token_exchange` | 令牌交换 | `urn:ietf:params:oauth:grant-type:token-exchange` |
| `get_device_code` | 设备码流程 | - |
| `get_token_by_device_code` | 设备码换取令牌 | `urn:ietf:params:oauth:grant-type:device_code` |
| `refresh_token` | 刷新令牌 | `refresh_token` |

---

## 6. 配置管理

### 6.1 配置层次

```
IDaaSClientConfig
├── idaas_instance_id          # IDaaS实例ID
├── client_id                  # 客户端ID
├── scope                      # OAuth Scope (默认: urn:cloud:idaas:pam|cloud_account:obtain_access_credential)
├── issuer                     # 签发者端点
├── token_endpoint             # 令牌端点
├── device_authorization_endpoint  # 设备授权端点
├── developer_api_endpoint     # 开发者API端点
├── authn_configuration        # 认证配置 (IdentityAuthenticationConfiguration)
│   ├── identity_type          # 身份类型 (HUMAN/CLIENT)
│   ├── authn_method           # 认证方法 (8种TokenAuthnMethod)
│   ├── client_secret_env_var_name       # 客户端密钥环境变量名
│   ├── private_key_env_var_name         # 私钥环境变量名
│   ├── application_federated_credential_name  # 联邦凭证名称
│   ├── client_deploy_environment        # 部署环境 (11种枚举)
│   ├── oidc_token_file_path*            # OIDC Token文件路径
│   ├── client_x509_certificate          # X509证书
│   └── x509_cert_chains                 # X509证书链
└── http_configuration         # HTTP配置 (HttpConfiguration)
    ├── connect_timeout        # 连接超时 (默认5000ms, 范围2000-60000)
    ├── read_timeout           # 读超时 (默认10000ms, 范围2000-60000)
    └── unsafe_ignore_ssl_cert # 忽略SSL证书验证
```

### 6.2 配置加载机制

1. **配置文件路径解析**: 环境变量 `CLOUD_IDAAS_CONFIG_PATH` > 默认 `~/.cloud_idaas/client-config.json`
2. **JSON解析**: 通过 `JSONUtil.parse_object` + `from_dict` 反序列化
3. **键名兼容**: 支持 camelCase(JSON风格) 和 snake_case(Python风格) 双格式，通过 `StringUtil.camel_to_snake` 统一转换
4. **配置校验**: `ValidatorUtil` 根据认证方法校验必填字段

### 6.3 敏感信息安全设计

SDK遵循安全的敏感信息管理原则：
- **客户端密钥**(client_secret)和**私钥**(private_key)不直接存储在配置中，而是通过环境变量名间接引用
- 配置中仅存储环境变量名（如 `client_secret_env_var_name`），运行时通过 `os.environ.get()` 读取实际值

---

## 7. 异常体系

```
IDaaSException (基类)
├── ClientException                 # 客户端错误 (4xx)
│   ├── ConfigException            # 配置错误
│   └── ConcurrentOperationException  # 并发操作失败
├── ServerException                 # 服务端错误 (5xx)
├── CacheException                  # 缓存操作失败
├── CredentialException             # 凭证操作失败
├── EncodingException               # 编码操作失败
└── HttpException                   # HTTP通信异常
```

所有异常携带 `error_code` 和 `error_message`，`ClientException`/`ServerException` 额外携带 `request_id` 用于问题追踪。`ErrorCode` 类定义了37个标准错误码。

---

## 8. 设计模式总结

| 设计模式 | 应用位置 | 说明 |
|---|---|---|
| **工厂模式** | `IDaaSCredentialProviderFactory` | 根据配置创建不同认证方式的Provider |
| **Builder模式** | `IDaaSMachineCredentialProviderBuilder`, `HttpRequest.Builder`, `RefreshResultBuilder`, `AlibabaCloudEcsAttestedDocumentProviderBuilder` | 复杂对象的链式构建 |
| **策略模式** | `PrefetchStrategy` -> `OneCallerBlocks` / `NonBlocking` | 可插拔的缓存预取策略 |
| **模板方法** | `AbstractRefreshedCredentialProvider._refresh_credential` | 子类实现具体刷新逻辑 |
| **Provider模式** | 四个Provider抽象接口 | 解耦认证材料获取与令牌请求 |
| **单例模式** | `HttpClientFactory`, `UserAgentConfig` | 全局唯一的HTTP客户端和UA |
| **上下文管理器** | `AbstractRefreshedCredentialProvider` | 支持 `with` 语句自动释放资源 |

---

## 9. 核心调用流程

### M2M令牌获取流程（以CLIENT_SECRET_POST为例）

```
用户代码
  │
  ▼
IDaaSCredentialProviderFactory.init()
  │  ← ConfigReader 读取配置文件
  │  ← ValidatorUtil 校验配置
  │  ← _create_credential_provider() 创建 IDaaSMachineCredentialProvider
  │
  ▼
factory.get_idaas_credential_provider()
  │
  ▼
provider.get_credential()
  │
  ▼
AbstractRefreshedCredentialProvider.get_cached_result_supplier().get()
  │
  ▼
CachedResultSupplier.get()
  ├── 缓存有效？→ 直接返回缓存值
  ├── 需要预取？→ PrefetchStrategy.prefetch() 触发刷新
  └── 缓存过期？→ _refresh_cache() 阻塞刷新
        │
        ▼
IDaaSMachineCredentialProvider._refresh_credential()
  │
  ▼
IDaaSMachineCredentialProvider._get_token_from_idaas()
  │  根据 authn_method 选择:
  │  ├── CLIENT_SECRET_POST → OAuth2TokenUtil.get_token_with_client_secret_post()
  │  ├── CLIENT_SECRET_BASIC → OAuth2TokenUtil.get_token_with_client_secret_basic()
  │  ├── CLIENT_SECRET_JWT → client_assertion_provider.get_client_assertion() + OAuth2TokenUtil
  │  ├── PRIVATE_KEY_JWT → client_assertion_provider.get_client_assertion() + OAuth2TokenUtil
  │  ├── PKCS7 → attested_document_provider.get_attested_document() + OAuth2TokenUtil
  │  ├── OIDC → oidc_token_provider.get_oidc_token() + OAuth2TokenUtil
  │  └── PCA → client_assertion + X509证书 + OAuth2TokenUtil
  │
  ▼
DefaultHttpClient.send(request)
  │  urllib3 发送 POST 到 token_endpoint
  │
  ▼
IDaaSTokenResponse (access_token, id_token, refresh_token, expires_in, expires_at)
  │
  ▼
RefreshResult.builder(token).stale_time(...).prefetch_time(...).build()
  │  stale_time = expires_at - expires_in/5
  │  prefetch_time = expires_at - expires_in/3
  │
  ▼
CachedResultSupplier 缓存结果 (带Jitter抖动)
```

---

## 10. 部署环境支持

SDK通过 `ClientDeployEnvironmentEnum` 支持多种部署环境，主要影响PKCS7/OIDC认证的材料获取方式：

| 环境 | 认证材料来源 | 实现状态 |
|---|---|---|
| `COMMON` | 环境变量 | 已实现 |
| `COMPUTER` | 本地配置 | 已实现 |
| `KUBERNETES` | ServiceAccount Token (`/var/run/secrets/kubernetes.io/serviceaccount/token`) | 已实现(文件读取) |
| `ALIBABA_CLOUD_ECS` | ECS元数据服务 (`100.100.100.200`) | 已实现 |
| `ALIBABA_CLOUD_ACK` | ACK RRSA OIDC Token (环境变量 `ALIBABA_CLOUD_OIDC_TOKEN_FILE`) | 已实现(文件读取) |
| `AWS_EC2` | EC2 Instance Metadata | 占位实现(未完成) |
| `CUSTOM` | 用户自定义Provider | 已实现 |

---

## 11. 线程安全保障

- `CachedResultSupplier`: `threading.Lock` 保护缓存刷新操作
- `NonBlockingPrefetchStrategy`: `threading.Event` + `threading.Semaphore` 控制并发刷新
- `OneCallerBlocksPrefetchStrategy`: `threading.Event` 确保单调用者刷新
- `RequestUtil._seq_id`: `threading.Lock` 保护序列号生成
- `HttpClientFactory`: 类级别单例，Python GIL保证初始化安全