# empEnglish - AI-powered English Oral Practice Platform

## 项目概述

面向中国考研生的英语口语练习AI平台，目标为西安地区的院校。

## 技术栈

- **后端框架**: FastAPI
- **数据库**: MySQL (SQLAlchemy ORM)
- **缓存**: Redis
- **对象存储**: MinIO (音频文件)
- **AI服务**:
  - ASR: faster-whisper (语音识别)
  - TTS: edge-tts (文本转语音)
  - LLM: Qwen/DeepSeek (大语言模型)
  - Agent: LangGraph (面试编排)
- **评分算法**: GOP (发音)、流利度、词汇、语法、院校匹配
- **认证**: JWT (JSON Web Token)
- **容器化**: Docker + docker-compose

## 项目结构

```
empEnglish/
├── main.py              # 应用入口点
├── Dockerfile            # Docker镜像配置
├── docker-compose.yml     # 完整服务编排
├── .env.example          # 环境变量示例
├── requirements.txt       # Python依赖
├── pytest.ini           # 测试配置
├── src/                 # 生产代码目录
│   ├── models/           # 数据库模型
│   ├── services/         # 业务逻辑层
│   ├── ai/              # AI服务层
│   ├── algorithms/       # 评分算法
│   ├── utils/           # 工具类（JWT、加密、限流）
│   └── api/             # API路由
├── tests/               # 测试目录
│   ├── unit/           # 单元测试
│   ├── integration/     # 集成测试
│   └── performance/     # 性能测试（Locust）
└── pseudocode/          # 原始设计文档代码（参考实现）
```

## 快速开始

### 前置要求

- Python 3.12+
- Docker & Docker Compose
- MySQL 8.0+
- Redis 7.0+

### 使用Docker Compose启动（推荐）

```bash
# 1. 克隆项目
git clone <repository-url>
cd empEnglish

# 2. 复制环境变量（可选，docker-compose.yml已包含基本配置）
cp .env.example .env

# 3. 编辑.env文件，配置以下参数（如果需要）：
#    - 数据库密码
#    - JWT密钥（生产环境使用强密钥）
#    - WeChat App ID和Secret
#    - LLM API密钥
#    - MinIO凭据

# 4. 启动所有服务
docker-compose up -d

# 5. 查看日志
docker-compose logs -f app

# 6. 检查服务状态
docker-compose ps

# 7. 访问API文档
open http://localhost:8000/docs
```

### 服务端口映射

| 服务 | 容器端口 | 主机端口 | 说明 |
|------|-----------|-----------|------|
| MySQL | 3306 | 3307 | 数据库 |
| Redis | 6379 | 6379 | 缓存 |
| MinIO | 9000-9001 | 9000-9001 | 对象存储 |
| App | 8000 | 8000 | 应用服务 |

### 本地开发运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动依赖服务（MySQL, Redis, MinIO）
docker-compose up mysql redis minio -d

# 3. 运行应用
python main.py

# 4. 访问API文档
open http://localhost:8000/docs
```

## API端点

### 健康检查

```
GET /health         - 健康检查
GET /               - 根路径信息
```

### 认证

```
POST /api/v1/auth/wechat/login    - 微信登录
POST /api/v1/auth/refresh          - 刷新访问令牌
```

### 用户管理

```
GET    /api/v1/users/profile      - 获取用户信息
PUT    /api/v1/users/profile      - 更新用户信息
GET    /api/v1/users/subscription  - 检查订阅状态
```

### 题库管理

```
GET    /api/v1/questions                - 题目列表（分页）
GET    /api/v1/questions/{id}          - 获取题目详情
GET    /api/v1/questions/recommendations - 推荐题目
```

### 练习会话

```
POST   /api/v1/practice/sessions                       - 创建练习会话
GET    /api/v1/practice/sessions/{id}/next        - 获取下一题
POST   /api/v1/practice/sessions/{id}/turns/{turn}/submit - 提交答案
GET    /api/v1/practice/sessions/{id}/turns/{turn}/feedback - 获取评分反馈
GET    /api/v1/practice/sessions/{id}/report     - 获取完整报告
```

## 评分维度

系统使用5个维度进行综合评分：

| 维度 | 权重 | 说明 |
|------|--------|------|
| 发音 (Pronunciation) | 25% | GOP音素评分 |
| 流利度 (Fluency) | 25% | 语速、停顿频率 |
| 词汇 (Vocabulary) | 25% | 词汇多样性、高级词汇 |
| 语法 (Grammar) | 25% | 语法错误检测 |
| 院校匹配 (University Match) | 20% | 仅在院校定制模式下启用 |

## 练习模式

### 通用模式（所有用户免费）

- 标准面试问题
- 5维度基础评分
- 无院校/专业定制

### 院校定制模式（高级订阅）

- 西安地区院校专属题库
- 院校匹配度评分（20%权重）
- 目标专业相关问题

### 高压模式（高级订阅）

- 3个难度级别（初级、中级、高级）
- 倒计时功能
- 模拟真实面试压力

## 运行测试

```bash
# 单元测试
pytest tests/unit/ -v

# 集成测试
pytest tests/integration/ -v

# 所有测试（含覆盖率）
pytest --cov=src --cov-report=html

# 性能测试（Locust）
locust -f tests/performance/locustfile.py --headless
```

## 配置说明

### 环境变量

| 变量 | 说明 | 默认值 |
|--------|------|----------|
| DATABASE_URL | MySQL连接字符串 | mysql+pymysql://user:password@localhost/empenglish |
| JWT_SECRET_KEY | JWT签名密钥 | your-secret-key |
| REDIS_URL | Redis连接字符串 | redis://localhost:6379/0 |
| WHISPER_MODEL | Whisper模型路径 | base |
| TTS_ENGINE | TTS引擎 | edge-tts |
| LLM_PROVIDER | LLM提供商 | qwen |
| MINIO_ENDPOINT | MinIO端点 | http://localhost:9000 |

### 限流配置

| 端点类型 | 限制 |
|----------|------|
| 通用API | 100次/分钟 |
| 登录 | 10次/小时 |
| 提交答案 | 20次/分钟 |
| 获取报告 | 60次/小时 |

## 生产部署建议

1. **安全配置**
   - 更改所有默认密码和密钥
   - 使用强JWT密钥（至少32字节）
   - 配置HTTPS和CORS
   - 启用API限流

2. **数据库优化**
   - 配置连接池大小
   - 启用查询缓存
   - 定期备份

3. **对象存储**
   - 使用云存储服务（阿里云OSS、AWS S3等）替代MinIO
   - 配置CDN加速
   - 设置合理的生命周期策略

4. **AI服务优化**
   - Whisper: 使用GPU加速
   - TTS: 预生成常用音频片段
   - LLM: 使用流式输出减少延迟

5. **监控**
   - 配置Prometheus + Grafana监控
   - 设置告警规则
   - 日志集中管理

## 已知限制

1. **AI服务依赖**
    - Whisper需要GPU才能达到理想性能
    - edge-tts仅支持英语语音
    - LLM调用有API速率限制

2. **评分准确性**
    - GOP评分需要高质量音频输入
    - 语法检测依赖规则引擎，可能遗漏复杂错误

3. **并发处理**
    - WebSocket连接数受限于服务器配置
    - 长音频文件处理占用大量资源

4. **依赖版本兼容性**
    - `pymilvus==2.3.4` 的 `grpcio` 依赖在某些环境中构建失败
    - `openai` 库版本需要固定以避免依赖冲突
    - `pydantic-settings==2.1.0` 的 `Config` 类与 `model_config` 不能同时使用

## 部署状态

✅ **当前状态**: 所有服务正常运行

### 运行中的服务

- ✅ MySQL 8.0 - 数据库服务
- ✅ Redis 7-alpine - 缓存服务
- ✅ MinIO - 对象存储服务
- ✅ empEnglish App - 应用服务 (FastAPI)

### 已验证的端点

- ✅ `GET /health` - 健康检查端点
  ```json
  {"status":"healthy","version":"1.0.0","service":"empEnglish"}
  ```

- ✅ `GET /` - 根路径信息
  ```json
  {"service":"empEnglish","description":"AI-powered English oral practice platform","version":"1.0.0","docs":"/docs"}
  ```

- ✅ `GET /docs` - Swagger API 文档 (http://localhost:8000/docs)
- ✅ `GET /redoc` - ReDoc API 文档 (http://localhost:8000/redoc)

### 可访问的外部服务

- MinIO 控制台: http://localhost:9001
  - 用户名: `minioadmin`
  - 密码: `minioadmin`
  - 桶: `empenglish-audio`

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交代码（遵循PEP 8规范）
4. 推送到分支
5. 创建Pull Request

## 许可证

[待定]

## 联系方式

- 项目负责人: [待填写]
- 问题反馈: [GitHub Issues链接]
- 邮箱: [待填写]

---

## 版本历史

### v1.0.1 (2026-01-18)
- 修复 Dockerfile 中的 `useradd` 命令参数错误
- 移除 `docker-compose.yml` 中过时的 `version` 字段
- 固定依赖版本以避免构建冲突：
  - `langchain==0.1.20`
  - `langgraph==0.0.26`
  - `openai==1.12.0`
  - `faster-whisper==1.0.3`
  - `edge-tts==6.1.9`
  - `locust==2.17.0`
  - `cryptography==41.0.7`
- 添加 `email-validator==2.1.0` 依赖
- 修复 `src/utils/config.py` 中的 Pydantic 配置兼容性问题
- 暂时注释掉 `pymilvus==2.3.4` (grpcio 构建问题)
- 成功部署所有服务并验证端点可用性

### v1.0.0 (2026-01-18)
- 初始版本
- 完整的TDD实现
- 5个评分算法
- 完整的API路由
- Docker化部署配置
