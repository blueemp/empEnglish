# empEnglish Utils Knowledge Base

**Generated:** 2026-01-17
**Status:** Design/Documentation Phase (Pseudocode Only)

## OVERVIEW

Cross-cutting utilities: JWT authentication, AES encryption, rate limiting, and structured logging.

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| JWT tokens | jwt_manager.py | Access/refresh tokens, expiration checks |
| Data encryption | encryption_manager.py | AES-256, data masking, password hashing |
| Rate limiting | rate_limiter.py | Sliding window, token bucket, Redis support |
| Logging | logger.py | JSON formatter, request context, middleware |

## CONVENTIONS

**Singleton Logger:** `Logger` class uses `__new__` pattern for single instance per name.

**Redis-Optional Rate Limiting:** Both `RateLimiter` and `TokenBucketRateLimiter` fall back to local storage if Redis unavailable.

**Data Masking Pattern:** `DataMasker` has static methods, `EncryptionManager` combines masking + encryption.

**Context-Aware Logging:** `RequestContext` tracks `user_id`, `request_id`, `session_id`, `trace_id` across requests.

## ANTI-PATTERNS (SECURITY)

**CRITICAL:** All security utilities are pseudocode/stubbed - DO NOT deploy.

- **Do NOT** use `decode_token_without_verification()` (`jwt_manager.py:172`) - bypasses signature verification (debug only)
- **Do NOT** deploy with stubbed password hashing (`encryption_manager.py:142`) - returns `"hashed_password"` literal
- **Do NOT** use mock encryption keys or salt in production
- **PasswordHasher.verify_password()** always returns `True` (line 156) - no actual verification
