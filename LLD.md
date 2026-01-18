# empEnglish 低层设计文档（LLD）

> 版本：V1.0
> 日期：2026年1月17日
> 状态：初稿

---

## 文档修订历史

| 版本 | 日期 | 修订人 | 修订内容 |
|------|------|--------|----------|
| V1.0 | 2026-01-17 | iFlow | 初始版本 |

---

## 一、文档概述

### 1.1 文档目的

本文档为 empEnglish（考研复试英语口语 AI 智能体）项目的低层设计文档（Low-Level Design），旨在：

1. 详细定义各模块的接口规范
2. 设计核心数据结构和算法
3. 定义数据库表结构和索引
4. 定义API接口规范
5. 定义消息格式和协议
6. 为开发提供详细的实现指导

### 1.2 适用范围

本文档适用于：

- 后端开发工程师
- 前端开发工程师
- AI/算法工程师
- 测试工程师
- 运维工程师

### 1.3 参考文档

- PRD.md（产品需求文档）
- HLD.md（高阶设计文档）

### 1.4 术语定义

| 术语 | 定义 |
|------|------|
| ASR | Automatic Speech Recognition，自动语音识别 |
| TTS | Text-to-Speech，文本转语音 |
| LLM | Large Language Model，大语言模型 |
| GOP | Goodness of Pronunciation，发音质量评分 |
| Agent | 智能体，具有自主决策能力的AI组件 |
| MVP | Minimum Viable Product，最小可行产品 |

---

## 二、系统架构概览

### 2.1 整体架构图

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
│  Kong (路由/认证/限流/熔断/日志)                              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       业务服务层（微服务）                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  用户服务    │  │  题库服务    │  │  练习服务    │         │
│  │  :8001      │  │  :8002      │  │  :8003      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  评分服务    │  │  报告服务    │  │  支付服务    │         │
│  │  :8004      │  │  :8005      │  │  :8006      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  通知服务    │  │  统计服务    │  │  订阅服务    │         │
│  │  :8007      │  │  :8008      │  │  :8009      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        AI服务层                              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  ASR服务    │  │  TTS服务    │  │  LLM服务    │         │
│  │  :9001      │  │  :9002      │  │  :9003      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Agent编排  │  │  评分引擎   │  │  纠错引擎   │         │
│  │  :9004      │  │  :9005      │  │  :9006      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        数据层                                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  MySQL      │  │  MongoDB    │  │  Redis      │         │
│  │  :3306      │  │  :27017     │  │  :6379      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Milvus     │  │  RabbitMQ   │  │  MinIO      │         │
│  │  :19530     │  │  :5672      │  │  :9000      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 技术栈详情

#### 2.2.1 后端技术栈

| 组件 | 版本 | 说明 |
|------|------|------|
| Python | 3.12+ | 主要开发语言 |
| FastAPI | 0.104+ | API框架 |
| SQLAlchemy | 2.0+ | ORM |
| Alembic | 1.13+ | 数据库迁移 |
| Pydantic | 2.5+ | 数据验证 |
| uvicorn | 0.24+ | ASGI服务器 |
| Redis | 7.0+ | 缓存 |
| RabbitMQ | 3.12+ | 消息队列 |
| Celery | 5.3+ | 异步任务 |

#### 2.2.2 AI技术栈

| 组件 | 版本 | 说明 |
|------|------|------|
| Whisper | 20231117 | ASR模型 |
| Faster-Whisper | 1.0.0+ | 优化版ASR |
| Qwen2.5 | 7B/72B | LLM模型 |
| LangChain | 0.1.0+ | LLM框架 |
| LangGraph | 0.0.20+ | Agent编排 |
| VITS | 0.1.0+ | TTS模型 |
| Edge-TTS | 6.1.0+ | 在线TTS |
| Milvus | 2.3+ | 向量数据库 |
| text2vec | 1.2+ | 文本向量化 |

#### 2.2.3 前端技术栈

| 组件 | 版本 | 说明 |
|------|------|------|
| uni-app | 3.0+ | 跨平台框架 |
| Vue 3 | 3.3+ | 前端框架 |
| TypeScript | 5.0+ | 类型系统 |
| Vant | 4.0+ | UI组件库 |
| Pinia | 2.1+ | 状态管理 |
| Axios | 1.6+ | HTTP客户端 |

#### 2.2.4 DevOps技术栈

| 组件 | 版本 | 说明 |
|------|------|------|
| Docker | 24.0+ | 容器化 |
| Kubernetes | 1.28+ | 容器编排 |
| Nginx | 1.24+ | 负载均衡 |
| Kong | 3.4+ | API网关 |
| Prometheus | 2.47+ | 监控 |
| Grafana | 10.0+ | 可视化 |
| ELK Stack | 8.10+ | 日志 |

---

## 三、数据库设计

### 3.1 MySQL数据库设计

#### 3.1.1 用户表（users）

```sql
CREATE TABLE users (
    id VARCHAR(64) PRIMARY KEY COMMENT '用户ID，UUID',
    openid VARCHAR(128) UNIQUE NOT NULL COMMENT '微信OpenID',
    unionid VARCHAR(128) UNIQUE COMMENT '微信UnionID',
    nickname VARCHAR(100) COMMENT '昵称',
    avatar_url VARCHAR(500) COMMENT '头像URL',
    phone VARCHAR(20) COMMENT '手机号',
    email VARCHAR(100) COMMENT '邮箱',
    target_university VARCHAR(100) COMMENT '目标院校',
    target_college VARCHAR(100) COMMENT '目标学院',
    target_major VARCHAR(100) COMMENT '目标专业',
    subscription_type ENUM('free', 'trial', 'premium_15d', 'premium_30d', 'annual') DEFAULT 'free' COMMENT '订阅类型',
    subscription_expiry DATETIME COMMENT '订阅到期时间',
    total_practice_count INT DEFAULT 0 COMMENT '总练习次数',
    last_practice_time DATETIME COMMENT '最后练习时间',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted_at TIMESTAMP NULL COMMENT '删除时间',
    INDEX idx_openid (openid),
    INDEX idx_unionid (unionid),
    INDEX idx_subscription (subscription_type, subscription_expiry),
    INDEX idx_target (target_university, target_major),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';
```

#### 3.1.2 题目表（questions）

```sql
CREATE TABLE questions (
    id VARCHAR(64) PRIMARY KEY COMMENT '题目ID，UUID',
    type ENUM('general', 'university', 'major') NOT NULL COMMENT '题目类型',
    university VARCHAR(100) COMMENT '所属院校',
    college VARCHAR(100) COMMENT '所属学院',
    major VARCHAR(100) COMMENT '所属专业',
    category VARCHAR(50) NOT NULL COMMENT '题类：自我介绍/家庭/专业背景/研究兴趣/职业规划等',
    difficulty INT DEFAULT 3 COMMENT '难度等级：1-5',
    content TEXT NOT NULL COMMENT '题目内容',
    reference_answer TEXT COMMENT '参考答案',
    tags JSON COMMENT '标签列表',
    keywords JSON COMMENT '关键词列表，用于追问',
    style_tags JSON COMMENT '导师风格标签',
    usage_count INT DEFAULT 0 COMMENT '使用次数',
    avg_score DECIMAL(5,2) COMMENT '平均得分',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    is_premium BOOLEAN DEFAULT FALSE COMMENT '是否为付费题目',
    created_by VARCHAR(64) COMMENT '创建人ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted_at TIMESTAMP NULL COMMENT '删除时间',
    INDEX idx_type (type),
    INDEX idx_university (university),
    INDEX idx_major (major),
    INDEX idx_category (category),
    INDEX idx_difficulty (difficulty),
    INDEX idx_is_active (is_active),
    FULLTEXT idx_content (content)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='题目表';
```

#### 3.1.3 导师风格表（tutor_styles）

```sql
CREATE TABLE tutor_styles (
    id VARCHAR(64) PRIMARY KEY COMMENT '风格ID，UUID',
    university VARCHAR(100) NOT NULL COMMENT '所属院校',
    college VARCHAR(100) COMMENT '所属学院',
    major VARCHAR(100) COMMENT '所属专业',
    style_type ENUM('academic_deep', 'practice_oriented', 'friendly', 'high_pressure') NOT NULL COMMENT '风格类型',
    name VARCHAR(100) NOT NULL COMMENT '风格名称',
    description TEXT COMMENT '风格描述',
    personality VARCHAR(200) COMMENT '性格描述',
    questioning_style VARCHAR(200) COMMENT '提问风格',
    tone VARCHAR(50) COMMENT '语气：formal/casual/friendly/stern',
    follow_up_frequency DECIMAL(3,2) DEFAULT 0.5 COMMENT '追问频率：0-1',
    tolerance_level DECIMAL(3,2) DEFAULT 0.7 COMMENT '容忍度：0-1',
    system_prompt TEXT COMMENT '系统提示词',
    examples JSON COMMENT '示例对话',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_university (university),
    INDEX idx_style_type (style_type),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='导师风格表';
```

#### 3.1.4 练习会话表（practice_sessions）

```sql
CREATE TABLE practice_sessions (
    id VARCHAR(64) PRIMARY KEY COMMENT '会话ID，UUID',
    user_id VARCHAR(64) NOT NULL COMMENT '用户ID',
    mode ENUM('general', 'university') NOT NULL COMMENT '练习模式',
    pressure_level INT DEFAULT 2 COMMENT '压力等级：1-温和/2-正常/3-高压',
    university VARCHAR(100) COMMENT '目标院校',
    major VARCHAR(100) COMMENT '目标专业',
    tutor_style_id VARCHAR(64) COMMENT '导师风格ID',
    status ENUM('ongoing', 'completed', 'aborted') DEFAULT 'ongoing' COMMENT '状态',
    question_count INT DEFAULT 0 COMMENT '已答题目数',
    max_questions INT DEFAULT 10 COMMENT '最大题目数',
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '开始时间',
    end_time TIMESTAMP NULL COMMENT '结束时间',
    duration INT COMMENT '持续时间（秒）',
    overall_score DECIMAL(5,2) COMMENT '综合得分',
    report_id VARCHAR(64) COMMENT '报告ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (tutor_style_id) REFERENCES tutor_styles(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_start_time (start_time),
    INDEX idx_mode_university (mode, university)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='练习会话表';
```

#### 3.1.5 练习轮次表（practice_turns）

```sql
CREATE TABLE practice_turns (
    id VARCHAR(64) PRIMARY KEY COMMENT '轮次ID，UUID',
    session_id VARCHAR(64) NOT NULL COMMENT '会话ID',
    turn_number INT NOT NULL COMMENT '轮次序号',
    question_id VARCHAR(64) NOT NULL COMMENT '题目ID',
    question TEXT NOT NULL COMMENT '题目内容',
    user_answer_audio_url VARCHAR(500) COMMENT '用户回答音频URL',
    user_answer_text TEXT COMMENT '用户回答文本',
    asr_result TEXT COMMENT 'ASR转写结果',
    pronunciation_score DECIMAL(5,2) COMMENT '发音得分',
    fluency_score DECIMAL(5,2) COMMENT '流利度得分',
    vocabulary_score DECIMAL(5,2) COMMENT '词汇得分',
    grammar_score DECIMAL(5,2) COMMENT '语法得分',
    university_match_score DECIMAL(5,2) COMMENT '院校匹配度得分',
    overall_score DECIMAL(5,2) COMMENT '综合得分',
    feedback TEXT COMMENT '反馈内容',
    feedback_audio_url VARCHAR(500) COMMENT '反馈音频URL',
    follow_up_questions JSON COMMENT '追问列表',
    is_recommended BOOLEAN DEFAULT FALSE COMMENT '是否推荐重练',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (session_id) REFERENCES practice_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id),
    INDEX idx_session_id (session_id),
    INDEX idx_question_id (question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='练习轮次表';
```

#### 3.1.6 评分记录表（scoring_records）

```sql
CREATE TABLE scoring_records (
    id VARCHAR(64) PRIMARY KEY COMMENT '评分记录ID，UUID',
    turn_id VARCHAR(64) NOT NULL COMMENT '轮次ID',
    user_id VARCHAR(64) NOT NULL COMMENT '用户ID',
    dimension ENUM('pronunciation', 'fluency', 'vocabulary', 'grammar', 'university_match') NOT NULL COMMENT '评分维度',
    score DECIMAL(5,2) NOT NULL COMMENT '得分',
    details JSON COMMENT '评分详情',
    suggestions JSON COMMENT '建议列表',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (turn_id) REFERENCES practice_turns(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_turn_id (turn_id),
    INDEX idx_user_id (user_id),
    INDEX idx_dimension (dimension),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='评分记录表';
```

#### 3.1.7 发音错误表（phoneme_errors）

```sql
CREATE TABLE phoneme_errors (
    id VARCHAR(64) PRIMARY KEY COMMENT '错误ID，UUID',
    turn_id VARCHAR(64) NOT NULL COMMENT '轮次ID',
    word VARCHAR(50) NOT NULL COMMENT '单词',
    correct_phoneme VARCHAR(20) COMMENT '正确音素',
    actual_phoneme VARCHAR(20) COMMENT '实际音素',
    position INT COMMENT '位置',
    score DECIMAL(5,2) COMMENT '得分',
    suggestion VARCHAR(200) COMMENT '建议',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (turn_id) REFERENCES practice_turns(id) ON DELETE CASCADE,
    INDEX idx_turn_id (turn_id),
    INDEX idx_word (word)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='发音错误表';
```

#### 3.1.8 报告表（reports）

```sql
CREATE TABLE reports (
    id VARCHAR(64) PRIMARY KEY COMMENT '报告ID，UUID',
    user_id VARCHAR(64) NOT NULL COMMENT '用户ID',
    session_id VARCHAR(64) NOT NULL COMMENT '会话ID',
    type ENUM('turn', 'session', 'daily', 'weekly') NOT NULL COMMENT '报告类型',
    title VARCHAR(200) COMMENT '报告标题',
    overall_score DECIMAL(5,2) COMMENT '综合得分',
    dimension_scores JSON COMMENT '维度得分',
    radar_data JSON COMMENT '雷达图数据',
    trend_data JSON COMMENT '趋势图数据',
    error_summary JSON COMMENT '错误汇总',
    suggestions JSON COMMENT '建议列表',
    training_plan JSON COMMENT '训练计划',
    pdf_url VARCHAR(500) COMMENT 'PDF报告URL',
    is_exported BOOLEAN DEFAULT FALSE COMMENT '是否已导出',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES practice_sessions(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_session_id (session_id),
    INDEX idx_type (type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='报告表';
```

#### 3.1.9 订单表（orders）

```sql
CREATE TABLE orders (
    id VARCHAR(64) PRIMARY KEY COMMENT '订单ID，UUID',
    user_id VARCHAR(64) NOT NULL COMMENT '用户ID',
    order_no VARCHAR(64) UNIQUE NOT NULL COMMENT '订单号',
    product_type ENUM('trial', 'premium_15d', 'premium_30d', 'annual') NOT NULL COMMENT '产品类型',
    product_name VARCHAR(100) NOT NULL COMMENT '产品名称',
    amount DECIMAL(10,2) NOT NULL COMMENT '金额',
    discount_amount DECIMAL(10,2) DEFAULT 0 COMMENT '优惠金额',
    actual_amount DECIMAL(10,2) NOT NULL COMMENT '实付金额',
    status ENUM('pending', 'paid', 'cancelled', 'refunded') DEFAULT 'pending' COMMENT '订单状态',
    payment_method ENUM('wechat', 'alipay') COMMENT '支付方式',
    transaction_id VARCHAR(128) COMMENT '交易流水号',
    paid_at TIMESTAMP NULL COMMENT '支付时间',
    expired_at TIMESTAMP NULL COMMENT '过期时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_order_no (order_no),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单表';
```

#### 3.1.10 机构表（institutions）

```sql
CREATE TABLE institutions (
    id VARCHAR(64) PRIMARY KEY COMMENT '机构ID，UUID',
    name VARCHAR(200) NOT NULL COMMENT '机构名称',
    code VARCHAR(50) UNIQUE COMMENT '机构代码',
    logo_url VARCHAR(500) COMMENT 'Logo URL',
    contact_person VARCHAR(100) COMMENT '联系人',
    contact_phone VARCHAR(20) COMMENT '联系电话',
    contact_email VARCHAR(100) COMMENT '联系邮箱',
    address VARCHAR(500) COMMENT '地址',
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active' COMMENT '状态',
    max_students INT COMMENT '最大学生数',
    current_students INT DEFAULT 0 COMMENT '当前学生数',
    subscription_expiry DATETIME COMMENT '订阅到期时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_status (status),
    INDEX idx_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='机构表';
```

#### 3.1.11 机构学生表（institution_students）

```sql
CREATE TABLE institution_students (
    id VARCHAR(64) PRIMARY KEY COMMENT 'ID，UUID',
    institution_id VARCHAR(64) NOT NULL COMMENT '机构ID',
    user_id VARCHAR(64) NOT NULL COMMENT '用户ID',
    student_name VARCHAR(100) COMMENT '学生姓名',
    student_phone VARCHAR(20) COMMENT '学生手机',
    status ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
    expiry_at TIMESTAMP NULL COMMENT '到期时间',
    FOREIGN KEY (institution_id) REFERENCES institutions(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_institution_id (institution_id),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='机构学生表';
```

### 3.2 MongoDB数据库设计

#### 3.2.1 对话记录集合（conversations）

```javascript
{
  _id: ObjectId,
  session_id: "uuid",
  user_id: "uuid",
  mode: "general|university",
  university: "西安交通大学",
  major: "电气工程",
  pressure_level: 2,
  tutor_style_id: "uuid",
  turns: [
    {
      turn_id: "uuid",
      turn_number: 1,
      question: {
        id: "uuid",
        content: "Please introduce yourself",
        type: "general",
        category: "introduction"
      },
      user_input: {
        audio_url: "minio://audio/user/session1/turn1.mp3",
        text: "My name is Zhang Wei...",
        asr_result: "My name is Zhang Wei..."
      },
      scoring: {
        overall: 85.5,
        pronunciation: {
          score: 88.0,
          details: [
            {
              word: "pronunciation",
              score: 85,
              errors: []
            }
          ]
        },
        fluency: {
          score: 82.0,
          speech_rate: 135,
          pause_frequency: 1.2
        },
        vocabulary: {
          score: 85.0,
          diversity: 0.75,
          advanced_words: ["consequently", "furthermore"]
        },
        grammar: {
          score: 87.0,
          errors: [],
          sentence_variety: 0.8
        },
        university_match: {
          score: null,
          relevance: null,
          suggestions: []
        }
      },
      feedback: {
        text: "Good introduction, but could be more specific about your research interests...",
        audio_url: "minio://audio/feedback/session1/turn1.mp3"
      },
      follow_up_questions: [
        "What is your research interest?",
        "Why did you choose this field?"
      ],
      timestamp: ISODate("2026-01-17T10:30:00Z"),
      duration: 15
    }
  ],
  statistics: {
    total_turns: 10,
    total_duration: 150,
    avg_score: 82.3,
    dimension_avg: {
      pronunciation: 85.0,
      fluency: 80.0,
      vocabulary: 82.0,
      grammar: 83.0
    }
  },
  created_at: ISODate("2026-01-17T10:30:00Z"),
  updated_at: ISODate("2026-01-17T10:45:00Z")
}
```

#### 3.2.2 院校知识库集合（university_knowledge）

```javascript
{
  _id: ObjectId,
  university: "西安交通大学",
  college: "电气工程学院",
  major: "电气工程",
  type: "course|research|faculty|admission",
  title: "电力系统分析",
  content: "电力系统分析是电气工程的核心课程，主要研究电力系统的稳态和暂态分析...",
  keywords: ["power system", "stability", "load flow"],
  related_questions: [
    "What is power system stability?",
    "How do you analyze load flow?"
  ],
  vector: [0.1, 0.2, ...],  // 768维向量
  created_at: ISODate("2026-01-17T10:00:00Z"),
  updated_at: ISODate("2026-01-17T10:00:00Z")
}
```

### 3.3 Redis缓存设计

#### 3.3.1 缓存键命名规范

```
# 用户信息
user:{user_id}
user:openid:{openid}

# 题目
question:{question_id}
questions:recommend:{user_id}:{university}:{major}

# 会话
session:{session_id}
session:active:{user_id}

# 评分
score:turn:{turn_id}

# 限流
ratelimit:{user_id}:{endpoint}
ratelimit:ip:{ip}:{endpoint}

# 订阅
subscription:{user_id}

# 统计
stats:daily:{date}
stats:weekly:{week}
```

#### 3.3.2 缓存策略

| 键类型 | TTL | 策略 |
|--------|-----|------|
| user:{user_id} | 3600s | 写穿透 |
| question:{question_id} | 86400s | 写回 |
| session:{session_id} | 7200s | 写穿透 |
| ratelimit:{user_id}:{endpoint} | 60s | 固定过期 |
| subscription:{user_id} | 300s | 写穿透 |

### 3.4 Milvus向量数据库设计

#### 3.4.1 Collection定义

**题目向量集合（question_vectors）**

```python
collection_name = "question_vectors"

schema = {
    "fields": [
        {"name": "id", "type": "VARCHAR", "max_length": 64, "is_primary": True},
        {"name": "vector", "type": "FLOAT_VECTOR", "dim": 768},
        {"name": "university", "type": "VARCHAR", "max_length": 100},
        {"name": "major", "type": "VARCHAR", "max_length": 100},
        {"name": "category", "type": "VARCHAR", "max_length": 50},
        {"name": "difficulty", "type": "INT64"}
    ],
    "index": {
        "field": "vector",
        "type": "IVF_FLAT",
        "params": {"nlist": 128}
    }
}
```

**院校知识库向量集合（knowledge_vectors）**

```python
collection_name = "knowledge_vectors"

schema = {
    "fields": [
        {"name": "id", "type": "VARCHAR", "max_length": 64, "is_primary": True},
        {"name": "vector", "type": "FLOAT_VECTOR", "dim": 768},
        {"name": "university", "type": "VARCHAR", "max_length": 100},
        {"name": "type", "type": "VARCHAR", "max_length": 20},
        {"name": "title", "type": "VARCHAR", "max_length": 200}
    ],
    "index": {
        "field": "vector",
        "type": "IVF_FLAT",
        "params": {"nlist": 128}
    }
}
```

---

## 四、API接口设计

### 4.1 接口规范

#### 4.1.1 通用规范

| 规范项 | 说明 |
|--------|------|
| 协议 | HTTPS |
| 基础路径 | /api/v1 |
| 请求格式 | JSON |
| 响应格式 | JSON |
| 字符编码 | UTF-8 |
| 时间格式 | ISO 8601 (YYYY-MM-DDTHH:mm:ssZ) |
| 分页 | page/page_size 或 offset/limit |

#### 4.1.2 统一响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "timestamp": "2026-01-17T10:30:00Z",
  "request_id": "uuid"
}
```

**错误响应格式：**

```json
{
  "code": 40001,
  "message": "参数错误",
  "errors": [
    {
      "field": "email",
      "message": "邮箱格式不正确"
    }
  ],
  "timestamp": "2026-01-17T10:30:00Z",
  "request_id": "uuid"
}
```

#### 4.1.3 状态码定义

| code | message | 说明 |
|------|---------|------|
| 0 | success | 成功 |
| 40001 | 参数错误 | 请求参数不正确 |
| 40002 | 参数缺失 | 必填参数缺失 |
| 40101 | 未登录 | 用户未登录 |
| 40102 | Token过期 | Token已过期 |
| 40103 | Token无效 | Token无效 |
| 40301 | 无权限 | 无权限访问 |
| 40401 | 资源不存在 | 请求的资源不存在 |
| 40901 | 资源冲突 | 资源冲突 |
| 42901 | 请求过多 | 请求频率过高 |
| 50001 | 服务器错误 | 服务器内部错误 |
| 50002 | 服务不可用 | 服务暂时不可用 |

### 4.2 用户服务接口（User Service）

#### 4.2.1 微信登录

**接口：** `POST /api/v1/auth/wechat/login`

**请求参数：**

```json
{
  "code": "wx_login_code"
}
```

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "user_id": "uuid",
    "access_token": "jwt_token",
    "refresh_token": "refresh_token",
    "expires_in": 7200,
    "user": {
      "id": "uuid",
      "nickname": "张三",
      "avatar_url": "https://...",
      "subscription_type": "free",
      "subscription_expiry": null
    }
  }
}
```

#### 4.2.2 获取用户信息

**接口：** `GET /api/v1/user/profile`

**请求头：**

```
Authorization: Bearer {access_token}
```

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "uuid",
    "openid": "wx_openid",
    "nickname": "张三",
    "avatar_url": "https://...",
    "phone": "13800138000",
    "email": "user@example.com",
    "target_university": "西安交通大学",
    "target_college": "电气工程学院",
    "target_major": "电气工程",
    "subscription_type": "premium_30d",
    "subscription_expiry": "2026-02-17T00:00:00Z",
    "total_practice_count": 50,
    "last_practice_time": "2026-01-17T10:30:00Z",
    "created_at": "2026-01-01T00:00:00Z"
  }
}
```

#### 4.2.3 更新用户信息

**接口：** `PUT /api/v1/user/profile`

**请求参数：**

```json
{
  "nickname": "李四",
  "phone": "13900139000",
  "target_university": "西安交通大学",
  "target_college": "电气工程学院",
  "target_major": "电气工程"
}
```

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "uuid",
    "nickname": "李四",
    "target_university": "西安交通大学",
    "target_college": "电气工程学院",
    "target_major": "电气工程"
  }
}
```

### 4.3 题库服务接口（Question Bank Service）

#### 4.3.1 获取题目列表

**接口：** `GET /api/v1/questions`

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | 否 | 题目类型：general/university/major |
| university | string | 否 | 院校名称 |
| major | string | 否 | 专业名称 |
| category | string | 否 | 题类 |
| difficulty | int | 否 | 难度：1-5 |
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 100,
    "page": 1,
    "page_size": 20,
    "questions": [
      {
        "id": "uuid",
        "type": "university",
        "university": "西安交通大学",
        "college": "电气工程学院",
        "major": "电气工程",
        "category": "专业背景",
        "difficulty": 3,
        "content": "Could you please introduce your research experience in electrical engineering?",
        "reference_answer": "I have been working on power system analysis for two years...",
        "tags": ["research", "power system"],
        "keywords": ["power system", "analysis", "stability"],
        "is_premium": true,
        "created_at": "2026-01-01T00:00:00Z"
      }
    ]
  }
}
```

#### 4.3.2 获取推荐题目

**接口：** `GET /api/v1/questions/recommend`

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| count | int | 否 | 推荐数量，默认10 |

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "questions": [
      {
        "id": "uuid",
        "type": "university",
        "university": "西安交通大学",
        "major": "电气工程",
        "category": "专业背景",
        "difficulty": 3,
        "content": "Could you please introduce your research experience in electrical engineering?",
        "match_score": 0.92,
        "reason": "与你的专业高度相关"
      }
    ]
  }
}
```

### 4.4 练习服务接口（Practice Service）

#### 4.4.1 创建练习会话

**接口：** `POST /api/v1/practice/sessions`

**请求参数：**

```json
{
  "mode": "university",
  "pressure_level": 2,
  "university": "西安交通大学",
  "major": "电气工程",
  "tutor_style_id": "uuid",
  "max_questions": 10
}
```

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "session_id": "uuid",
    "mode": "university",
    "pressure_level": 2,
    "university": "西安交通大学",
    "major": "电气工程",
    "tutor_style": {
      "id": "uuid",
      "name": "学术深挖型",
      "description": "深入挖掘理论背景"
    },
    "first_question": {
      "id": "uuid",
      "content": "Could you please introduce yourself?",
      "audio_url": "minio://audio/questions/uuid.mp3"
    },
    "websocket_url": "wss://api.empenglish.com/api/v1/practice/sessions/{session_id}/ws"
  }
}
```

#### 4.4.2 WebSocket实时交互

**接口：** `WS /api/v1/practice/sessions/{session_id}/ws`

**消息格式：**

**客户端 → 服务器（提交答案）：**

```json
{
  "type": "answer",
  "turn_id": "uuid",
  "audio_data": "base64_encoded_audio",
  "duration": 15
}
```

**服务器 → 客户端（评分结果）：**

```json
{
  "type": "score",
  "turn_id": "uuid",
  "score": {
    "overall": 85.5,
    "pronunciation": 88.0,
    "fluency": 82.0,
    "vocabulary": 85.0,
    "grammar": 87.0,
    "university_match": 84.0
  },
  "feedback": {
    "text": "Good answer! Your pronunciation is clear...",
    "audio_url": "minio://audio/feedback/uuid.mp3"
  },
  "follow_up_questions": [
    "What methodology did you use?"
  ]
}
```

**服务器 → 客户端（下一题）：**

```json
{
  "type": "question",
  "turn_id": "uuid",
  "question": {
    "id": "uuid",
    "content": "What is your research interest?",
    "audio_url": "minio://audio/questions/uuid.mp3"
  }
}
```

**服务器 → 客户端（会话结束）：**

```json
{
  "type": "session_end",
  "session_id": "uuid",
  "report_id": "uuid",
  "overall_score": 83.5,
  "statistics": {
    "total_turns": 10,
    "total_duration": 180,
    "avg_score": 83.5
  }
}
```

#### 4.4.3 获取练习会话详情

**接口：** `GET /api/v1/practice/sessions/{session_id}`

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "mode": "university",
    "pressure_level": 2,
    "university": "西安交通大学",
    "major": "电气工程",
    "status": "completed",
    "question_count": 10,
    "max_questions": 10,
    "start_time": "2026-01-17T10:00:00Z",
    "end_time": "2026-01-17T10:30:00Z",
    "duration": 1800,
    "overall_score": 83.5,
    "report_id": "uuid",
    "turns": [
      {
        "id": "uuid",
        "turn_number": 1,
        "question": "Could you please introduce yourself?",
        "overall_score": 85.5,
        "created_at": "2026-01-17T10:00:00Z"
      }
    ]
  }
}
```

#### 4.4.4 获取练习记录

**接口：** `GET /api/v1/practice/records`

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| mode | string | 否 | 练习模式 |
| status | string | 否 | 状态 |
| start_date | string | 否 | 开始日期 |
| end_date | string | 否 | 结束日期 |
| page | int | 否 | 页码 |
| page_size | int | 否 | 每页数量 |

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 50,
    "page": 1,
    "page_size": 20,
    "records": [
      {
        "id": "uuid",
        "mode": "university",
        "university": "西安交通大学",
        "major": "电气工程",
        "overall_score": 83.5,
        "question_count": 10,
        "duration": 1800,
        "start_time": "2026-01-17T10:00:00Z",
        "status": "completed"
      }
    ]
  }
}
```

### 4.5 评分服务接口（Scoring Service）

#### 4.5.1 提交评分请求

**接口：** `POST /api/v1/scoring/evaluate`

**请求参数：**

```json
{
  "turn_id": "uuid",
  "question": "Could you please introduce yourself?",
  "audio_url": "minio://audio/user/session1/turn1.mp3",
  "user_answer_text": "My name is Zhang Wei...",
  "university": "西安交通大学",
  "major": "电气工程",
  "dimensions": ["pronunciation", "fluency", "vocabulary", "grammar", "university_match"]
}
```

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "turn_id": "uuid",
    "overall_score": 85.5,
    "dimensions": {
      "pronunciation": {
        "score": 88.0,
        "details": [
          {
            "word": "pronunciation",
            "score": 85,
            "errors": []
          },
          {
            "word": "introduction",
            "score": 90,
            "errors": []
          }
        ]
      },
      "fluency": {
        "score": 82.0,
        "speech_rate": 135,
        "pause_frequency": 1.2,
        "avg_speech_length": 4.5
      },
      "vocabulary": {
        "score": 85.0,
        "diversity": 0.75,
        "advanced_words": ["consequently", "furthermore"],
        "word_count": 150
      },
      "grammar": {
        "score": 87.0,
        "errors": [],
        "sentence_variety": 0.8
      },
      "university_match": {
        "score": 84.0,
        "relevance": 0.85,
        "professional_terms": ["power system", "stability"],
        "suggestions": [
          "Try to include more specific terminology related to your major",
          "Mention specific courses or projects from your target university"
        ]
      }
    },
    "feedback": "Good introduction! Your pronunciation is clear and your grammar is correct. However, try to include more specific terminology related to electrical engineering to show your expertise.",
    "suggestions": [
      "Practice using more professional terminology",
      "Work on reducing pause frequency",
      "Include more specific examples from your field"
    ]
  }
}
```

#### 4.5.2 发音诊断

**接口：** `POST /api/v1/scoring/phoneme-diagnosis`

**请求参数：**

```json
{
  "turn_id": "uuid",
  "audio_url": "minio://audio/user/session1/turn1.mp3",
  "text": "My name is Zhang Wei and I am studying electrical engineering."
}
```

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "turn_id": "uuid",
    "overall_score": 85.0,
    "word_scores": [
      {
        "word": "electrical",
        "score": 82,
        "phoneme_errors": [
          {
            "correct": "/ɪ/",
            "actual": "/i/",
            "position": 3,
            "suggestion": "Try to pronounce the /ɪ/ sound as in 'bit'"
          }
        ]
      },
      {
        "word": "engineering",
        "score": 88,
        "phoneme_errors": []
      }
    ],
    "common_errors": [
      {
        "phoneme": "/θ/",
        "actual": "/s/",
        "frequency": 3,
        "suggestion": "Practice the /θ/ sound by putting your tongue between your teeth"
      }
    ]
  }
}
```

### 4.6 报告服务接口（Report Service）

#### 4.6.1 生成报告

**接口：** `POST /api/v1/reports/generate`

**请求参数：**

```json
{
  "type": "session",
  "session_id": "uuid"
}
```

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "report_id": "uuid",
    "type": "session",
    "title": "练习报告 - 西安交通大学电气工程",
    "overall_score": 83.5,
    "dimension_scores": {
      "pronunciation": 85.0,
      "fluency": 80.0,
      "vocabulary": 82.0,
      "grammar": 87.0,
      "university_match": 84.0
    },
    "radar_data": [
      {"dimension": "发音", "score": 85},
      {"dimension": "流利度", "score": 80},
      {"dimension": "词汇", "score": 82},
      {"dimension": "语法", "score": 87},
      {"dimension": "院校匹配", "score": 84}
    ],
    "error_summary": {
      "pronunciation_errors": [
        {"word": "electrical", "error": "/ɪ/ → /i/", "count": 2}
      ],
      "grammar_errors": [],
      "common_issues": [
        "Pause frequency is slightly high",
        "Could use more professional terminology"
      ]
    },
    "suggestions": [
      "Practice the /ɪ/ sound more frequently",
      "Include more professional terminology in your answers",
      "Work on reducing pause frequency"
    ],
    "training_plan": {
      "focus_areas": ["pronunciation", "vocabulary"],
      "recommended_questions": ["uuid1", "uuid2"],
      "daily_practice_time": 30
    },
    "created_at": "2026-01-17T10:45:00Z"
  }
}
```

#### 4.6.2 获取报告

**接口：** `GET /api/v1/reports/{report_id}`

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "session_id": "uuid",
    "type": "session",
    "title": "练习报告 - 西安交通大学电气工程",
    "overall_score": 83.5,
    "dimension_scores": {...},
    "radar_data": [...],
    "trend_data": {
      "dates": ["2026-01-10", "2026-01-11", "2026-01-12", "2026-01-13", "2026-01-14", "2026-01-15", "2026-01-17"],
      "scores": [78, 80, 79, 82, 81, 83, 83.5]
    },
    "error_summary": {...},
    "suggestions": [...],
    "training_plan": {...},
    "pdf_url": "minio://reports/uuid.pdf",
    "created_at": "2026-01-17T10:45:00Z"
  }
}
```

#### 4.6.3 导出PDF报告

**接口：** `GET /api/v1/reports/{report_id}/pdf`

**响应：** PDF文件流

### 4.7 支付服务接口（Payment Service）

#### 4.7.1 创建订单

**接口：** `POST /api/v1/orders`

**请求参数：**

```json
{
  "product_type": "premium_30d",
  "payment_method": "wechat"
}
```

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "order_id": "uuid",
    "order_no": "EMP20260117100001",
    "product_type": "premium_30d",
    "product_name": "30天冲刺包",
    "amount": 168.00,
    "discount_amount": 0.00,
    "actual_amount": 168.00,
    "status": "pending",
    "payment_params": {
      "appid": "wx1234567890",
      "noncestr": "random_string",
      "package": "prepay_id=wx1234567890",
      "timestamp": "1642394400",
      "sign": "signature"
    },
    "expired_at": "2026-01-17T11:00:00Z",
    "created_at": "2026-01-17T10:00:00Z"
  }
}
```

#### 4.7.2 支付回调

**接口：** `POST /api/v1/payments/wechat/callback`

**请求参数：** 微信支付回调数据

**响应数据：**

```json
{
  "code": 0,
  "message": "success"
}
```

#### 4.7.3 查询订单

**接口：** `GET /api/v1/orders/{order_id}`

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "uuid",
    "order_no": "EMP20260117100001",
    "product_type": "premium_30d",
    "product_name": "30天冲刺包",
    "amount": 168.00,
    "actual_amount": 168.00,
    "status": "paid",
    "paid_at": "2026-01-17T10:05:00Z",
    "created_at": "2026-01-17T10:00:00Z"
  }
}
```

### 4.8 AI服务接口（AI Service）

#### 4.8.1 ASR语音转写

**接口：** `POST /api/v1/ai/asr/transcribe`

**请求参数：**

```json
{
  "audio_url": "minio://audio/user/session1/turn1.mp3",
  "language": "en",
  "model": "whisper-large-v3"
}
```

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "text": "My name is Zhang Wei and I am studying electrical engineering at Xi'an Jiaotong University.",
    "language": "en",
    "language_probability": 0.99,
    "segments": [
      {
        "text": "My name is Zhang Wei",
        "start": 0.0,
        "end": 2.5
      },
      {
        "text": "and I am studying electrical engineering",
        "start": 2.5,
        "end": 5.0
      }
    ],
    "processing_time": 1.2
  }
}
```

#### 4.8.2 TTS语音合成

**接口：** `POST /api/v1/ai/tts/synthesize`

**请求参数：**

```json
{
  "text": "Good introduction! Your pronunciation is clear.",
  "voice": "female_us",
  "rate": "medium",
  "pitch": "medium"
}
```

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "audio_url": "minio://audio/tts/uuid.mp3",
    "duration": 3.5,
    "processing_time": 0.8
  }
}
```

#### 4.8.3 LLM对话

**接口：** `POST /api/v1/ai/llm/chat`

**请求参数：**

```json
{
  "model": "qwen2.5-7b",
  "messages": [
    {
      "role": "system",
      "content": "You are an English interview examiner."
    },
    {
      "role": "user",
      "content": "Generate an interview question about research experience."
    }
  ],
  "temperature": 0.7,
  "max_tokens": 500
}
```

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "chatcmpl-uuid",
    "model": "qwen2.5-7b",
    "choices": [
      {
        "index": 0,
        "message": {
          "role": "assistant",
          "content": "Could you please describe your research experience and explain how it relates to your field of study?"
        },
        "finish_reason": "stop"
      }
    ],
    "usage": {
      "prompt_tokens": 50,
      "completion_tokens": 30,
      "total_tokens": 80
    },
    "processing_time": 1.5
  }
}
```

#### 4.8.4 Agent面试流程

**接口：** `POST /api/v1/ai/agent/interview`

**请求参数：**

```json
{
  "session_id": "uuid",
  "user_id": "uuid",
  "university": "西安交通大学",
  "major": "电气工程",
  "pressure_level": 2,
  "tutor_style_id": "uuid",
  "action": "generate_question",
  "context": {
    "previous_questions": ["Could you please introduce yourself?"],
    "conversation_history": [...]
  }
}
```

**响应数据：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "action": "generate_question",
    "question": {
      "id": "uuid",
      "content": "What is your research interest in electrical engineering?",
      "audio_url": "minio://audio/questions/uuid.mp3"
    },
    "state": {
      "question_count": 2,
      "max_questions": 10,
      "is_finished": false
    }
  }
}
```

---

## 五、核心算法设计

### 5.1 ASR算法设计

#### 5.1.1 Whisper模型优化

**模型选择：**

| 模型 | 参数量 | 速度 | 准确率 | 推荐场景 |
|------|--------|------|--------|----------|
| whisper-tiny | 39M | 最快 | 中等 | 实时场景 |
| whisper-base | 74M | 快 | 中等 | 通用场景 |
| whisper-small | 244M | 中等 | 较高 | 高质量场景 |
| whisper-medium | 769M | 慢 | 高 | 离线场景 |
| whisper-large-v3 | 1550M | 最慢 | 最高 | 最高质量 |

**优化策略：**

1. **模型量化：**
```python
from faster_whisper import WhisperModel

# 使用int8量化
model = WhisperModel(
    "whisper-base",
    device="cuda",
    compute_type="int8_float16"  # 混合精度量化
)
```

2. **VAD过滤：**
```python
segments, info = model.transcribe(
    audio_path,
    language="en",
    beam_size=5,
    vad_filter=True,  # 启用VAD过滤
    vad_parameters={
        "threshold": 0.5,
        "min_speech_duration_ms": 250,
        "min_silence_duration_ms": 2000
    }
)
```

3. **中文口音优化：**
```python
# 使用中文口音微调的模型
model = WhisperModel(
    "whisper-base-chinese-accent",
    device="cuda",
    compute_type="float16"
)
```

#### 5.1.2 流式ASR实现

```python
import numpy as np
from faster_whisper import WhisperModel

class StreamingASR:
    def __init__(self, model_size="base", device="cuda"):
        self.model = WhisperModel(model_size, device=device)
        self.sample_rate = 16000
        self.chunk_size = 16000  # 1秒
        self.buffer = []
    
    def process_chunk(self, audio_chunk):
        """
        处理音频块
        """
        self.buffer.extend(audio_chunk)
        
        # 当缓冲区达到一定大小时进行转写
        if len(self.buffer) >= self.chunk_size * 3:  # 3秒
            audio_data = np.array(self.buffer, dtype=np.float32)
            
            segments, info = self.model.transcribe(
                audio_data,
                language="en",
                beam_size=5,
                vad_filter=True
            )
            
            result = []
            for segment in segments:
                result.append({
                    "text": segment.text,
                    "start": segment.start,
                    "end": segment.end
                })
            
            # 清空缓冲区
            self.buffer = []
            
            return result
        
        return None
    
    def finalize(self):
        """
        完成转写
        """
        if self.buffer:
            audio_data = np.array(self.buffer, dtype=np.float32)
            
            segments, info = self.model.transcribe(
                audio_data,
                language="en",
                beam_size=5
            )
            
            result = []
            for segment in segments:
                result.append({
                    "text": segment.text,
                    "start": segment.start,
                    "end": segment.end
                })
            
            return result
        
        return []
```

### 5.2 TTS算法设计

#### 5.2.1 Edge-TTS实现

```python
import edge_tts
import asyncio
import io

class TTSService:
    def __init__(self):
        self.voices = {
            "male_us": "en-US-GuyNeural",
            "female_us": "en-US-JennyNeural",
            "male_uk": "en-GB-RyanNeural",
            "female_uk": "en-GB-SoniaNeural"
        }
        
        self.style_presets = {
            "academic": {
                "voice": "male_us",
                "rate": "-10%",
                "pitch": "-10%",
                "volume": "+0%"
            },
            "friendly": {
                "voice": "female_us",
                "rate": "+0%",
                "pitch": "+0%",
                "volume": "+0%"
            },
            "high_pressure": {
                "voice": "male_us",
                "rate": "+20%",
                "pitch": "+10%",
                "volume": "+10%"
            }
        }
    
    async def synthesize(self, text, style="friendly"):
        """
        合成语音
        """
        preset = self.style_presets.get(style, self.style_presets["friendly"])
        voice = self.voices[preset["voice"]]
        
        communicate = edge_tts.Communicate(
            text,
            voice,
            rate=preset["rate"],
            pitch=preset["pitch"],
            volume=preset["volume"]
        )
        
        audio_data = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.write(chunk["data"])
        
        audio_data.seek(0)
        return audio_data.getvalue()
    
    def synthesize_sync(self, text, style="friendly"):
        """
        同步合成
        """
        return asyncio.run(self.synthesize(text, style))
```

#### 5.2.2 VITS本地部署

```python
import torch
from vits import VITSModel

class VITSService:
    def __init__(self, model_path, config_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = VITSModel(config_path)
        self.model.load_state_dict(torch.load(model_path))
        self.model.to(self.device)
        self.model.eval()
    
    def synthesize(self, text, speaker_id=0):
        """
        合成语音
        """
        with torch.no_grad():
            audio = self.model.inference(text, speaker_id)
        
        return audio.cpu().numpy()
```

### 5.3 评分算法设计

#### 5.3.1 GOP发音评分算法

```python
import numpy as np
import torch
import torchaudio

class GOPScorer:
    def __init__(self, acoustic_model_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.sample_rate = 16000
        
        # 加载声学模型
        self.acoustic_model = torch.load(acoustic_model_path)
        self.acoustic_model.to(self.device)
        self.acoustic_model.eval()
        
        # 音素映射
        self.phoneme_map = self._load_phoneme_map()
    
    def _load_phoneme_map(self):
        """
        加载音素映射
        """
        return {
            "AA": 0, "AE": 1, "AH": 2, "AO": 3, "AW": 4,
            "AY": 5, "B": 6, "CH": 7, "D": 8, "DH": 9,
            "EH": 10, "ER": 11, "EY": 12, "F": 13, "G": 14,
            "HH": 15, "IH": 16, "IY": 17, "JH": 18, "K": 19,
            "L": 20, "M": 21, "N": 22, "NG": 23, "OW": 24,
            "OY": 25, "P": 26, "R": 27, "S": 28, "SH": 29,
            "T": 30, "TH": 31, "UH": 32, "UW": 33, "V": 34,
            "W": 35, "Y": 36, "Z": 37, "ZH": 38
        }
    
    def extract_features(self, audio_path):
        """
        提取MFCC特征
        """
        waveform, sample_rate = torchaudio.load(audio_path)
        
        # 重采样
        if sample_rate != self.sample_rate:
            resampler = torchaudio.transforms.Resample(sample_rate, self.sample_rate)
            waveform = resampler(waveform)
        
        # 提取MFCC
        mfcc_transform = torchaudio.transforms.MFCC(
            sample_rate=self.sample_rate,
            n_mfcc=13,
            melkwargs={
                "n_fft": 512,
                "hop_length": 160,
                "n_mels": 40
            }
        )
        
        mfcc = mfcc_transform(waveform)
        
        # 添加一阶和二阶差分
        delta = torchaudio.functional.compute_deltas(mfcc)
        delta_delta = torchaudio.functional.compute_deltas(delta)
        
        features = torch.cat([mfcc, delta, delta_delta], dim=1)
        
        return features.squeeze(0).numpy()
    
    def forced_alignment(self, features, text):
        """
        强制对齐
        """
        # 文本转音素序列
        phonemes = self._text_to_phonemes(text)
        
        # 使用声学模型进行对齐
        with torch.no_grad():
            features_tensor = torch.from_numpy(features).unsqueeze(0).to(self.device)
            phoneme_ids = [self.phoneme_map.get(p, 0) for p in phonemes]
            phoneme_tensor = torch.tensor(phoneme_ids).unsqueeze(0).to(self.device)
            
            alignments = self.acoustic_model.align(features_tensor, phoneme_tensor)
        
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
            posterior_prob = self._calculate_posterior_prob(features, alignment)
            
            # 计算GOP分数（对数后验概率）
            gop_score = np.log(posterior_prob + 1e-10)
            
            # 归一化到0-100
            normalized_score = self._normalize_score(gop_score)
            
            phoneme_scores.append({
                "phoneme": alignment["phoneme"],
                "score": normalized_score,
                "confidence": posterior_prob
            })
        
        # 计算整体得分
        overall_score = np.mean([p["score"] for p in phoneme_scores])
        
        return {
            "overall_score": overall_score,
            "phoneme_scores": phoneme_scores,
            "alignments": alignments
        }
    
    def _calculate_posterior_prob(self, features, alignment):
        """
        计算后验概率
        """
        start_frame = alignment["start_frame"]
        end_frame = alignment["end_frame"]
        
        # 提取对应帧的特征
        frame_features = features[start_frame:end_frame]
        
        # 使用声学模型计算后验概率
        with torch.no_grad():
            features_tensor = torch.from_numpy(frame_features).unsqueeze(0).to(self.device)
            posterior = self.acoustic_model.forward(features_tensor)
        
        # 取最大概率
        max_prob = torch.max(posterior).item()
        
        return max_prob
    
    def _normalize_score(self, score):
        """
        归一化分数到0-100
        """
        # 使用sigmoid函数
        normalized = 1 / (1 + np.exp(-score))
        
        # 映射到0-100
        return normalized * 100
    
    def _text_to_phonemes(self, text):
        """
        文本转音素
        """
        # 这里可以使用CMU词典或其他音素转换工具
        # 简化实现
        return ["IH", "N", "T", "R", "AH", "D", "AH", "K", "SH", "AH", "N"]
```

#### 5.3.2 流利度评分算法

```python
import numpy as np
import torch
import torchaudio

class FluencyScorer:
    def __init__(self):
        self.sample_rate = 16000
        self.energy_threshold = 0.01
        self.min_pause_duration = 0.3  # 300ms
    
    def calculate_fluency_score(self, audio_path, text):
        """
        计算流利度分数
        """
        waveform, sample_rate = torchaudio.load(audio_path)
        
        # 重采样
        if sample_rate != self.sample_rate:
            resampler = torchaudio.transforms.Resample(sample_rate, self.sample_rate)
            waveform = resampler(waveform)
        
        waveform = waveform.squeeze().numpy()
        duration = len(waveform) / self.sample_rate
        
        # 计算语速
        speech_rate = self._calculate_speech_rate(text, duration)
        
        # 检测停顿
        pauses = self._detect_pauses(waveform)
        
        # 计算平均语流长度
        avg_speech_length = self._calculate_avg_speech_length(pauses, duration)
        
        # 计算停顿频率
        pause_frequency = len(pauses) / duration * 60  # 每分钟停顿次数
        
        # 计算综合得分
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
            "pauses": pauses,
            "details": {
                "rate_score": self._calculate_rate_score(speech_rate),
                "length_score": self._calculate_length_score(avg_speech_length),
                "pause_score": self._calculate_pause_score(pause_frequency)
            }
        }
    
    def _calculate_speech_rate(self, text, duration):
        """
        计算语速（词/分钟）
        """
        word_count = len(text.split())
        speech_rate = word_count / (duration / 60)
        return speech_rate
    
    def _detect_pauses(self, waveform):
        """
        检测停顿
        """
        # 计算能量
        frame_length = int(0.02 * self.sample_rate)  # 20ms
        hop_length = int(0.01 * self.sample_rate)  # 10ms
        
        energy = []
        for i in range(0, len(waveframe) - frame_length, hop_length):
            frame = waveform[i:i + frame_length]
            frame_energy = np.mean(np.abs(frame))
            energy.append(frame_energy)
        
        energy = np.array(energy)
        
        # 检测停顿
        pauses = []
        in_pause = False
        pause_start = 0
        
        for i, e in enumerate(energy):
            time = i * hop_length / self.sample_rate
            
            if e < self.energy_threshold and not in_pause:
                in_pause = True
                pause_start = time
            elif e >= self.energy_threshold and in_pause:
                in_pause = False
                pause_end = time
                pause_duration = pause_end - pause_start
                
                if pause_duration >= self.min_pause_duration:
                    pauses.append({
                        "start": pause_start,
                        "end": pause_end,
                        "duration": pause_duration
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
        计算综合得分
        """
        rate_score = self._calculate_rate_score(speech_rate)
        length_score = self._calculate_length_score(avg_speech_length)
        pause_score = self._calculate_pause_score(pause_frequency)
        
        # 加权平均
        composite_score = (
            rate_score * 0.4 +
            length_score * 0.3 +
            pause_score * 0.3
        )
        
        return composite_score
    
    def _calculate_rate_score(self, speech_rate):
        """
        语速评分（理想值：120-150 wpm）
        """
        if 120 <= speech_rate <= 150:
            return 100
        elif speech_rate < 120:
            return (speech_rate / 120) * 100
        else:
            return max(0, 100 - (speech_rate - 150) * 2)
    
    def _calculate_length_score(self, avg_speech_length):
        """
        语流长度评分（理想值：> 3秒）
        """
        return min(100, avg_speech_length * 30)
    
    def _calculate_pause_score(self, pause_frequency):
        """
        停顿频率评分（理想值：< 2次/分钟）
        """
        if pause_frequency < 2:
            return 100
        else:
            return max(0, 100 - (pause_frequency - 2) * 20)
```

#### 5.3.3 词汇多样性评分

```python
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords

class VocabularyScorer:
    def __init__(self):
        # 下载停用词
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
        
        # 高级词汇列表
        self.advanced_words = self._load_advanced_words()
    
    def _load_advanced_words(self):
        """
        加载高级词汇列表
        """
        return [
            "consequently", "furthermore", "nevertheless", "nonetheless",
            "moreover", "therefore", "thus", "hence", "accordingly",
            "subsequently", "simultaneously", "predominantly", "significantly",
            "substantially", "considerably", "remarkably", "notably",
            "fundamentally", "essentially", "inherently", "intrinsically"
        ]
    
    def calculate_vocabulary_score(self, text):
        """
        计算词汇多样性分数
        """
        # 预处理
        words = self._preprocess(text)
        
        if not words:
            return {
                "overall_score": 0,
                "diversity": 0,
                "advanced_count": 0,
                "word_count": 0,
                "unique_count": 0
            }
        
        # 计算词汇多样性（TTR）
        ttr = self._calculate_ttr(words)
        
        # 计算高级词汇使用
        advanced_words = self._find_advanced_words(words)
        
        # 计算词汇丰富度
        richness = self._calculate_richness(words)
        
        # 综合评分
        overall_score = self._calculate_composite_score(ttr, advanced_words, richness)
        
        return {
            "overall_score": overall_score,
            "diversity": ttr,
            "advanced_words": advanced_words,
            "advanced_count": len(advanced_words),
            "word_count": len(words),
            "unique_count": len(set(words)),
            "richness": richness
        }
    
    def _preprocess(self, text):
        """
        预处理文本
        """
        # 转小写
        text = text.lower()
        
        # 移除标点
        text = re.sub(r'[^\w\s]', '', text)
        
        # 分词
        words = text.split()
        
        # 移除停用词
        words = [w for w in words if w not in self.stop_words]
        
        # 过滤短词
        words = [w for w in words if len(w) > 2]
        
        return words
    
    def _calculate_ttr(self, words):
        """
        计算类型-标记比（Type-Token Ratio）
        """
        if not words:
            return 0
        
        unique_words = len(set(words))
        total_words = len(words)
        
        # 标准化TTR（考虑文本长度）
        standardized_ttr = (unique_words / total_words) * 100
        
        return standardized_ttr
    
    def _find_advanced_words(self, words):
        """
        查找高级词汇
        """
        advanced = []
        for word in words:
            if word in self.advanced_words:
                advanced.append(word)
        
        return advanced
    
    def _calculate_richness(self, words):
        """
        计算词汇丰富度
        """
        if not words:
            return 0
        
        # 词长分布
        word_lengths = [len(w) for w in words]
        avg_length = np.mean(word_lengths)
        
        # 长词比例（长度>6）
        long_word_ratio = sum(1 for l in word_lengths if l > 6) / len(words)
        
        # 综合丰富度
        richness = (avg_length / 10) * 0.5 + long_word_ratio * 0.5
        
        return richness * 100
    
    def _calculate_composite_score(self, ttr, advanced_words, richness):
        """
        计算综合得分
        """
        # TTR评分（理想值：> 50）
        ttr_score = min(100, ttr * 2)
        
        # 高级词汇评分
        advanced_score = min(100, len(advanced_words) * 20)
        
        # 丰富度评分
        richness_score = richness
        
        # 加权平均
        composite_score = (
            ttr_score * 0.4 +
            advanced_score * 0.3 +
            richness_score * 0.3
        )
        
        return composite_score
```

### 5.4 Agent编排设计

#### 5.4.1 LangGraph工作流定义

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional, Annotated
import operator

class InterviewState(TypedDict):
    """面试状态"""
    user_id: str
    session_id: str
    university: Optional[str]
    major: Optional[str]
    pressure_level: int
    tutor_style_id: Optional[str]
    
    # 当前轮次
    current_question: Optional[str]
    current_question_id: Optional[str]
    user_answer: Optional[str]
    user_answer_audio_url: Optional[str]
    
    # 评分结果
    score: Optional[dict]
    feedback: Optional[str]
    feedback_audio_url: Optional[str]
    
    # 追问
    follow_up_questions: List[str]
    
    # 对话历史
    conversation_history: List[dict]
    
    # 统计
    question_count: int
    max_questions: int
    
    # 状态
    is_finished: bool
    
    # 报告
    report: Optional[dict]

class InterviewAgent:
    def __init__(self, services):
        self.llm_service = services["llm"]
        self.asr_service = services["asr"]
        self.tts_service = services["tts"]
        self.question_bank = services["question_bank"]
        self.scoring_service = services["scoring"]
        self.report_service = services["report"]
        
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """构建Agent工作流"""
        graph = StateGraph(InterviewState)
        
        # 添加节点
        graph.add_node("generate_question", self._generate_question)
        graph.add_node("transcribe_audio", self._transcribe_audio)
        graph.add_node("score_answer", self._score_answer)
        graph.add_node("generate_feedback", self._generate_feedback)
        graph.add_node("synthesize_feedback_audio", self._synthesize_feedback_audio)
        graph.add_node("generate_follow_up", self._generate_follow_up)
        graph.add_node("check_completion", self._check_completion)
        graph.add_node("generate_report", self._generate_report)
        
        # 添加边
        graph.set_entry_point("generate_question")
        graph.add_edge("generate_question", "transcribe_audio")
        graph.add_edge("transcribe_audio", "score_answer")
        graph.add_edge("score_answer", "generate_feedback")
        graph.add_edge("generate_feedback", "synthesize_feedback_audio")
        graph.add_edge("synthesize_feedback_audio", "generate_follow_up")
        graph.add_edge("generate_follow_up", "check_completion")
        
        # 条件边
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
        # 获取题目
        question = self.question_bank.get_next_question(
            user_id=state["user_id"],
            university=state["university"],
            major=state["major"],
            previous_questions=state["conversation_history"],
            question_count=state["question_count"]
        )
        
        # 更新状态
        state["current_question"] = question["content"]
        state["current_question_id"] = question["id"]
        
        # 添加到历史
        state["conversation_history"].append({
            "turn_id": len(state["conversation_history"]) + 1,
            "question": question["content"],
            "question_id": question["id"],
            "answer": None,
            "score": None
        })
        
        return state
    
    def _transcribe_audio(self, state: InterviewState) -> InterviewState:
        """语音转写"""
        if state["user_answer_audio_url"]:
            # 调用ASR服务
            result = self.asr_service.transcribe(
                audio_url=state["user_answer_audio_url"],
                language="en"
            )
            state["user_answer"] = result["text"]
        
        return state
    
    def _score_answer(self, state: InterviewState) -> InterviewState:
        """评分"""
        # 调用评分服务
        score_result = self.scoring_service.evaluate(
            question=state["current_question"],
            answer=state["user_answer"],
            audio_url=state["user_answer_audio_url"],
            university=state["university"],
            major=state["major"]
        )
        
        state["score"] = score_result
        
        # 更新历史
        state["conversation_history"][-1]["answer"] = state["user_answer"]
        state["conversation_history"][-1]["score"] = score_result
        
        return state
    
    def _generate_feedback(self, state: InterviewState) -> InterviewState:
        """生成反馈"""
        # 使用LLM生成反馈
        feedback = self.llm_service.generate_feedback(
            question=state["current_question"],
            answer=state["user_answer"],
            score=state["score"]
        )
        
        state["feedback"] = feedback
        
        return state
    
    def _synthesize_feedback_audio(self, state: InterviewState) -> InterviewState:
        """合成反馈语音"""
        if state["feedback"]:
            # 根据压力等级选择风格
            style = self._get_tts_style(state["pressure_level"])
            
            audio_url = self.tts_service.synthesize(
                text=state["feedback"],
                style=style
            )
            
            state["feedback_audio_url"] = audio_url
        
        return state
    
    def _generate_follow_up(self, state: InterviewState) -> InterviewState:
        """生成追问"""
        # 使用LLM生成追问
        follow_up = self.llm_service.generate_follow_up(
            question=state["current_question"],
            answer=state["user_answer"],
            pressure_level=state["pressure_level"],
            tutor_style_id=state["tutor_style_id"]
        )
        
        state["follow_up_questions"] = follow_up
        
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
        # 调用报告服务
        report = self.report_service.generate(
            session_id=state["session_id"],
            conversation_history=state["conversation_history"]
        )
        
        state["report"] = report
        
        return state
    
    def _get_tts_style(self, pressure_level):
        """获取TTS风格"""
        style_map = {
            1: "friendly",
            2: "academic",
            3: "high_pressure"
        }
        return style_map.get(pressure_level, "academic")
    
    def run(self, initial_state: InterviewState):
        """运行Agent"""
        return self.graph.invoke(initial_state)
```

---

## 六、消息队列设计

### 6.1 RabbitMQ队列定义

#### 6.1.1 队列列表

| 队列名 | 用途 | 路由键 |
|--------|------|--------|
| practice.audio_upload | 音频上传处理 | practice.audio.upload |
| practice.scoring | 评分任务 | practice.scoring |
| practice.report | 报告生成 | practice.report |
| notification.email | 邮件通知 | notification.email |
| notification.push | 推送通知 | notification.push |
| analytics.event | 事件统计 | analytics.event |

#### 6.1.2 消息格式

**音频上传消息：**

```json
{
  "message_id": "uuid",
  "timestamp": "2026-01-17T10:30:00Z",
  "type": "audio_upload",
  "data": {
    "session_id": "uuid",
    "turn_id": "uuid",
    "user_id": "uuid",
    "audio_url": "minio://audio/user/session1/turn1.mp3",
    "duration": 15
  }
}
```

**评分任务消息：**

```json
{
  "message_id": "uuid",
  "timestamp": "2026-01-17T10:30:00Z",
  "type": "scoring",
  "data": {
    "turn_id": "uuid",
    "question": "Could you please introduce yourself?",
    "audio_url": "minio://audio/user/session1/turn1.mp3",
    "user_answer_text": "My name is Zhang Wei...",
    "university": "西安交通大学",
    "major": "电气工程"
  }
}
```

**报告生成消息：**

```json
{
  "message_id": "uuid",
  "timestamp": "2026-01-17T10:30:00Z",
  "type": "report",
  "data": {
    "report_id": "uuid",
    "session_id": "uuid",
    "user_id": "uuid",
    "type": "session"
  }
}
```

### 6.2 Celery任务定义

```python
from celery import Celery
from datetime import timedelta

# Celery配置
celery_app = Celery(
    'empenglish',
    broker='amqp://guest:guest@localhost:5672//',
    backend='redis://localhost:6379/0'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30分钟
    task_soft_time_limit=25 * 60,  # 25分钟
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000
)

# 音频上传处理任务
@celery_app.task(bind=True, name='practice.audio_upload')
def process_audio_upload(self, turn_id, audio_url):
    """
    处理音频上传
    """
    from services.audio_service import AudioService
    
    audio_service = AudioService()
    
    # 验证音频
    result = audio_service.validate_audio(audio_url)
    
    if not result["valid"]:
        raise Exception(f"Invalid audio: {result['error']}")
    
    # 转换格式
    converted_url = audio_service.convert_format(audio_url, target_format="mp3")
    
    # 更新数据库
    from db.models import PracticeTurn
    turn = PracticeTurn.get_by_id(turn_id)
    turn.user_answer_audio_url = converted_url
    turn.save()
    
    return {"turn_id": turn_id, "converted_url": converted_url}

# 评分任务
@celery_app.task(bind=True, name='practice.scoring')
def score_answer(self, turn_id, question, audio_url, user_answer_text, university=None, major=None):
    """
    评分任务
    """
    from services.scoring_service import ScoringService
    
    scoring_service = ScoringService()
    
    # 执行评分
    result = scoring_service.evaluate(
        question=question,
        answer=user_answer_text,
        audio_url=audio_url,
        university=university,
        major=major
    )
    
    # 保存结果
    from db.models import PracticeTurn, ScoringRecord
    turn = PracticeTurn.get_by_id(turn_id)
    turn.overall_score = result["overall_score"]
    turn.pronunciation_score = result["dimensions"]["pronunciation"]["score"]
    turn.fluency_score = result["dimensions"]["fluency"]["score"]
    turn.vocabulary_score = result["dimensions"]["vocabulary"]["score"]
    turn.grammar_score = result["dimensions"]["grammar"]["score"]
    turn.save()
    
    # 保存详细评分记录
    for dimension, score_data in result["dimensions"].items():
        ScoringRecord.create(
            turn_id=turn_id,
            user_id=turn.session.user_id,
            dimension=dimension,
            score=score_data["score"],
            details=score_data.get("details", {}),
            suggestions=score_data.get("suggestions", [])
        )
    
    return {"turn_id": turn_id, "score": result["overall_score"]}

# 报告生成任务
@celery_app.task(bind=True, name='practice.report')
def generate_report(self, report_id, session_id, user_id, report_type):
    """
    生成报告
    """
    from services.report_service import ReportService
    
    report_service = ReportService()
    
    # 生成报告
    result = report_service.generate(
        report_id=report_id,
        session_id=session_id,
        user_id=user_id,
        report_type=report_type
    )
    
    return {"report_id": report_id, "status": "completed"}

# 定时任务：生成每日报告
@celery_app.task(name='reports.daily')
def generate_daily_reports():
    """
    生成每日报告
    """
    from services.report_service import ReportService
    from db.models import User
    
    # 获取所有活跃用户
    users = User.get_active_users()
    
    for user in users:
        # 检查是否需要生成每日报告
        if user.needs_daily_report():
            report_service = ReportService()
            report_service.generate_daily_report(user.id)
    
    return {"processed": len(users)}

# 配置定时任务
celery_app.conf.beat_schedule = {
    'generate-daily-reports': {
        'task': 'reports.daily',
        'schedule': timedelta(hours=1),  # 每小时执行一次
    },
}
```

---

## 七、安全设计

### 7.1 认证与授权

#### 7.1.1 JWT Token设计

```python
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any

class JWTManager:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def generate_access_token(self, user_id: str, payload: Dict[str, Any] = None) -> str:
        """
        生成访问令牌
        """
        now = datetime.utcnow()
        
        default_payload = {
            "user_id": user_id,
            "type": "access",
            "iat": now,
            "exp": now + timedelta(hours=2)  # 2小时过期
        }
        
        if payload:
            default_payload.update(payload)
        
        token = jwt.encode(default_payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def generate_refresh_token(self, user_id: str) -> str:
        """
        生成刷新令牌
        """
        now = datetime.utcnow()
        
        payload = {
            "user_id": user_id,
            "type": "refresh",
            "iat": now,
            "exp": now + timedelta(days=7)  # 7天过期
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        验证令牌
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """
        刷新访问令牌
        """
        payload = self.verify_token(refresh_token)
        
        if payload["type"] != "refresh":
            raise Exception("Invalid refresh token")
        
        return self.generate_access_token(payload["user_id"])
```

#### 7.1.2 RBAC权限控制

```python
from enum import Enum
from functools import wraps
from fastapi import HTTPException, Depends

class Role(Enum):
    """角色枚举"""
    USER = "user"
    ADMIN = "admin"
    INSTITUTION = "institution"

class Permission(Enum):
    """权限枚举"""
    # 用户权限
    PRACTICE_GENERAL = "practice:general"
    PRACTICE_UNIVERSITY = "practice:university"
    VIEW_REPORT = "report:view"
    EXPORT_REPORT = "report:export"
    
    # 管理员权限
    MANAGE_QUESTIONS = "questions:manage"
    MANAGE_USERS = "users:manage"
    VIEW_ANALYTICS = "analytics:view"
    
    # 机构权限
    VIEW_INSTITUTION_STUDENTS = "institution:students:view"
    MANAGE_INSTITUTION_STUDENTS = "institution:students:manage"

# 角色权限映射
ROLE_PERMISSIONS = {
    Role.USER: [
        Permission.PRACTICE_GENERAL,
        Permission.VIEW_REPORT
    ],
    Role.ADMIN: [
        Permission.PRACTICE_GENERAL,
        Permission.PRACTICE_UNIVERSITY,
        Permission.VIEW_REPORT,
        Permission.EXPORT_REPORT,
        Permission.MANAGE_QUESTIONS,
        Permission.MANAGE_USERS,
        Permission.VIEW_ANALYTICS
    ],
    Role.INSTITUTION: [
        Permission.PRACTICE_GENERAL,
        Permission.PRACTICE_UNIVERSITY,
        Permission.VIEW_REPORT,
        Permission.EXPORT_REPORT,
        Permission.VIEW_INSTITUTION_STUDENTS,
        Permission.MANAGE_INSTITUTION_STUDENTS
    ]
}

def require_permission(permission: Permission):
    """
    权限装饰器
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 获取当前用户
            current_user = kwargs.get("current_user")
            
            if not current_user:
                raise HTTPException(status_code=401, detail="Unauthorized")
            
            # 检查权限
            user_role = Role(current_user.role)
            user_permissions = ROLE_PERMISSIONS.get(user_role, [])
            
            if permission not in user_permissions:
                raise HTTPException(status_code=403, detail="Forbidden")
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator
```

### 7.2 数据加密

#### 7.2.1 敏感数据加密

```python
from cryptography.fernet import Fernet
import base64
import hashlib

class EncryptionManager:
    def __init__(self, secret_key: str):
        # 生成加密密钥
        key = hashlib.sha256(secret_key.encode()).digest()
        self.cipher = Fernet(base64.urlsafe_b64encode(key))
    
    def encrypt(self, data: str) -> str:
        """
        加密数据
        """
        encrypted = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        解密数据
        """
        encrypted = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = self.cipher.decrypt(encrypted)
        return decrypted.decode()
    
    def encrypt_phone(self, phone: str) -> str:
        """
        加密手机号
        """
        # 手机号脱敏：保留前3后4
        masked = phone[:3] + "****" + phone[-4:]
        return self.encrypt(masked)
    
    def encrypt_email(self, email: str) -> str:
        """
        加密邮箱
        """
        # 邮箱脱敏：保留首字母和域名
        parts = email.split("@")
        username = parts[0][0] + "***"
        masked = f"{username}@{parts[1]}"
        return self.encrypt(masked)
```

### 7.3 接口限流

```python
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

# 限流器
limiter = Limiter(key_func=get_remote_address)

# 限流规则
RATE_LIMITS = {
    "default": "100/minute",  # 默认：每分钟100次
    "auth": "10/minute",      # 认证：每分钟10次
    "practice": "20/minute",  # 练习：每分钟20次
    "upload": "5/minute",     # 上传：每分钟5次
}

# 使用示例
@app.post("/api/v1/auth/wechat/login")
@limiter.limit(RATE_LIMITS["auth"])
async def wechat_login(request: Request, code: str):
    pass

@app.post("/api/v1/practice/sessions")
@limiter.limit(RATE_LIMITS["practice"])
async def create_session(request: Request, session_data: SessionCreate):
    pass
```

### 7.4 音频安全

```python
import magic
import os
from pathlib import Path

class AudioValidator:
    """音频验证器"""
    
    ALLOWED_TYPES = [
        "audio/mpeg",
        "audio/wav",
        "audio/ogg",
        "audio/webm"
    ]
    
    MAX_SIZE = 10 * 1024 * 1024  # 10MB
    MIN_DURATION = 1  # 最小1秒
    MAX_DURATION = 300  # 最大5分钟
    
    @classmethod
    def validate(cls, file_path: str) -> dict:
        """
        验证音频文件
        """
        result = {
            "valid": True,
            "errors": []
        }
        
        # 检查文件大小
        file_size = os.path.getsize(file_path)
        if file_size > cls.MAX_SIZE:
            result["valid"] = False
            result["errors"].append(f"File size exceeds {cls.MAX_SIZE} bytes")
        
        # 检查文件类型
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        
        if file_type not in cls.ALLOWED_TYPES:
            result["valid"] = False
            result["errors"].append(f"Invalid file type: {file_type}")
        
        # 检查音频时长
        try:
            import librosa
            y, sr = librosa.load(file_path, sr=None)
            duration = len(y) / sr
            
            if duration < cls.MIN_DURATION:
                result["valid"] = False
                result["errors"].append(f"Audio duration too short: {duration}s")
            
            if duration > cls.MAX_DURATION:
                result["valid"] = False
                result["errors"].append(f"Audio duration too long: {duration}s")
        except Exception as e:
            result["valid"] = False
            result["errors"].append(f"Failed to analyze audio: {str(e)}")
        
        return result
```

---

## 八、监控与日志

### 8.1 Prometheus指标定义

```python
from prometheus_client import Counter, Histogram, Gauge, Summary

# HTTP请求计数器
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# HTTP请求延迟
http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0]
)

# ASR处理延迟
asr_processing_duration = Histogram(
    'asr_processing_duration_seconds',
    'ASR processing latency',
    ['model'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

# LLM处理延迟
llm_processing_duration = Histogram(
    'llm_processing_duration_seconds',
    'LLM processing latency',
    ['model'],
    buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0]
)

# 评分处理延迟
scoring_processing_duration = Histogram(
    'scoring_processing_duration_seconds',
    'Scoring processing latency',
    ['dimension'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

# 活跃会话数
active_sessions = Gauge(
    'active_sessions',
    'Number of active practice sessions'
)

# 在线用户数
online_users = Gauge(
    'online_users',
    'Number of online users'
)

# 队列任务数
queue_tasks = Gauge(
    'queue_tasks',
    'Number of tasks in queue',
    ['queue_name']
)

# 数据库连接池
db_connections = Gauge(
    'db_connections',
    'Database connections',
    ['pool_name', 'state']
)

# 缓存命中率
cache_hit_rate = Gauge(
    'cache_hit_rate',
    'Cache hit rate',
    ['cache_name']
)

# 错误计数器
errors_total = Counter(
    'errors_total',
    'Total errors',
    ['type', 'endpoint']
)
```

### 8.2 日志格式定义

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """JSON日志格式化器"""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # 添加额外字段
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        
        if hasattr(record, 'session_id'):
            log_data['session_id'] = record.session_id
        
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)

# 日志配置
def setup_logging():
    """配置日志"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)
    
    # 文件处理器
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)
```

### 8.3 告警规则定义

```yaml
# prometheus_alerts.yml
groups:
  - name: empenglish_alerts
    interval: 30s
    rules:
      # 高错误率告警
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} for the last 5 minutes"
      
      # 高延迟告警
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "P95 latency is {{ $value }}s"
      
      # ASR处理延迟告警
      - alert: HighASRLatency
        expr: histogram_quantile(0.95, rate(asr_processing_duration_seconds_bucket[5m])) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High ASR processing latency"
          description: "P95 ASR latency is {{ $value }}s"
      
      # LLM处理延迟告警
      - alert: HighLLMLatency
        expr: histogram_quantile(0.95, rate(llm_processing_duration_seconds_bucket[5m])) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High LLM processing latency"
          description: "P95 LLM latency is {{ $value }}s"
      
      # 数据库连接池告警
      - alert: DatabaseConnectionPoolExhausted
        expr: db_connections{state="idle"} < 5
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Database connection pool exhausted"
          description: "Only {{ $value }} idle connections available"
      
      # 队列积压告警
      - alert: QueueBacklog
        expr: queue_tasks > 100
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Queue backlog detected"
          description: "{{ $labels.queue_name }} has {{ $value }} pending tasks"
      
      # 缓存命中率低告警
      - alert: LowCacheHitRate
        expr: cache_hit_rate < 0.5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Low cache hit rate"
          description: "{{ $labels.cache_name }} hit rate is {{ $value }}"
```

---

## 九、部署配置

### 9.1 Docker配置

#### 9.1.1 用户服务Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8001

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8001/health || exit 1

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

#### 9.1.2 ASR服务Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 下载模型（如果需要）
RUN python scripts/download_models.py

# 暴露端口
EXPOSE 9001

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:9001/health || exit 1

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9001"]
```

### 9.2 Kubernetes配置

#### 9.2.1 用户服务部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  namespace: empenglish
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
      - name: user-service
        image: empenglish/user-service:latest
        ports:
        - containerPort: 8001
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-secret
              key: url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: redis-secret
              key: url
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: jwt-secret
              key: secret
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: empenglish
spec:
  selector:
    app: user-service
  ports:
  - protocol: TCP
    port: 8001
    targetPort: 8001
  type: ClusterIP
```

#### 9.2.2 ASR服务部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: asr-service
  namespace: empenglish
spec:
  replicas: 3
  selector:
    matchLabels:
      app: asr-service
  template:
    metadata:
      labels:
        app: asr-service
    spec:
      containers:
      - name: asr-service
        image: empenglish/asr-service:latest
        ports:
        - containerPort: 9001
        env:
        - name: MODEL_PATH
          value: "/models/whisper-base"
        - name: DEVICE
          value: "cuda"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
            nvidia.com/gpu: 1
          limits:
            memory: "4Gi"
            cpu: "2000m"
            nvidia.com/gpu: 1
        volumeMounts:
        - name: models
          mountPath: /models
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: models-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: asr-service
  namespace: empenglish
spec:
  selector:
    app: asr-service
  ports:
  - protocol: TCP
    port: 9001
    targetPort: 9001
  type: ClusterIP
```

### 9.3 Kong API网关配置

```yaml
# Kong配置
_format_version: "3.0"

services:
  # 用户服务
  - name: user-service
    url: http://user-service.empenglish.svc.cluster.local:8001
    routes:
      - name: user-routes
        paths:
          - /api/v1/user
          - /api/v1/auth
        strip_path: false
    plugins:
      - name: rate-limiting
        config:
          minute: 100
          policy: redis
          redis_host: redis.empenglish.svc.cluster.local
          redis_port: 6379
      - name: jwt
        config:
          claims_to_verify:
            - exp
  
  # 题库服务
  - name: question-bank-service
    url: http://question-bank-service.empenglish.svc.cluster.local:8002
    routes:
      - name: question-routes
        paths:
          - /api/v1/questions
        strip_path: false
    plugins:
      - name: rate-limiting
        config:
          minute: 100
          policy: redis
      - name: jwt
        config:
          claims_to_verify:
            - exp
  
  # 练习服务
  - name: practice-service
    url: http://practice-service.empenglish.svc.cluster.local:8003
    routes:
      - name: practice-routes
        paths:
          - /api/v1/practice
        strip_path: false
    plugins:
      - name: rate-limiting
        config:
          minute: 20
          policy: redis
      - name: jwt
        config:
          claims_to_verify:
            - exp
  
  # ASR服务
  - name: asr-service
    url: http://asr-service.empenglish.svc.cluster.local:9001
    routes:
      - name: asr-routes
        paths:
          - /api/v1/ai/asr
        strip_path: false
    plugins:
      - name: rate-limiting
        config:
          minute: 10
          policy: redis
      - name: jwt
        config:
          claims_to_verify:
            - exp
```

---

## 十、测试策略

### 10.1 单元测试

```python
import pytest
from services.scoring_service import ScoringService

class TestScoringService:
    """评分服务测试"""
    
    @pytest.fixture
    def scoring_service(self):
        return ScoringService()
    
    def test_evaluate_pronunciation(self, scoring_service):
        """测试发音评分"""
        result = scoring_service.evaluate_pronunciation(
            audio_url="test_audio.mp3",
            text="Hello, my name is John."
        )
        
        assert "overall_score" in result
        assert 0 <= result["overall_score"] <= 100
        assert "phoneme_scores" in result
    
    def test_evaluate_fluency(self, scoring_service):
        """测试流利度评分"""
        result = scoring_service.evaluate_fluency(
            audio_url="test_audio.mp3",
            text="Hello, my name is John. I am a student."
        )
        
        assert "overall_score" in result
        assert "speech_rate" in result
        assert "pause_frequency" in result
    
    def test_evaluate_vocabulary(self, scoring_service):
        """测试词汇评分"""
        result = scoring_service.evaluate_vocabulary(
            text="I have extensive experience in machine learning and deep learning."
        )
        
        assert "overall_score" in result
        assert "diversity" in result
        assert "advanced_words" in result
```

### 10.2 集成测试

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

class TestPracticeFlow:
    """练习流程集成测试"""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    @pytest.fixture
    def auth_token(self, client):
        """获取认证令牌"""
        response = client.post(
            "/api/v1/auth/wechat/login",
            json={"code": "test_code"}
        )
        return response.json()["data"]["access_token"]
    
    def test_create_session(self, client, auth_token):
        """测试创建会话"""
        response = client.post(
            "/api/v1/practice/sessions",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "mode": "general",
                "pressure_level": 2,
                "max_questions": 5
            }
        )
        
        assert response.status_code == 200
        data = response.json()["data"]
        assert "session_id" in data
        assert "first_question" in data
    
    def test_submit_answer(self, client, auth_token):
        """测试提交答案"""
        # 先创建会话
        session_response = client.post(
            "/api/v1/practice/sessions",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "mode": "general",
                "pressure_level": 2,
                "max_questions": 5
            }
        )
        session_id = session_response.json()["data"]["session_id"]
        
        # 提交答案
        response = client.post(
            f"/api/v1/practice/sessions/{session_id}/answer",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "turn_id": "test_turn_id",
                "audio_url": "test_audio.mp3",
                "duration": 15
            }
        )
        
        assert response.status_code == 200
        data = response.json()["data"]
        assert "score" in data
```

### 10.3 性能测试

```python
import pytest
import asyncio
from locust import HttpUser, task, between

class EmpEnglishUser(HttpUser):
    """性能测试用户"""
    
    wait_time = between(1, 3)
    
    def on_start(self):
        """开始时的操作"""
        # 登录
        response = self.client.post(
            "/api/v1/auth/wechat/login",
            json={"code": "test_code"}
        )
        self.token = response.json()["data"]["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def create_session(self):
        """创建会话"""
        self.client.post(
            "/api/v1/practice/sessions",
            headers=self.headers,
            json={
                "mode": "general",
                "pressure_level": 2,
                "max_questions": 5
            }
        )
    
    @task(2)
    def get_questions(self):
        """获取题目"""
        self.client.get(
            "/api/v1/questions",
            headers=self.headers,
            params={"type": "general", "page": 1, "page_size": 10}
        )
    
    @task(1)
    def get_reports(self):
        """获取报告"""
        self.client.get(
            "/api/v1/reports",
            headers=self.headers
        )
```

---

## 十一、附录

### 11.1 错误码列表

| 错误码 | 说明 | HTTP状态码 |
|--------|------|-----------|
| 0 | 成功 | 200 |
| 40001 | 参数错误 | 400 |
| 40002 | 参数缺失 | 400 |
| 40003 | 参数格式错误 | 400 |
| 40101 | 未登录 | 401 |
| 40102 | Token过期 | 401 |
| 40103 | Token无效 | 401 |
| 40301 | 无权限 | 403 |
| 40302 | 订阅已过期 | 403 |
| 40303 | 超出免费额度 | 403 |
| 40401 | 资源不存在 | 404 |
| 40402 | 用户不存在 | 404 |
| 40403 | 题目不存在 | 404 |
| 40404 | 会话不存在 | 404 |
| 40901 | 资源冲突 | 409 |
| 40902 | 用户已存在 | 409 |
| 42901 | 请求过多 | 429 |
| 50001 | 服务器错误 | 500 |
| 50002 | 服务不可用 | 503 |
| 50003 | ASR服务异常 | 500 |
| 50004 | LLM服务异常 | 500 |
| 50005 | TTS服务异常 | 500 |

### 11.2 配置文件示例

#### 11.2.1 应用配置（config.yaml）

```yaml
app:
  name: empenglish
  version: "1.0.0"
  debug: false
  host: "0.0.0.0"
  port: 8001

database:
  url: "mysql://user:password@localhost:3306/empenglish"
  pool_size: 10
  max_overflow: 20
  pool_timeout: 30
  pool_recycle: 3600

redis:
  url: "redis://localhost:6379/0"
  pool_size: 10
  decode_responses: true

mongodb:
  url: "mongodb://localhost:27017"
  database: empenglish

rabbitmq:
  url: "amqp://guest:guest@localhost:5672//"
  queue_prefix: empenglish

jwt:
  secret_key: "your-secret-key"
  algorithm: "HS256"
  access_token_expire_hours: 2
  refresh_token_expire_days: 7

minio:
  endpoint: "localhost:9000"
  access_key: "your-access-key"
  secret_key: "your-secret-key"
  bucket_name: empenglish
  secure: false

milvus:
  host: "localhost"
  port: 19530
  collection_prefix: empenglish

llm:
  provider: "qwen"
  model: "qwen2.5-7b"
  api_key: "your-api-key"
  base_url: "https://api.qwen.com"
  temperature: 0.7
  max_tokens: 1000

asr:
  model: "whisper-base"
  device: "cuda"
  language: "en"

tts:
  provider: "edge-tts"
  default_voice: "female_us"

scoring:
  pronunciation_weight: 0.25
  fluency_weight: 0.25
  vocabulary_weight: 0.25
  grammar_weight: 0.25
  university_match_weight: 0.0

rate_limit:
  default: "100/minute"
  auth: "10/minute"
  practice: "20/minute"
  upload: "5/minute"

logging:
  level: "INFO"
  format: "json"
  file: "logs/app.log"
  max_size: "100MB"
  backup_count: 10
```

### 11.3 数据库迁移脚本

```python
# Alembic迁移脚本示例
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    """升级数据库"""
    op.create_table(
        'users',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('openid', sa.String(128), unique=True, nullable=False),
        sa.Column('unionid', sa.String(128), unique=True),
        sa.Column('nickname', sa.String(100)),
        sa.Column('avatar_url', sa.String(500)),
        sa.Column('phone', sa.String(20)),
        sa.Column('email', sa.String(100)),
        sa.Column('target_university', sa.String(100)),
        sa.Column('target_college', sa.String(100)),
        sa.Column('target_major', sa.String(100)),
        sa.Column('subscription_type', mysql.ENUM('free', 'trial', 'premium_15d', 'premium_30d', 'annual'), default='free'),
        sa.Column('subscription_expiry', sa.DateTime),
        sa.Column('total_practice_count', sa.Integer, default=0),
        sa.Column('last_practice_time', sa.DateTime),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.Column('deleted_at', sa.TIMESTAMP),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci'
    )
    
    op.create_index('idx_openid', 'users', ['openid'])
    op.create_index('idx_unionid', 'users', ['unionid'])
    op.create_index('idx_subscription', 'users', ['subscription_type', 'subscription_expiry'])
    op.create_index('idx_target', 'users', ['target_university', 'target_major'])

def downgrade():
    """回滚数据库"""
    op.drop_table('users')
```

---

## 文档结束

本低层设计文档（LLD）详细定义了 empEnglish 项目的：

1. **数据库设计**：MySQL、MongoDB、Redis、Milvus 的详细表结构和索引
2. **API接口设计**：所有服务接口的详细规范
3. **核心算法设计**：ASR、TTS、评分算法的详细实现
4. **Agent编排设计**：基于 LangGraph 的工作流定义
5. **消息队列设计**：RabbitMQ 队列和 Celery 任务定义
6. **安全设计**：认证授权、数据加密、接口限流、音频安全
7. **监控与日志**：Prometheus 指标、日志格式、告警规则
8. **部署配置**：Docker、Kubernetes、Kong 配置
9. **测试策略**：单元测试、集成测试、性能测试
10. **附录**：错误码、配置文件、迁移脚本

本文档为开发团队提供了详细的实现指导，确保项目能够按照 PRD 和 HLD 的要求顺利实施。