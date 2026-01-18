# empEnglish 高阶设计文档（HLD）

> 版本：V1.0  
> 日期：2026年1月15日  
> 状态：初稿

---

## 文档修订历史

| 版本 | 日期 | 修订人 | 修订内容 |
|------|------|--------|----------|
| V1.0 | 2026-01-15 | iFlow | 初始版本 |

---

## 一、文档概述

### 1.1 文档目的

本文档为 empEnglish（考研复试英语口语 AI 智能体）项目的高阶设计文档（High-Level Design），旨在：

1. 明确系统整体架构和技术选型
2. 定义核心模块及其交互关系
3. 为后续详细设计和开发提供指导
4. 确保技术方案与产品需求（PRD）对齐

### 1.2 适用范围

本文档适用于：

- 架构师和技术负责人
- 后端开发工程师
- 前端开发工程师
- AI/算法工程师
- 测试工程师
- 产品经理（了解技术实现）

### 1.3 参考文档

- PRD.md（产品需求文档）
- 技术调研报告（竞品分析）

---

## 二、竞品分析总结

### 2.1 竞品功能对比

| 功能模块 | 可栗口语 | 咕噜口语 | 星空外语 | empEnglish（差异化） |
|---------|---------|---------|---------|---------------------|
| **语音识别（ASR）** | Whisper/Faster-Whisper | 自研深度学习引擎 | 自研深度学习引擎 | Whisper + 中文口音优化 |
| **语音合成（TTS）** | 标准TTS | 神经网络TTS | 多音色TTS | 多音色TTS + 导师风格定制 |
| **LLM模型** | OpenAI GPT系列 | DeepSeek-R1 | DeepSeek-R1 | Qwen/DeepSeek + 院校知识库 |
| **评分维度** | 4维度（发音、流利度、词汇、语法） | 4维度 + 音素级 | 4维度 + 音素级 | 4维度 + 院校匹配度 |
| **场景覆盖** | 通用场景 | 15000+场景 | 15000+场景 | 西安高校定制场景 |
| **压力模式** | 基础压力模式 | 3级压力模式 | 3级压力模式 | 3级压力模式 + 导师风格 |
| **实时性** | 中等（2-3秒） | 高（<100ms） | 高（<100ms） | 目标：<200ms |
| **定价** | ¥98-398 | ¥98-398 | ¥98-398 | ¥88-298 |

### 2.2 竞品技术架构分析

#### 2.2.1 咕噜口语（SpeakGuru）

**核心技术栈：**
- **ASR**: 自研深度学习语音识别引擎，准确率99.99%
- **LLM**: DeepSeek-R1，支持中英文混合
- **TTS**: 神经网络语音合成，多音色支持
- **Agent架构**: 多智能体工作流（Multi-Agent Workflow）
- **评分算法**: GOP（Goodness of Pronunciation）改进版 + DNN-HMM

**架构特点：**
- 流式语音识别，首帧延迟<100ms
- 端到端语音视频对话
- 多智能体协作（面试官、评分员、导师等角色）
- 自适应学习引擎，根据用户水平动态调整

**优势：**
- 响应速度快，用户体验流畅
- 音素级发音纠错准确率99.9%
- 场景覆盖广（15000+）
- 个性化程度高

**劣势：**
- 通用场景为主，缺乏院校/专业深度定制
- 导师风格模拟较泛化
- 本地化不足

#### 2.2.2 星空外语（SkyLingo）

**核心技术栈：**
- **ASR**: 自研深度学习引擎，支持44种口音
- **LLM**: DeepSeek-R1
- **TTS**: 多音色TTS，支持Labubu形象
- **Agent架构**: Agent多智能体AI外教
- **评分算法**: GOP + 强化学习自适应

**架构特点：**
- 全球首个接入DeepSeek-R1的口语应用
- 端到端语音视频对话
- 企业定制课程服务（1300+行业）
- 游戏化学习机制

**优势：**
- 技术领先，多项全球第一
- 企业级认可度高（华为、微软等）
- 场景覆盖最广
- 性价比高

**劣势：**
- 同样缺乏院校/专业深度定制
- 考研复试场景针对性不强

#### 2.2.3 可栗口语（Keli Speak）

**核心技术栈：**
- **ASR**: Whisper/Faster-Whisper
- **LLM**: OpenAI GPT系列
- **TTS**: 标准TTS
- **评分算法**: 基础GOP算法

**架构特点：**
- 轻量级部署
- 成本较低
- 功能相对简单

**优势：**
- 成本控制好
- 易于部署

**劣势：**
- 技术相对落后
- 功能不够丰富
- 个性化程度低

### 2.3 竞品技术差距与机会

**技术差距：**
1. **院校/专业深度定制**：竞品均为通用场景，缺乏针对特定院校、专业的深度定制
2. **导师风格数字孪生**：竞品有压力模式，但缺乏真实导师风格的数字孪生
3. **本地化发音训练**：竞品有音素级纠错，但缺乏针对西安地区考生的特定发音问题训练
4. **院校匹配度评分**：竞品无此功能

**技术机会：**
1. **差异化竞争**：通过院校/专业深度定制建立护城河
2. **本地化优势**：西安高校密集，本地化服务有天然优势
3. **成本优化**：使用开源模型（Qwen、Whisper）降低成本
4. **快速迭代**：基于LangChain/LangGraph快速构建Agent系统

---

## 三、系统架构设计

### 3.1 整体架构

empEnglish 采用**分层架构** + **微服务** + **事件驱动**的混合架构模式。

```
┌─────────────────────────────────────────────────────────────┐
│                         客户端层                              │
├─────────────────────────────────────────────────────────────┤
│  微信小程序  │  H5 Web  │  管理后台  │  B端机构后台           │
└─────────────────────────────────────────────────────────────┘
                              ↓ HTTPS/WSS
┌─────────────────────────────────────────────────────────────┐
│                         API网关层                            │
├─────────────────────────────────────────────────────────────┤
│  路由转发  │  认证授权  │  限流熔断  │  日志监控              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       业务服务层（微服务）                     │
├─────────────────────────────────────────────────────────────┤
│  用户服务  │  题库服务  │  练习服务  │  评分服务               │
│  报告服务  │  支付服务  │  通知服务  │  统计服务               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        AI服务层                              │
├─────────────────────────────────────────────────────────────┤
│  ASR服务   │  TTS服务   │  LLM服务   │  Agent编排服务          │
│  评分引擎  │  纠错引擎  │  报告生成   │  推荐引擎               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        数据层                                │
├─────────────────────────────────────────────────────────────┤
│  MySQL    │  Redis     │  MongoDB   │  MinIO/OSS             │
│  向量数据库 │  消息队列  │  时序数据库 │  Elasticsearch         │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 核心模块

#### 3.2.1 用户服务（User Service）

**职责：**
- 用户注册/登录（微信授权）
- 用户信息管理
- 目标院校/专业选择
- 订阅和权限管理

**技术栈：**
- 框架：FastAPI / Spring Boot
- 数据库：MySQL
- 缓存：Redis
- 认证：JWT + OAuth2.0

**核心接口：**
```python
# 用户注册/登录
POST /api/v1/auth/wechat/login
GET  /api/v1/user/profile
PUT  /api/v1/user/profile

# 目标院校/专业
GET  /api/v1/user/target-university
PUT  /api/v1/user/target-university

# 订阅管理
GET  /api/v1/user/subscription
POST /api/v1/user/subscription/purchase
```

#### 3.2.2 题库服务（Question Bank Service）

**职责：**
- 题库管理（通用题库 + 院校定制题库）
- 导师风格管理
- 题目推荐
- 题目版本控制

**技术栈：**
- 框架：FastAPI
- 数据库：MySQL（结构化数据） + MongoDB（非结构化数据）
- 搜索：Elasticsearch
- 向量数据库：Milvus / Pinecone（语义搜索）

**数据结构：**
```python
# 题目结构
class Question(BaseModel):
    id: str
    type: QuestionType  # 通用/院校定制/专业定制
    university: Optional[str]  # 所属院校
    college: Optional[str]  # 所属学院
    major: Optional[str]  # 所属专业
    category: str  # 自我介绍/家庭/专业背景等
    difficulty: int  # 1-5
    content: str  # 题目内容
    tags: List[str]  # 标签
    keywords: List[str]  # 关键词（用于追问）
    style_tags: List[str]  # 导师风格标签
    created_at: datetime
    updated_at: datetime

# 导师风格结构
class TutorStyle(BaseModel):
    id: str
    university: str
    college: Optional[str]
    major: Optional[str]
    style_type: StyleType  # 学术深挖型/实践导向型/友好交流型/刻板高压型
    personality: str  # 性格描述
    questioning_style: str  # 提问风格
    tone: str  # 语气
    follow_up_frequency: float  # 追问频率 0-1
    tolerance_level: float  # 容忍度 0-1
```

**核心接口：**
```python
# 题目查询
GET  /api/v1/questions
GET  /api/v1/questions/{id}
GET  /api/v1/questions/recommend  # 推荐题目

# 题目管理（管理员）
POST /api/v1/admin/questions
PUT  /api/v1/admin/questions/{id}
DELETE /api/v1/admin/questions/{id}

# 导师风格
GET  /api/v1/tutor-styles
POST /api/v1/admin/tutor-styles
```

#### 3.2.3 练习服务（Practice Service）

**职责：**
- 练习会话管理
- 练习流程控制
- 实时交互
- 练习记录存储

**技术栈：**
- 框架：FastAPI + WebSocket
- 数据库：MySQL（会话信息） + MongoDB（对话记录）
- 消息队列：RabbitMQ / Kafka
- 缓存：Redis

**核心接口：**
```python
# 练习会话
POST /api/v1/practice/sessions
GET  /api/v1/practice/sessions/{id}
PUT  /api/v1/practice/sessions/{id}

# WebSocket实时交互
WS   /api/v1/practice/sessions/{id}/ws

# 练习记录
GET  /api/v1/practice/records
GET  /api/v1/practice/records/{id}
```

**练习流程：**
```
1. 创建会话 → 选择模式（通用/院校定制）→ 选择压力等级
2. 开始练习 → AI提问 → 用户录音 → ASR转写 → LLM评分 → TTS反馈
3. 循环提问 → 根据回答生成追问
4. 结束练习 → 生成报告
```

#### 3.2.4 评分服务（Scoring Service）

**职责：**
- 多维度评分（发音、流利度、词汇、语法）
- 音素级发音诊断
- 语法纠错
- 院校匹配度评分

**技术栈：**
- 框架：FastAPI
- ASR：Whisper / Faster-Whisper
- LLM：Qwen / DeepSeek
- 评分算法：GOP + DNN-HMM
- 数据库：MySQL（评分结果） + 时序数据库（历史趋势）

**评分维度：**
```python
class ScoreDimension(BaseModel):
    pronunciation: float  # 发音 0-100
    fluency: float  # 流利度 0-100
    vocabulary: float  # 词汇多样性 0-100
    grammar: float  # 语法准确性 0-100
    university_match: float  # 院校匹配度 0-100（仅院校定制模式）

class DetailedScore(BaseModel):
    overall_score: float  # 综合得分
    dimensions: ScoreDimension
    phoneme_errors: List[PhonemeError]  # 音素级错误
    grammar_errors: List[GrammarError]  # 语法错误
    vocabulary_suggestions: List[str]  # 词汇建议
    university_match_details: Optional[UniversityMatchDetails]  # 院校匹配详情
```

**核心接口：**
```python
# 评分
POST /api/v1/scoring/evaluate
GET  /api/v1/scoring/results/{id}

# 发音诊断
POST /api/v1/scoring/phoneme-diagnosis

# 语法纠错
POST /api/v1/scoring/grammar-check
```

#### 3.2.5 报告服务（Report Service）

**职责：**
- 学习报告生成
- 报告导出（PDF）
- 学习趋势分析
- 薄弱环节分析

**技术栈：**
- 框架：FastAPI
- 数据库：MySQL + MongoDB
- 报告生成：ReportLab / WeasyPrint
- 数据分析：Pandas + Matplotlib

**报告类型：**
1. **单题报告**：单题评分 + 建议
2. **场次报告**：整场练习的综合评分 + 雷达图 + 建议
3. **每日小结**：当天场次平均分 + 维度雷达图 + 建议
4. **周度报告**：一周趋势图 + 高频错误列表 + 推荐训练计划

**核心接口：**
```python
# 报告生成
POST /api/v1/reports/generate
GET  /api/v1/reports/{id}
GET  /api/v1/reports/{id}/pdf

# 学习趋势
GET  /api/v1/reports/trends/daily
GET  /api/v1/reports/trends/weekly
```

#### 3.2.6 AI服务层（AI Service Layer）

**职责：**
- 提供统一的AI能力接口
- 管理AI模型调用
- 模型版本管理
- 成本控制

**技术栈：**
- 框架：FastAPI
- LLM框架：LangChain + LangGraph
- 模型：Qwen / DeepSeek / OpenAI
- 部署：Docker + Kubernetes

**Agent架构：**
```python
# 使用LangGraph构建Agent工作流
from langgraph.graph import StateGraph, END

# 定义状态
class InterviewState(TypedDict):
    user_id: str
    session_id: str
    university: Optional[str]
    major: Optional[str]
    pressure_level: int
    current_question: Optional[str]
    user_answer: Optional[str]
    asr_result: Optional[str]
    score: Optional[DetailedScore]
    follow_up_questions: List[str]
    conversation_history: List[dict]
    is_finished: bool

# Agent节点
def question_generator(state: InterviewState) -> InterviewState:
    """生成下一道题"""
    pass

def asr_processor(state: InterviewState) -> InterviewState:
    """语音识别"""
    pass

def scoring_agent(state: InterviewState) -> InterviewState:
    """评分Agent"""
    pass

def follow_up_generator(state: InterviewState) -> InterviewState:
    """追问生成器"""
    pass

def tts_generator(state: InterviewState) -> InterviewState:
    """语音合成"""
    pass

def report_generator(state: InterviewState) -> InterviewState:
    """报告生成"""
    pass

# 构建工作流
graph = StateGraph(InterviewState)
graph.add_node("question_generator", question_generator)
graph.add_node("asr_processor", asr_processor)
graph.add_node("scoring_agent", scoring_agent)
graph.add_node("follow_up_generator", follow_up_generator)
graph.add_node("tts_generator", tts_generator)
graph.add_node("report_generator", report_generator)

# 定义边
graph.set_entry_point("question_generator")
graph.add_edge("question_generator", "asr_processor")
graph.add_edge("asr_processor", "scoring_agent")
graph.add_edge("scoring_agent", "follow_up_generator")
graph.add_conditional_edges(
    "follow_up_generator",
    should_continue,
    {"continue": "tts_generator", "end": "report_generator"}
)
graph.add_edge("tts_generator", "question_generator")
graph.add_edge("report_generator", END)

# 编译
interview_agent = graph.compile()
```

**核心接口：**
```python
# ASR
POST /api/v1/ai/asr/transcribe

# TTS
POST /api/v1/ai/tts/synthesize

# LLM
POST /api/v1/ai/llm/chat
POST /api/v1/ai/llm/completion

# Agent
POST /api/v1/ai/agent/interview
```

### 3.3 数据库设计

#### 3.3.1 MySQL（关系型数据）

**用户表（users）**
```sql
CREATE TABLE users (
    id VARCHAR(64) PRIMARY KEY,
    openid VARCHAR(128) UNIQUE NOT NULL,
    nickname VARCHAR(100),
    avatar_url VARCHAR(500),
    target_university VARCHAR(100),
    target_college VARCHAR(100),
    target_major VARCHAR(100),
    subscription_type ENUM('free', 'trial', 'premium'),
    subscription_expiry DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_openid (openid),
    INDEX idx_subscription (subscription_type, subscription_expiry)
);
```

**题目表（questions）**
```sql
CREATE TABLE questions (
    id VARCHAR(64) PRIMARY KEY,
    type ENUM('general', 'university', 'major') NOT NULL,
    university VARCHAR(100),
    college VARCHAR(100),
    major VARCHAR(100),
    category VARCHAR(50) NOT NULL,
    difficulty INT DEFAULT 3,
    content TEXT NOT NULL,
    tags JSON,
    keywords JSON,
    style_tags JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_type (type),
    INDEX idx_university (university),
    INDEX idx_category (category),
    FULLTEXT idx_content (content)
);
```

**练习会话表（practice_sessions）**
```sql
CREATE TABLE practice_sessions (
    id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    mode ENUM('general', 'university') NOT NULL,
    pressure_level INT DEFAULT 2,
    university VARCHAR(100),
    major VARCHAR(100),
    status ENUM('ongoing', 'completed', 'aborted'),
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    overall_score DECIMAL(5,2),
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_start_time (start_time)
);
```

**评分记录表（scoring_records）**
```sql
CREATE TABLE scoring_records (
    id VARCHAR(64) PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,
    question_id VARCHAR(64) NOT NULL,
    user_answer TEXT,
    asr_result TEXT,
    pronunciation_score DECIMAL(5,2),
    fluency_score DECIMAL(5,2),
    vocabulary_score DECIMAL(5,2),
    grammar_score DECIMAL(5,2),
    university_match_score DECIMAL(5,2),
    overall_score DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES practice_sessions(id),
    FOREIGN KEY (question_id) REFERENCES questions(id),
    INDEX idx_session_id (session_id)
);
```

#### 3.3.2 MongoDB（非结构化数据）

**对话记录集合（conversations）**
```javascript
{
  _id: ObjectId,
  session_id: "uuid",
  user_id: "uuid",
  turns: [
    {
      turn_id: 1,
      question: "Please introduce yourself",
      user_answer_audio: "audio_url",
      user_answer_text: "My name is...",
      asr_result: "My name is...",
      score: {
        overall: 85.5,
        pronunciation: 88.0,
        fluency: 82.0,
        vocabulary: 85.0,
        grammar: 87.0,
        university_match: null
      },
      feedback: "Good introduction, but could be more specific...",
      follow_up_questions: ["What is your research interest?"]
    }
  ],
  created_at: ISODate,
  updated_at: ISODate
}
```

**导师风格集合（tutor_styles）**
```javascript
{
  _id: ObjectId,
  university: "西安交通大学",
  college: "电气工程学院",
  major: "电气工程",
  style_type: "academic_deep",
  personality: "严谨、学术导向",
  questioning_style: "深入挖掘理论背景",
  tone: "正式、专业",
  follow_up_frequency: 0.8,
  tolerance_level: 0.6,
  system_prompt: "You are a professor from Xi'an Jiaotong University...",
  examples: [
    {
      question: "Tell me about your research experience",
      follow_up: "What methodology did you use? Why?"
    }
  ],
  created_at: ISODate,
  updated_at: ISODate
}
```

#### 3.3.3 Redis（缓存）

**缓存策略：**
```python
# 用户信息缓存
key: user:{user_id}
ttl: 3600s

# 题目缓存
key: question:{question_id}
ttl: 86400s

# 用户会话缓存
key: session:{session_id}
ttl: 7200s

# 题目推荐缓存
key: recommend:{user_id}:{university}:{major}
ttl: 3600s

# 限流
key: ratelimit:{user_id}:{endpoint}
ttl: 60s
```

#### 3.3.4 向量数据库（Milvus / Pinecone）

**用途：**
- 题目语义搜索
- 用户回答相似度匹配
- 院校专业知识库检索

**数据结构：**
```python
# 题目向量
{
    "id": "question_id",
    "vector": [0.1, 0.2, ...],  # 768维向量
    "metadata": {
        "university": "西安交通大学",
        "major": "电气工程",
        "category": "专业背景"
    }
}

# 院校知识库向量
{
    "id": "knowledge_id",
    "vector": [0.1, 0.2, ...],
    "metadata": {
        "university": "西安交通大学",
        "type": "course",
        "content": "电力系统分析是电气工程的核心课程..."
    }
}
```

### 3.4 技术选型

#### 3.4.1 后端技术栈

| 组件 | 技术选型 | 说明 |
|------|---------|------|
| **API框架** | FastAPI | 高性能、异步、自动文档 |
| **ORM** | SQLAlchemy / Tortoise ORM | SQL数据库操作 |
| **数据库** | MySQL 8.0 | 关系型数据存储 |
| **NoSQL** | MongoDB 6.0 | 非结构化数据存储 |
| **缓存** | Redis 7.0 | 缓存、会话、限流 |
| **消息队列** | RabbitMQ / Kafka | 异步任务处理 |
| **向量数据库** | Milvus / Pinecone | 语义搜索 |
| **搜索引擎** | Elasticsearch 8.0 | 全文搜索 |
| **对象存储** | MinIO / 阿里云OSS | 音频/文件存储 |
| **容器化** | Docker + Kubernetes | 部署和编排 |
| **API网关** | Kong / APISIX | 路由、认证、限流 |
| **监控** | Prometheus + Grafana | 系统监控 |
| **日志** | ELK Stack | 日志收集和分析 |

#### 3.4.2 AI技术栈

| 组件 | 技术选型 | 说明 |
|------|---------|------|
| **ASR** | Whisper / Faster-Whisper | 开源、高准确率 |
| **ASR优化** | 中文口音微调 | 针对中国考生优化 |
| **LLM** | Qwen2.5 / DeepSeek | 开源、中文友好 |
| **LLM编排** | LangChain + LangGraph | Agent工作流 |
| **TTS** | VITS / Edge-TTS | 高质量语音合成 |
| **评分算法** | GOP + DNN-HMM | 音素级评分 |
| **向量模型** | text2vec / BGE | 文本向量化 |

#### 3.4.3 前端技术栈

| 组件 | 技术选型 | 说明 |
|------|---------|------|
| **小程序** | 原生小程序 / uni-app | 微信小程序 |
| **H5/Web** | Vue 3 + TypeScript | 响应式Web |
| **UI框架** | Element Plus / Vant | UI组件库 |
| **状态管理** | Pinia | 状态管理 |
| **HTTP客户端** | Axios | API调用 |
| **WebSocket** | Socket.io | 实时通信 |
| **音频处理** | Web Audio API | 音频录制/播放 |

#### 3.4.4 DevOps技术栈

| 组件 | 技术选型 | 说明 |
|------|---------|------|
| **版本控制** | Git + GitLab | 代码管理 |
| **CI/CD** | GitLab CI / Jenkins | 持续集成/部署 |
| **容器编排** | Kubernetes | 容器编排 |
| **配置管理** | Consul / Nacos | 配置中心 |
| **服务网格** | Istio | 服务治理 |
| **负载均衡** | Nginx / HAProxy | 负载均衡 |

### 3.5 部署架构

```
┌─────────────────────────────────────────────────────────────┐
│                         CDN                                  │
│              静态资源加速 / 音频文件加速                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       负载均衡层                              │
├─────────────────────────────────────────────────────────────┤
│              Nginx / HAProxy (L4/L7)                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       API网关层                              │
├─────────────────────────────────────────────────────────────┤
│              Kong / APISIX (多实例)                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes集群                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  用户服务    │  │  题库服务    │  │  练习服务    │         │
│  │  (3实例)    │  │  (2实例)    │  │  (3实例)    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  评分服务    │  │  报告服务    │  │  支付服务    │         │
│  │  (2实例)    │  │  (2实例)    │  │  (2实例)    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  ASR服务    │  │  TTS服务    │  │  LLM服务    │         │
│  │  (3实例)    │  │  (2实例)    │  │  (3实例)    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       数据层                                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  MySQL      │  │  MongoDB    │  │  Redis      │         │
│  │  (主从)     │  │  (副本集)   │  │  (集群)     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Milvus     │  │  RabbitMQ   │  │  MinIO      │         │
│  │  (集群)     │  │  (集群)     │  │  (分布式)   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

---

## 四、核心流程设计

### 4.1 用户注册/登录流程

```
1. 用户打开小程序
2. 点击"微信一键登录"
3. 小程序调用wx.login()获取code
4. 前端将code发送到后端
5. 后端调用微信API获取openid和session_key
6. 后端查询用户是否存在
   - 不存在：创建新用户，返回JWT token
   - 存在：更新登录信息，返回JWT token
7. 前端存储token，跳转到首页
```

**时序图：**
```
用户 → 小程序 → 后端API → 微信API → 后端API → 小程序 → 用户
```

### 4.2 练习流程（核心）

#### 4.2.1 创建练习会话

```
1. 用户选择练习模式（通用/院校定制）
2. 选择压力等级（温和/正常/高压）
3. 点击"开始练习"
4. 前端调用 POST /api/v1/practice/sessions
5. 后端创建会话记录
6. 后端调用Agent生成第一道题
7. 后端调用TTS生成语音
8. 返回会话ID和第一道题（文本+语音）
9. 前端建立WebSocket连接
```

#### 4.2.2 练习交互循环

```
1. AI提问（文本+语音）
2. 用户录音
3. 前端上传音频到ASR服务
4. ASR返回转写文本
5. 后端调用评分Agent进行多维度评分
6. 后端调用追问生成器生成追问
7. 后端调用TTS生成反馈语音
8. 通过WebSocket返回评分结果和追问
9. 前端展示评分和反馈
10. 循环回到步骤1，直到达到结束条件
```

**结束条件：**
- 完成预设题目数量（如10题）
- 用户主动结束
- 会话超时（如30分钟）

#### 4.2.3 生成报告

```
1. 会话结束
2. 后端调用报告生成Agent
3. 汇总所有题目的评分
4. 计算综合得分和各维度得分
5. 生成雷达图数据
6. 生成改进建议
7. 保存报告到数据库
8. 通知前端报告已生成
```

### 4.3 评分流程

```
1. 接收用户音频
2. ASR转写为文本
3. 发音评分（GOP算法）
   - 提取音频特征（MFCC）
   - 强制对齐（Forced Alignment）
   - 计算音素级得分
   - 汇总得到发音得分
4. 流利度评分
   - 计算语速（words per minute）
   - 检测停顿（silence detection）
   - 计算平均语流长度
   - 汇总得到流利度得分
5. 词汇评分（LLM分析）
   - 提取词汇
   - 计算词汇多样性（TTR）
   - 识别高级词汇
   - 汇总得到词汇得分
6. 语法评分（LLM分析）
   - 语法错误检测
   - 句式多样性分析
   - 汇总得到语法得分
7. 院校匹配度评分（仅院校定制模式）
   - 提取专业术语
   - 检查与目标专业的相关性
   - 评估表达结构是否符合该校风格
   - 汇总得到匹配度得分
8. 综合评分
   - 加权计算综合得分
   - 生成详细反馈
```

### 4.4 题目推荐流程

```
1. 用户选择目标院校/专业
2. 系统查询该院校/专业的定制题库
3. 如果题库不足，从通用题库补充
4. 根据用户历史表现调整难度
5. 使用向量搜索推荐相似题目
6. 返回推荐题目列表
```

---

## 五、关键技术实现

### 5.1 ASR服务实现

**技术选型：** Whisper / Faster-Whisper

**实现方案：**
```python
from faster_whisper import WhisperModel
import torch

class ASRService:
    def __init__(self, model_size="base", device="cuda"):
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type="float16"
        )
    
    def transcribe(self, audio_path, language="en"):
        """
        语音转写
        """
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            beam_size=5,
            vad_filter=True
        )
        
        result = ""
        for segment in segments:
            result += segment.text + " "
        
        return {
            "text": result.strip(),
            "language": info.language,
            "language_probability": info.language_probability
        }
    
    def transcribe_stream(self, audio_stream, language="en"):
        """
        流式转写（用于实时场景）
        """
        segments, info = self.model.transcribe(
            audio_stream,
            language=language,
            beam_size=5,
            vad_filter=True
        )
        
        for segment in segments:
            yield {
                "text": segment.text,
                "start": segment.start,
                "end": segment.end
            }
```

**优化策略：**
1. **模型量化**：使用int8量化减少内存占用
2. **批处理**：批量处理音频提高吞吐量
3. **缓存**：缓存常用音频的转写结果
4. **中文口音优化**：使用中国考生数据微调模型

### 5.2 TTS服务实现

**技术选型：** VITS / Edge-TTS

**实现方案：**
```python
import edge_tts
import asyncio

class TTSService:
    def __init__(self):
        self.voices = {
            "male_us": "en-US-GuyNeural",
            "female_us": "en-US-JennyNeural",
            "male_uk": "en-GB-RyanNeural",
            "female_uk": "en-GB-SoniaNeural"
        }
    
    async def synthesize(self, text, voice="female_us", output_path=None):
        """
        语音合成
        """
        communicate = edge_tts.Communicate(
            text,
            self.voices[voice]
        )
        
        if output_path:
            await communicate.save(output_path)
            return output_path
        else:
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            return audio_data
    
    def synthesize_sync(self, text, voice="female_us", output_path=None):
        """
        同步语音合成
        """
        return asyncio.run(self.synthesize(text, voice, output_path))
```

**导师风格定制：**
```python
class TutorStyleTTS(TTSService):
    def __init__(self):
        super().__init__()
        self.style_presets = {
            "academic_deep": {
                "voice": "male_us",
                "rate": "slow",
                "pitch": "low",
                "volume": "normal"
            },
            "friendly": {
                "voice": "female_us",
                "rate": "medium",
                "pitch": "medium",
                "volume": "normal"
            },
            "high_pressure": {
                "voice": "male_us",
                "rate": "fast",
                "pitch": "high",
                "volume": "loud"
            }
        }
    
    def synthesize_with_style(self, text, style_type="friendly"):
        """
        根据导师风格合成语音
        """
        style = self.style_presets.get(style_type, self.style_presets["friendly"])
        return self.synthesize(
            text,
            voice=style["voice"]
        )
```

### 5.3 LLM服务实现

**技术选型：** Qwen2.5 / DeepSeek

**实现方案：**
```python
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

class LLMService:
    def __init__(self, model_name="qwen2.5-7b", api_key=None):
        self.llm = ChatOpenAI(
            model=model_name,
            api_key=api_key,
            temperature=0.7,
            max_tokens=1000
        )
    
    def chat(self, messages):
        """
        对话
        """
        response = self.llm(messages)
        return response.content
    
    def generate_question(self, context):
        """
        生成题目
        """
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are an English interview examiner for graduate school admission."),
            HumanMessage(content=f"""
            Based on the following context, generate an interview question:
            
            Context:
            - University: {context['university']}
            - Major: {context['major']}
            - Category: {context['category']}
            - Previous questions: {context['previous_questions']}
            
            Generate a relevant and challenging question.
            """)
        ])
        
        messages = prompt.format_messages(**context)
        return self.chat(messages)
    
    def score_answer(self, question, answer):
        """
        评分
        """
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are an English speaking examiner."),
            HumanMessage(content=f"""
            Question: {question}
            Answer: {answer}
            
            Please score the answer on the following dimensions (0-100):
            1. Pronunciation
            2. Fluency
            3. Vocabulary
            4. Grammar
            
            Also provide specific feedback and suggestions.
            
            Return the result in JSON format:
            {
                "pronunciation": 85,
                "fluency": 80,
                "vocabulary": 82,
                "grammar": 88,
                "overall": 84,
                "feedback": "...",
                "suggestions": ["...", "..."]
            }
            """)
        ])
        
        messages = prompt.format_messages(question=question, answer=answer)
        response = self.chat(messages)
        return json.loads(response)
    
    def generate_follow_up(self, question, answer, keywords):
        """
        生成追问
        """
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are an English interview examiner."),
            HumanMessage(content=f"""
            Question: {question}
            Answer: {answer}
            Keywords: {keywords}
            
            Generate 1-2 follow-up questions based on the answer.
            The questions should be relevant and challenging.
            """)
        ])
        
        messages = prompt.format_messages(
            question=question,
            answer=answer,
            keywords=keywords
        )
        return self.chat(messages)
```

### 5.4 Agent编排实现

**使用LangGraph构建Agent工作流：**

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional
import json

class InterviewState(TypedDict):
    user_id: str
    session_id: str
    university: Optional[str]
    major: Optional[str]
    pressure_level: int
    current_question: Optional[str]
    user_answer: Optional[str]
    asr_result: Optional[str]
    score: Optional[dict]
    feedback: Optional[str]
    follow_up_questions: List[str]
    conversation_history: List[dict]
    question_count: int
    max_questions: int
    is_finished: bool

class InterviewAgent:
    def __init__(self, llm_service, asr_service, tts_service):
        self.llm = llm_service
        self.asr = asr_service
        self.tts = tts_service
        self.graph = self._build_graph()
    
    def _build_graph(self):
        graph = StateGraph(InterviewState)
        
        # 添加节点
        graph.add_node("generate_question", self._generate_question)
        graph.add_node("transcribe_audio", self._transcribe_audio)
        graph.add_node("score_answer", self._score_answer)
        graph.add_node("generate_follow_up", self._generate_follow_up)
        graph.add_node("synthesize_feedback", self._synthesize_feedback)
        graph.add_node("check_completion", self._check_completion)
        graph.add_node("generate_report", self._generate_report)
        
        # 添加边
        graph.set_entry_point("generate_question")
        graph.add_edge("generate_question", "transcribe_audio")
        graph.add_edge("transcribe_audio", "score_answer")
        graph.add_edge("score_answer", "generate_follow_up")
        graph.add_edge("generate_follow_up", "synthesize_feedback")
        graph.add_edge("synthesize_feedback", "check_completion")
        
        graph.add_conditional_edges(
            "check_completion",
            self._should_continue,
            {
                "continue": "generate_question",
                "end": "generate_report"
            }
        )
        graph.add_edge("generate_report", END)
        
        return graph.compile()
    
    def _generate_question(self, state: InterviewState) -> InterviewState:
        """生成题目"""
        context = {
            "university": state.get("university"),
            "major": state.get("major"),
            "category": "introduction" if state["question_count"] == 0 else "general",
            "previous_questions": [turn["question"] for turn in state["conversation_history"]]
        }
        
        question = self.llm.generate_question(context)
        
        state["current_question"] = question
        state["conversation_history"].append({
            "turn_id": len(state["conversation_history"]) + 1,
            "question": question,
            "answer": None,
            "score": None
        })
        
        return state
    
    def _transcribe_audio(self, state: InterviewState) -> InterviewState:
        """语音识别"""
        # 这里应该是从state中获取音频文件路径
        # audio_path = state["audio_path"]
        # result = self.asr.transcribe(audio_path)
        # state["asr_result"] = result["text"]
        
        # 模拟
        state["asr_result"] = state["user_answer"]
        
        return state
    
    def _score_answer(self, state: InterviewState) -> InterviewState:
        """评分"""
        score_result = self.llm.score_answer(
            state["current_question"],
            state["asr_result"]
        )
        
        state["score"] = score_result
        state["conversation_history"][-1]["answer"] = state["asr_result"]
        state["conversation_history"][-1]["score"] = score_result
        
        return state
    
    def _generate_follow_up(self, state: InterviewState) -> InterviewState:
        """生成追问"""
        # 从题目中提取关键词
        keywords = self._extract_keywords(state["current_question"])
        
        follow_up = self.llm.generate_follow_up(
            state["current_question"],
            state["asr_result"],
            keywords
        )
        
        state["follow_up_questions"] = [follow_up]
        
        return state
    
    def _synthesize_feedback(self, state: InterviewState) -> InterviewState:
        """合成反馈语音"""
        feedback = state["score"]["feedback"]
        audio_path = self.tts.synthesize_with_style(feedback, "friendly")
        
        state["feedback"] = feedback
        state["feedback_audio"] = audio_path
        
        return state
    
    def _check_completion(self, state: InterviewState) -> InterviewState:
        """检查是否完成"""
        state["question_count"] += 1
        
        if state["question_count"] >= state["max_questions"]:
            state["is_finished"] = True
        else:
            state["is_finished"] = False
        
        return state
    
    def _should_continue(self, state: InterviewState) -> str:
        """决定是否继续"""
        if state["is_finished"]:
            return "end"
        else:
            return "continue"
    
    def _generate_report(self, state: InterviewState) -> InterviewState:
        """生成报告"""
        # 汇总所有评分
        scores = [turn["score"] for turn in state["conversation_history"]]
        
        overall_score = sum(s["overall"] for s in scores) / len(scores)
        pronunciation_score = sum(s["pronunciation"] for s in scores) / len(scores)
        fluency_score = sum(s["fluency"] for s in scores) / len(scores)
        vocabulary_score = sum(s["vocabulary"] for s in scores) / len(scores)
        grammar_score = sum(s["grammar"] for s in scores) / len(scores)
        
        report = {
            "overall_score": overall_score,
            "dimensions": {
                "pronunciation": pronunciation_score,
                "fluency": fluency_score,
                "vocabulary": vocabulary_score,
                "grammar": grammar_score
            },
            "conversation_history": state["conversation_history"],
            "suggestions": [s["suggestions"] for s in scores]
        }
        
        state["report"] = report
        
        return state
    
    def _extract_keywords(self, question: str) -> List[str]:
        """提取关键词"""
        # 简单实现，实际可以使用NLP
        words = question.split()
        keywords = [word for word in words if len(word) > 4]
        return keywords[:5]
    
    def run(self, initial_state: InterviewState):
        """运行Agent"""
        return self.graph.invoke(initial_state)
```

### 5.5 评分算法实现

**GOP（Goodness of Pronunciation）算法：**

```python
import numpy as np
from scipy.signal import spectrogram
import torch
import torchaudio

class GOPScorer:
    def __init__(self, model_path):
        # 加载预训练的声学模型
        self.acoustic_model = torch.load(model_path)
        self.sample_rate = 16000
    
    def extract_features(self, audio_path):
        """
        提取音频特征（MFCC）
        """
        waveform, sample_rate = torchaudio.load(audio_path)
        if sample_rate != self.sample_rate:
            resampler = torchaudio.transforms.Resample(sample_rate, self.sample_rate)
            waveform = resampler(waveform)
        
        mfcc = torchaudio.transforms.MFCC(
            sample_rate=self.sample_rate,
            n_mfcc=13
        )(waveform)
        
        return mfcc.numpy()
    
    def forced_alignment(self, features, text):
        """
        强制对齐
        """
        # 使用声学模型进行强制对齐
        # 返回每个音素的时间边界
        alignments = []
        # ... 实现细节
        return alignments
    
    def calculate_gop_score(self, audio_path, text):
        """
        计算GOP分数
        """
        features = self.extract_features(audio_path)
        alignments = self.forced_alignment(features, text)
        
        phoneme_scores = []
        for alignment in alignments:
            # 计算每个音素的后验概率
            posterior_prob = self._calculate_posterior_prob(
                features,
                alignment
            )
            
            # 计算GOP分数
            gop_score = np.log(posterior_prob)
            phoneme_scores.append(gop_score)
        
        # 汇总得到整体发音得分
        overall_score = np.mean(phoneme_scores)
        
        # 归一化到0-100
        normalized_score = self._normalize_score(overall_score)
        
        return {
            "overall_score": normalized_score,
            "phoneme_scores": phoneme_scores,
            "alignments": alignments
        }
    
    def _calculate_posterior_prob(self, features, alignment):
        """
        计算后验概率
        """
        # 使用声学模型计算后验概率
        # ... 实现细节
        return 0.85
    
    def _normalize_score(self, score):
        """
        归一化分数到0-100
        """
        # 使用sigmoid函数归一化
        normalized = 1 / (1 + np.exp(-score))
        return normalized * 100
```

**流利度评分：**

```python
class FluencyScorer:
    def __init__(self):
        self.sample_rate = 16000
    
    def calculate_fluency_score(self, audio_path, text):
        """
        计算流利度分数
        """
        waveform, sample_rate = torchaudio.load(audio_path)
        
        # 计算语速（words per minute）
        duration = len(waveform) / sample_rate
        word_count = len(text.split())
        speech_rate = word_count / (duration / 60)
        
        # 检测停顿
        pauses = self._detect_pauses(waveform, sample_rate)
        
        # 计算平均语流长度
        avg_speech_length = self._calculate_avg_speech_length(pauses, duration)
        
        # 计算停顿频率
        pause_frequency = len(pauses) / duration
        
        # 综合评分
        score = self._calculate_composite_score(
            speech_rate,
            avg_speech_length,
            pause_frequency
        )
        
        return {
            "overall_score": score,
            "speech_rate": speech_rate,
            "avg_speech_length": avg_speech_length,
            "pause_frequency": pause_frequency,
            "pauses": pauses
        }
    
    def _detect_pauses(self, waveform, sample_rate, threshold=0.01):
        """
        检测停顿
        """
        energy = torch.mean(torch.abs(waveform), dim=0)
        pauses = []
        
        in_pause = False
        pause_start = 0
        
        for i, e in enumerate(energy):
            if e < threshold and not in_pause:
                in_pause = True
                pause_start = i / sample_rate
            elif e >= threshold and in_pause:
                in_pause = False
                pause_end = i / sample_rate
                pauses.append({
                    "start": pause_start,
                    "end": pause_end,
                    "duration": pause_end - pause_start
                })
        
        return pauses
    
    def _calculate_avg_speech_length(self, pauses, duration):
        """
        计算平均语流长度
        """
        if not pauses:
            return duration
        
        speech_segments = []
        prev_end = 0
        
        for pause in pauses:
            speech_segments.append(pause["start"] - prev_end)
            prev_end = pause["end"]
        
        speech_segments.append(duration - prev_end)
        
        return np.mean(speech_segments)
    
    def _calculate_composite_score(self, speech_rate, avg_speech_length, pause_frequency):
        """
        综合评分
        """
        # 语速评分（理想值：120-150 wpm）
        if 120 <= speech_rate <= 150:
            rate_score = 100
        elif speech_rate < 120:
            rate_score = (speech_rate / 120) * 100
        else:
            rate_score = max(0, 100 - (speech_rate - 150) * 2)
        
        # 语流长度评分（理想值：> 3秒）
        length_score = min(100, avg_speech_length * 30)
        
        # 停顿频率评分（理想值：< 2次/分钟）
        if pause_frequency < 2:
            pause_score = 100
        else:
            pause_score = max(0, 100 - (pause_frequency - 2) * 20)
        
        # 加权平均
        composite_score = (
            rate_score * 0.4 +
            length_score * 0.3 +
            pause_score * 0.3
        )
        
        return composite_score
```

---

## 六、性能优化策略

### 6.1 ASR优化

1. **模型量化**：使用int8量化减少内存占用和推理时间
2. **批处理**：批量处理音频提高吞吐量
3. **缓存**：缓存常用音频的转写结果
4. **GPU加速**：使用CUDA加速推理
5. **流式处理**：支持流式转写，降低延迟

### 6.2 LLM优化

1. **模型选择**：根据任务复杂度选择不同规模的模型
   - 简单任务：Qwen2.5-7B
   - 复杂任务：Qwen2.5-72B
2. **Prompt优化**：优化提示词减少推理时间
3. **缓存**：缓存常见问题的回答
4. **批处理**：批量处理请求提高吞吐量
5. **KV Cache**：使用KV Cache加速生成

### 6.3 数据库优化

1. **索引优化**：为常用查询字段添加索引
2. **读写分离**：MySQL主从分离，读写分离
3. **分库分表**：按用户ID分库分表
4. **缓存**：使用Redis缓存热点数据
5. **连接池**：使用连接池管理数据库连接

### 6.4 缓存策略

1. **多级缓存**：
   - L1：本地缓存（内存）
   - L2：Redis缓存
   - L3：数据库
2. **缓存预热**：系统启动时预加载热点数据
3. **缓存更新**：使用写穿透或写回策略
4. **缓存过期**：设置合理的TTL

### 6.5 并发优化

1. **异步处理**：使用异步I/O提高并发能力
2. **消息队列**：使用消息队列削峰填谷
3. **限流**：使用令牌桶算法限流
4. **熔断**：使用熔断器防止雪崩

---

## 七、安全设计

### 7.1 认证与授权

1. **JWT Token**：使用JWT进行身份认证
2. **OAuth2.0**：支持OAuth2.0授权
3. **RBAC**：基于角色的访问控制
4. **API密钥**：为第三方应用提供API密钥

### 7.2 数据安全

1. **数据加密**：
   - 传输加密：HTTPS
   - 存储加密：敏感数据加密存储
2. **数据脱敏**：日志中敏感数据脱敏
3. **数据备份**：定期备份数据
4. **数据审计**：记录数据访问日志

### 7.3 接口安全

1. **HTTPS**：所有接口使用HTTPS
2. **签名验证**：API请求签名验证
3. **防重放攻击**：使用nonce和timestamp
4. **限流**：接口限流防止滥用

### 7.4 音频安全

1. **音频验证**：验证音频格式和大小
2. **病毒扫描**：上传音频病毒扫描
3. **内容审核**：音频内容审核
4. **隐私保护**：用户音频隐私保护

---

## 八、监控与运维

### 8.1 监控指标

1. **系统指标**：
   - CPU使用率
   - 内存使用率
   - 磁盘使用率
   - 网络流量
2. **应用指标**：
   - 请求量
   - 响应时间
   - 错误率
   - 并发数
3. **业务指标**：
   - 用户数
   - 练习次数
   - 付费转化率
   - 用户留存率

### 8.2 日志管理

1. **日志级别**：DEBUG、INFO、WARNING、ERROR
2. **日志格式**：JSON格式，结构化日志
3. **日志收集**：使用ELK Stack收集日志
4. **日志分析**：使用Kibana分析日志

### 8.3 告警机制

1. **告警级别**：INFO、WARNING、ERROR、CRITICAL
2. **告警方式**：邮件、短信、钉钉、企业微信
3. **告警规则**：
   - 错误率 > 5%
   - 响应时间 > 2s
   - CPU使用率 > 80%
   - 内存使用率 > 80%

### 8.4 部署策略

1. **蓝绿部署**：零停机部署
2. **金丝雀发布**：灰度发布
3. **回滚策略**：快速回滚
4. **健康检查**：服务健康检查

---

## 九、成本估算

### 9.1 开发成本

| 角色 | 人数 | 月薪（万） | 月数 | 小计（万） |
|------|------|-----------|------|-----------|
| 架构师 | 1 | 3.5 | 2 | 7 |
| 后端工程师 | 3 | 2.5 | 4 | 30 |
| 前端工程师 | 2 | 2.0 | 4 | 16 |
| AI工程师 | 2 | 3.0 | 4 | 24 |
| 测试工程师 | 1 | 1.5 | 3 | 4.5 |
| 产品经理 | 1 | 2.0 | 4 | 8 |
| **合计** | **10** | | | **89.5** |

### 9.2 运营成本（月）

| 项目 | 成本（元） |
|------|-----------|
| 云服务器（K8S集群） | 20,000 |
| 数据库（MySQL主从） | 5,000 |
| 对象存储（MinIO/OSS） | 3,000 |
| CDN | 2,000 |
| LLM API调用 | 10,000 |
| 其他（域名、SSL等） | 1,000 |
| **合计** | **41,000** |

### 9.3 优化建议

1. **使用开源模型**：使用Qwen等开源模型替代商业API
2. **模型量化**：量化模型减少资源消耗
3. **缓存优化**：优化缓存减少API调用
4. **批量处理**：批量处理提高效率

---

## 十、风险评估

### 10.1 技术风险

| 风险 | 影响 | 概率 | 应对措施 |
|------|------|------|----------|
| ASR准确率不足 | 高 | 中 | 使用Whisper + 中文口音微调 |
| LLM响应慢 | 中 | 中 | 使用流式输出 + 缓存 |
| 并发能力不足 | 高 | 低 | 使用消息队列 + 限流 |
| 数据库性能瓶颈 | 高 | 中 | 读写分离 + 分库分表 |

### 10.2 业务风险

| 风险 | 影响 | 概率 | 应对措施 |
|------|------|------|----------|
| 用户增长不及预期 | 高 | 中 | 增加营销投入 |
| 竞品抄袭 | 中 | 高 | 快速迭代 + 建立护城河 |
| 付费转化率低 | 高 | 中 | 优化产品体验 |
| 题库内容不足 | 中 | 中 | 持续更新题库 |

### 10.3 合规风险

| 风险 | 影响 | 概率 | 应对措施 |
|------|------|------|----------|
| 数据隐私问题 | 高 | 低 | 数据加密 + 隐私政策 |
| 音频版权问题 | 中 | 低 | 用户授权 + 审核机制 |
| 内容合规问题 | 高 | 低 | 内容审核 + 过滤机制 |

---

## 十一、后续规划

### 11.1 MVP阶段（1-2个月）

**目标：** 跑通通用模拟 + 评分闭环

**功能：**
- 用户注册/登录
- 通用题库（10-20个话题）
- 基础评分（4维度）
- 练习记录（3天）
- 单题报告

**技术：**
- 基础架构搭建
- ASR服务（Whisper）
- TTS服务（Edge-TTS）
- LLM服务（Qwen2.5-7B）
- 基础评分算法

### 11.2 迭代一（3-4个月）

**目标：** 上线西安高校定制 + 冲刺包付费

**功能：**
- 西安高校定制题库（3所重点院校）
- 高压模式（3级）
- 突发追问引擎
- 学习报告（每日小结 + 周度报告）
- 支付功能（微信支付）
- 导师风格数字孪生

**技术：**
- Agent编排（LangGraph）
- 高级评分算法（音素级）
- 报告生成引擎
- 支付集成

### 11.3 迭代二（5-6个月）

**目标：** 拓展院校与专业 + B端试点

**功能：**
- 西安主流院校覆盖（10+所）
- 专业定制题库（20+个专业）
- B端机构后台
- 院校匹配度评分
- 西安特化发音训练模块

**技术：**
- 向量数据库（Milvus）
- 语义搜索
- 院校知识库
- B端管理系统

### 11.4 后续规划（6个月+）

**目标：** 复制到其他城市/场景

**功能：**
- 全国更多院校通用版
- 四六级口语场景
- 职场英语场景
- 多语言支持

**技术：**
- 多语言ASR/TTS
- 多语言LLM
- 多语言题库

---

## 十二、总结

本文档详细阐述了 empEnglish 的高阶设计，包括：

1. **竞品分析**：深入分析了咕噜口语、星空外语等竞品的功能和技术架构
2. **系统架构**：设计了分层架构 + 微服务 + 事件驱动的混合架构
3. **核心模块**：定义了用户服务、题库服务、练习服务、评分服务、报告服务等核心模块
4. **技术选型**：选择了FastAPI、LangChain/LangGraph、Whisper、Qwen等技术栈
5. **核心流程**：设计了用户注册/登录、练习流程、评分流程、题目推荐流程
6. **技术实现**：提供了ASR、TTS、LLM、Agent编排、评分算法的详细实现方案
7. **性能优化**：提出了ASR、LLM、数据库、缓存、并发等优化策略
8. **安全设计**：设计了认证授权、数据安全、接口安全、音频安全方案
9. **监控运维**：定义了监控指标、日志管理、告警机制、部署策略
10. **成本估算**：估算了开发成本和运营成本
11. **风险评估**：识别了技术风险、业务风险、合规风险
12. **后续规划**：规划了MVP、迭代一、迭代二及后续的发展路线

**核心差异化优势：**

1. **院校/专业深度定制**：校–院–专业三级题库 + 导师风格包
2. **本地化优势**：西安高校密集，本地化服务有天然优势
3. **成本优化**：使用开源模型（Qwen、Whisper）降低成本
4. **快速迭代**：基于LangChain/LangGraph快速构建Agent系统

**下一步行动：**

1. 详细设计：基于HLD进行详细设计（LLD）
2. 技术验证：验证关键技术（ASR、LLM、Agent编排）
3. 原型开发：开发MVP原型
4. 用户测试：邀请目标用户测试
5. 迭代优化：根据反馈迭代优化

---

**文档结束**