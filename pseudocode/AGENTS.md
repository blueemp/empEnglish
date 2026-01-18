# pseudocode/ Domain Documentation

**Generated:** 2026-01-17
**Status:** Reference Implementation (Pseudocode Only)

## OVERVIEW
Complete reference implementation with 75+ classes across 17 Python files (4,860 lines), all marked as pseudocode for structural reference only.

## STRUCTURE
```
pseudocode/
├── models/          # 5 SQLAlchemy models + Pydantic DTOs (1,620 lines)
├── services/        # 4 business logic services (1,440 lines)
├── ai/              # 4 AI service wrappers (1,180 lines)
├── utils/           # 4 utility classes (620 lines)
└── api/             # EMPTY - routes not yet defined
```

## WHERE TO LOOK

| File | Purpose | Key Classes |
|------|---------|-------------|
| models/user.py | User accounts, subscriptions | User, UserRepository, DTOs |
| models/question.py | Question bank, categories | Question, QuestionRepository |
| models/practice.py | Session orchestration | PracticeSession, Turn, SessionRepository |
| models/scoring.py | Multi-dimensional scores | ScoringRecord, ScoreRepository |
| models/tutor_style.py | AI personality config | TutorStyle, StyleRepository |
| services/user_service.py | User management, auth | UserService, AuthService |
| services/question_service.py | Question retrieval | QuestionService |
| services/practice_service.py | Session flow, WebSocket | PracticeService, WebSocketManager |
| services/scoring_service.py | Score calculation | ScoringService (references missing algorithms) |
| ai/asr_service.py | Speech recognition (Whisper) | ASRService |
| ai/tts_service.py | Speech synthesis (Edge-TTS/VITS) | TTSService |
| ai/llm_service.py | LLM integration (Qwen/DeepSeek) | LLMService |
| ai/agent_service.py | LangGraph orchestration | InterviewAgent |
| utils/jwt_manager.py | Token generation/validation | JWTManager |
| utils/encryption_manager.py | Password hashing stub | EncryptionManager |
| utils/rate_limiter.py | Rate limiting (Redis stub) | RateLimiter |
| utils/logger.py | Structured logging | EMPLogger |

## CONVENTIONS

**Repository Pattern:** Each model has `XxxRepository` class for data access with CRUD methods.

**Service Layer:** Business logic encapsulated in `XxxService` classes using repositories.

**DTO Pattern:** Separate Pydantic models for input (`XxxCreate`, `XxxUpdate`) and output (`XxxResponse`).

**Pseudocode Markers:** All files start with `# Xxx服务伪代码` comments. Repository methods contain `pass` statements.

**Mock Data:** Uses placeholders like `"mock_openid"`, `"temp_audio.wav"`, mock MinIO URLs.

## ANTI-PATTERNS (THIS IS REFERENCE CODE, NOT PRODUCTION)

**CRITICAL:** All files are pseudocode for structural reference only - DO NOT deploy without implementing:

- Database operations (all repository methods contain only `pass` statements)
- Password hashing (`EncryptionManager` returns `"hashed_password"` stub)
- Rate limiting (uses `None` for Redis client, no actual storage)
- Audio processing (references `temp_audio.wav`, no actual file I/O)
- AI algorithms (`gop_scorer.py`, `fluency_scorer.py` referenced but don't exist)
- Report generation (`report_service.py` referenced but doesn't exist)
- API routes (`api/` directory is empty)

**Missing Components:** `requirements.txt`, entry points (`main.py`, `app.py`), Docker configs, migrations, tests.
