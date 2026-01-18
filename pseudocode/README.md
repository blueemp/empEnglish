# empEnglish 伪代码文档

## 概述

本文档包含了 empEnglish（考研复试英语口语 AI 智能体）项目的伪代码实现，基于 LLD 低层设计文档生成。伪代码用于指导开发团队进行实际编码实现。

## 目录结构

```
pseudocode/
├── models/              # 数据模型
│   ├── user.py          # 用户模型
│   ├── question.py      # 题目模型
│   ├── practice.py      # 练习模型
│   ├── scoring.py       # 评分模型
│   └── tutor_style.py   # 导师风格模型
├── services/            # 服务层
│   ├── user_service.py      # 用户服务
│   ├── question_service.py  # 题库服务
│   ├── practice_service.py  # 练习服务
│   └── scoring_service.py   # 评分服务
├── ai/                  # AI服务
│   ├── asr_service.py        # ASR语音识别服务
│   ├── tts_service.py        # TTS语音合成服务
│   ├── llm_service.py        # LLM大语言模型服务
│   └── agent_service.py      # Agent编排服务
└── utils/               # 工具类
    ├── jwt_manager.py        # JWT管理器
    ├── encryption_manager.py # 加密管理器
    ├── rate_limiter.py       # 限流器
    └── logger.py             # 日志器
```

## 模块说明

### 1. 数据模型 (models/)

#### user.py
- **User**: 用户数据库模型
- **UserRepository**: 用户数据访问层
- **UserService**: 用户业务逻辑层
- **UserPermissionChecker**: 用户权限检查器

主要功能：
- 微信登录
- 用户信息管理
- 订阅管理
- 权限检查

#### question.py
- **Question**: 题目数据库模型
- **QuestionRepository**: 题目数据访问层
- **QuestionService**: 题库业务逻辑层
- **QuestionCategoryManager**: 题类管理器

主要功能：
- 题目CRUD
- 题目推荐
- 题类管理

#### practice.py
- **PracticeSession**: 练习会话模型
- **PracticeTurn**: 练习轮次模型
- **PracticeRepository**: 练习数据访问层
- **PracticeService**: 练习业务逻辑层
- **WebSocketPracticeHandler**: WebSocket处理器

主要功能：
- 会话管理
- 答题流程
- WebSocket实时交互

#### scoring.py
- **ScoringRecord**: 评分记录模型
- **PhonemeError**: 发音错误模型
- **ScoringRepository**: 评分数据访问层
- **ScoringService**: 评分业务逻辑层

主要功能：
- 多维度评分
- 发音诊断
- 评分历史

#### tutor_style.py
- **TutorStyle**: 导师风格模型
- **TutorStyleRepository**: 导师风格数据访问层

主要功能：
- 导师风格管理
- 风格配置

### 2. 服务层 (services/)

#### user_service.py
用户服务，处理用户相关的业务逻辑：
- 微信登录
- 用户信息管理
- 订阅检查
- 权限验证

#### question_service.py
题库服务，处理题目相关的业务逻辑：
- 题目查询
- 题目推荐
- 题目管理

#### practice_service.py
练习服务，处理练习流程：
- 创建会话
- 提交答案
- 获取下一题
- 会话管理

#### scoring_service.py
评分服务，处理评分逻辑：
- 综合评分
- 各维度评分
- 评分建议生成
- 评分趋势分析

### 3. AI服务 (ai/)

#### asr_service.py
ASR语音识别服务：
- Whisper模型集成
- 语音转写
- 流式ASR
- 批量转写

#### tts_service.py
TTS语音合成服务：
- Edge-TTS集成
- VITS本地部署
- 多音色支持
- 风格定制

#### llm_service.py
LLM大语言模型服务：
- Qwen/DeepSeek集成
- 题目生成
- 反馈生成
- 追问生成
- 表达增强

#### agent_service.py
Agent编排服务：
- LangGraph工作流
- 面试流程编排
- 状态管理
- 节点定义

### 4. 工具类 (utils/)

#### jwt_manager.py
JWT管理器：
- Token生成
- Token验证
- Token刷新
- 用户ID提取

#### encryption_manager.py
加密管理器：
- 数据加密/解密
- 敏感数据脱敏
- 密码哈希
- 数据掩码

#### rate_limiter.py
限流器：
- 滑动窗口限流
- 令牌桶限流
- Redis支持
- 本地存储支持

#### logger.py
日志器：
- JSON格式日志
- 结构化日志
- 上下文管理
- 中间件支持

## 核心流程

### 1. 用户登录流程

```
用户 → 小程序 → 后端API → 微信API → 后端API → 返回Token
```

**关键代码位置：**
- `services/user_service.py` - `UserService.wechat_login()`
- `utils/jwt_manager.py` - `JWTManager.generate_access_token()`

### 2. 练习流程

```
创建会话 → 生成题目 → 用户录音 → ASR转写 → 评分 → 生成反馈 → 生成追问 → 循环
```

**关键代码位置：**
- `services/practice_service.py` - `PracticeService.create_session()`
- `services/practice_service.py` - `PracticeService.submit_answer()`
- `ai/agent_service.py` - `InterviewAgent.run()`

### 3. 评分流程

```
音频输入 → ASR转写 → 发音评分 → 流利度评分 → 词汇评分 → 语法评分 → 综合评分
```

**关键代码位置：**
- `services/scoring_service.py` - `ScoringService.evaluate()`
- `algorithms/gop_scorer.py` - GOP发音评分
- `algorithms/fluency_scorer.py` - 流利度评分

### 4. Agent工作流

```
生成题目 → 转写音频 → 评分 → 生成反馈 → 合成语音 → 生成追问 → 检查完成 → 生成报告
```

**关键代码位置：**
- `ai/agent_service.py` - `InterviewAgent._build_graph()`
- `ai/agent_service.py` - 各节点函数

## 技术栈

### 后端框架
- FastAPI: API框架
- SQLAlchemy: ORM
- Pydantic: 数据验证

### AI框架
- LangChain: LLM框架
- LangGraph: Agent编排
- Whisper/Faster-Whisper: ASR
- Edge-TTS/VITS: TTS
- Qwen/DeepSeek: LLM

### 数据库
- MySQL: 关系型数据
- MongoDB: 非结构化数据
- Redis: 缓存
- Milvus: 向量数据库

### 工具库
- JWT: 认证
- Cryptography: 加密
- Logging: 日志

## 使用说明

### 1. 环境准备

```bash
# 安装Python依赖
pip install fastapi uvicorn sqlalchemy pydantic
pip install langchain langgraph
pip install faster-whisper edge-tts
pip install cryptography

# 安装数据库
# MySQL, MongoDB, Redis, Milvus
```

### 2. 配置文件

创建 `config.yaml`:

```yaml
app:
  name: empenglish
  version: "1.0.0"

database:
  url: "mysql://user:password@localhost:3306/empenglish"

redis:
  url: "redis://localhost:6379/0"

jwt:
  secret_key: "your-secret-key"

llm:
  provider: "qwen"
  model: "qwen2.5-7b"
  api_key: "your-api-key"
```

### 3. 初始化服务

```python
from services.user_service import UserService
from services.practice_service import PracticeService
from ai.asr_service import ASRService
from ai.tts_service import TTSService
from ai.llm_service import LLMService
from ai.agent_service import InterviewAgent

# 初始化服务
jwt_manager = JWTManager(secret_key="your-secret-key")
encryption_manager = EncryptionManager(secret_key="your-secret-key")

asr_service = ASRService(model_size="base", device="cuda")
tts_service = TTSService()
llm_service = LLMService(model_name="qwen2.5-7b", api_key="your-api-key")

question_service = QuestionService()
scoring_service = ScoringService(...)
practice_service = PracticeService(
    question_service=question_service,
    scoring_service=scoring_service,
    asr_service=asr_service,
    tts_service=tts_service,
    llm_service=llm_service
)

# 创建Agent
agent = InterviewAgent(
    question_service=question_service,
    scoring_service=scoring_service,
    asr_service=asr_service,
    tts_service=tts_service,
    llm_service=llm_service
)
```

### 4. 运行服务

```bash
# 启动API服务
uvicorn app.main:app --host 0.0.0.0 --port 8001

# 启动ASR服务
uvicorn ai.asr_main:app --host 0.0.0.0 --port 9001

# 启动TTS服务
uvicorn ai.tts_main:app --host 0.0.0.0 --port 9002

# 启动LLM服务
uvicorn ai.llm_main:app --host 0.0.0.0 --port 9003
```

## 注意事项

1. **伪代码说明**：本代码为伪代码，部分实现为简化版本，实际开发时需要：
   - 完善数据库查询逻辑
   - 实现实际的API调用
   - 添加错误处理
   - 完善日志记录

2. **依赖安装**：实际部署时需要安装所有依赖包

3. **配置管理**：实际配置应使用环境变量或配置文件

4. **安全考虑**：
   - 使用HTTPS
   - 验证所有输入
   - 加密敏感数据
   - 实施限流

5. **性能优化**：
   - 使用连接池
   - 实现缓存
   - 异步处理
   - 数据库索引

## 下一步

1. **完善算法实现**：实现评分算法的详细逻辑
2. **添加单元测试**：为每个模块编写测试
3. **集成测试**：测试服务间的交互
4. **性能测试**：测试系统性能
5. **部署准备**：准备Docker和Kubernetes配置

## 参考资料

- [PRD.md](../PRD.md) - 产品需求文档
- [HLD.md](../HLD.md) - 高层设计文档
- [LLD.md](../LLD.md) - 低层设计文档

## 联系方式

如有问题，请联系开发团队。