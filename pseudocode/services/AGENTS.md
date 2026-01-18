# pseudocode/services/ Knowledge Base

**Generated:** 2026-01-17
**Status:** Design/Documentation Phase (Pseudocode Only)

## OVERVIEW

Business logic layer orchestrating user management, question handling, practice sessions, and multi-dimensional scoring.

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| User authentication | user_service.py | WeChat login (mock), JWT token management, subscription validation |
| Permission checks | user_service.py:157-212 | UserPermissionChecker: mode-specific access control, daily limits |
| Question management | question_service.py | CRUD, recommendations, university/major matching |
| Category flow | question_service.py:193-229 | QuestionCategoryManager: sequential progression through 8 categories |
| Session orchestration | practice_service.py | Create, submit answers, manage turns, coordinate AI services |
| Real-time interaction | practice_service.py:318-383 | WebSocketPracticeHandler: answer/next_question/abort message handling |
| Multi-dimensional scoring | scoring_service.py | Pronunciation, fluency, vocabulary, grammar, university match |

## CONVENTIONS

**Service Pattern:** XxxService classes with dependency injection in `__init__` (e.g., PracticeService injects QuestionService, ScoringService, ASRService, TTSService, LLMService).

**Repository Pattern:** All data access via XxxRepository classes from models layer.

**Helper Classes:** Permission checkers (UserPermissionChecker), managers (QuestionCategoryManager), configs (ScoringConfig) separate from main services.

**Mock Implementations:** WeChat API returns mock data (user_service.py:150-154), references non-existent modules (algorithms/, report_service).

**Scoring Weights:** Default 25% each for pronunciation, fluency, vocabulary, grammar; university match adds 20% (rebalances to 20% each) when enabled.

**Feedback Thresholds:** ScoringConfig defines 4 levels (excellent≥90, good≥80, fair≥70, poor<60) across all dimensions.
