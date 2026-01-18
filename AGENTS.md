# empEnglish Project Knowledge Base

**Generated:** 2026-01-17
**Status:** Design/Documentation Phase (Pseudocode Only)

## OVERVIEW

AI-powered English oral practice platform for Chinese graduate school entrance exams. Target: Xi'an universities. All Python files are **pseudocode only** - no production code.

## STRUCTURE

```
empEnglish/
├── PRD.md              # Product Requirements (384 lines)
├── HLD.md              # High-Level Design (1,542 lines)
├── LLD.md              # Low-Level Design (3,900+ lines)
└── pseudocode/         # Reference implementation (4,860 lines)
    ├── models/          # SQLAlchemy + Pydantic models
    ├── services/        # Business logic layer
    ├── ai/              # AI services (ASR/TTS/LLM/Agent)
    ├── utils/           # JWT, encryption, rate limiting, logging
    └── api/            # EMPTY - routes not yet defined
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Product requirements | PRD.md | Target users, features, business goals |
| Architecture | HLD.md | System design, tech stack, microservices |
| API specs | LLD.md | Detailed interface definitions |
| Data models | pseudocode/models/ | User, Question, Practice, Scoring, TutorStyle |
| Business logic | pseudocode/services/ | User, Question, Practice, Scoring services |
| AI integration | pseudocode/ai/ | ASR (Whisper), TTS (Edge-TTS/VITS), LLM (Qwen/DeepSeek), Agent (LangGraph) |
| Utilities | pseudocode/utils/ | JWT, encryption, rate limiting, logging |

## CODE MAP

Total: 75+ classes across 17 Python files (pseudocode only).

| Symbol | Type | Location | Role |
|--------|------|----------|------|
| User | Model | pseudocode/models/user.py | User accounts, subscriptions, targets |
| Question | Model | pseudocode/models/question.py | Question bank, categories, difficulty |
| PracticeSession | Model | pseudocode/models/practice.py | Interview sessions, turns |
| ScoringRecord | Model | pseudocode/models/scoring.py | Multi-dimensional scores |
| InterviewAgent | Class | pseudocode/ai/agent_service.py | LangGraph orchestration |
| ASRService | Class | pseudocode/ai/asr_service.py | Whisper speech recognition |
| TTSService | Class | pseudocode/ai/tts_service.py | Edge-TTS/VITS synthesis |
| LLMService | Class | pseudocode/ai/llm_service.py | Qwen/DeepSeek integration |
| PracticeService | Class | pseudocode/services/practice_service.py | Session orchestration, WebSocket |
| ScoringService | Class | pseudocode/services/scoring_service.py | GOP, fluency, vocabulary, grammar scoring |

## CONVENTIONS

**Repository Pattern:** Each model has `XxxRepository` for data access.

**Service Layer:** Business logic in `XxxService` classes.

**DTO Pattern:** Separate Pydantic models (`XxxCreate`, `XxxUpdate`, `XxxResponse`).

**Pseudocode Format:** All Python files contain `# 伪代码` comments indicating placeholder implementations.

**All Database Operations Stubbed:** Repository methods contain only `pass` statements.

**Language:** English-only (ASR default `language="en"`), but with Chinese-accent optimized model mentioned.

## ANTI-PATTERNS (THIS PROJECT)

**CRITICAL:** This is a pseudocode/reference implementation, NOT production code.

- **Do NOT** use `decode_token_without_verification()` in production (`jwt_manager.py:172`)
- **Do NOT** deploy without implementing password hashing (currently returns `"hashed_password"` stub)
- **Do NOT** use mock data (`mock_openid`, `temp_audio.wav`, mock MinIO URLs)
- **Do NOT** use `pass` statement implementations in production

**Missing Components:**
- `requirements.txt`, `pyproject.toml`, Dockerfile, docker-compose.yml
- API routes (`pseudocode/api/` is empty)
- Algorithms directory (`gop_scorer.py`, `fluency_scorer.py` referenced but not implemented)
- Tests, migrations, entry points (`main.py`, `app.py`)

## UNIQUE STYLES

**Subscription Types:** FREE, TRIAL, PREMIUM_15D, PREMIUM_30D, ANNUAL.

**Practice Modes:** GENERAL (free), UNIVERSITY (premium), PRESSURE (premium, 3 levels).

**Scoring Dimensions (5):** Pronunciation (25%), Fluency (25%), Vocabulary (25%), Grammar (25%), University Match (20% in uni mode).

**Agent Workflow (LangGraph):** generate_question → transcribe → score → generate_feedback → synthesize → follow_up → check_completion → generate_report.

## COMMANDS

```bash
# No actual build commands exist (design phase only)
# Manual pip install commands in pseudocode/README.md lines 257-260:
pip install fastapi uvicorn sqlalchemy pydantic
pip install langchain langgraph
pip install faster-whisper edge-tts
pip install cryptography
```

## NOTES

**Tech Stack:** FastAPI, SQLAlchemy, Pydantic, LangChain/LangGraph, Whisper/Faster-Whisper, Edge-TTS/VITS, Qwen/DeepSeek.

**Databases:** MySQL (relational), MongoDB (unstructured), Redis (cache), Milvus (vectors).

**Deployment:** Docker + Kubernetes (configs documented in LLD.md lines 3295-3568).

**API Gateway:** Kong with rate limiting (documented in LLD.md lines 3488-3568).

**Rate Limits:** General API 100/min, Create session 10/hour, Submit answer 20/min, Get report 60/hour.

**Security Concerns:** JWT decode without verification (debug only), no password hashing, mock API responses.

**Next Steps:** Implement all stubbed database operations, add missing components (API routes, algorithms), create build/deploy configs, add tests.
