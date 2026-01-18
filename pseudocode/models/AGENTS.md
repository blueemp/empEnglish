# empEnglish Models Layer

**Generated:** 2026-01-17
**Parent:** ../AGENTS.md

## OVERVIEW

SQLAlchemy ORM models with Pydantic DTOs defining the complete data schema for users, questions, practice sessions, and AI scoring.

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| User accounts, subscriptions | user.py | Subscription types (FREE/TRIAL/PREMIUM/ANNUAL), targets |
| Question bank management | question.py | Types (GENERAL/UNIVERSITY/MAJOR), difficulty 1-5, 8 categories |
| Interview sessions, turns | practice.py | Session modes (GENERAL/UNIVERSITY), pressure levels 1-3 |
| Multi-dimensional scoring | scoring.py | 5 dimensions (pronunciation/fluency/vocabulary/grammar/uni_match) |
| AI tutor personalities | tutor_style.py | 4 types (ACADEMIC_DEEP/PRACTICE_ORIENTED/FRIENDLY/HIGH_PRESSURE) |

## CONVENTIONS

**File Structure:** Enums (module-level) → SQLAlchemy Model → Pydantic DTOs → Repository class.

**Enum Definitions:** All enums use `str` or `int` base (e.g., `SubscriptionType(str, Enum)`).

**Model Fields:** `id` = UUID string (64 chars), timestamps use `datetime.utcnow()`, soft delete via `deleted_at` column.

**JSON Columns:** Flexible storage for `details`, `suggestions`, `examples`, `tags`.

**Decimal Precision:** Scores use `DECIMAL(5, 2)` (max 999.99).

**Relationships:** SQLAlchemy `relationship()` with `back_populates`, foreign keys as string references.

**Repository Methods:** All stubbed with `pass`, signatures follow CRUD pattern (create, get_by_id, update, delete, list).

## CODE MAP

| Symbol | File | Lines | DTOs | Repository Methods |
|--------|------|-------|------|--------------------|
| User | user.py | 184 | Create, Update, Response | 6 methods |
| Question | question.py | 158 | Create, Response | 6 methods |
| PracticeSession, PracticeTurn | practice.py | 247 | SessionCreate, SessionResponse, TurnResponse | 10 methods |
| ScoringRecord, PhonemeError | scoring.py | 174 | (none) | 8 methods |
| TutorStyle | tutor_style.py | 154 | Response | 5 methods |

Total: 8 models, 35 DTOs, 35 repository methods.
