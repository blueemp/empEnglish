"""
Tests for Rate Limiter (TDD approach).
"""

import pytest
from datetime import datetime, timedelta


class TestRateLimiter:
    """Test cases for RateLimiter class."""

    def test_init_without_redis(self):
        """Test initialization without Redis client (local storage)."""
        from pseudocode.utils.rate_limiter import RateLimiter

        limiter = RateLimiter(redis_client=None)

        assert limiter.redis_client is None
        assert limiter.local_store is not None

    def test_init_with_redis(self):
        """Test initialization with Redis client."""
        from pseudocode.utils.rate_limiter import RateLimiter

        mock_redis = MagicMock()
        limiter = RateLimiter(redis_client=mock_redis)

        assert limiter.redis_client is mock_redis

    def test_is_allowed_first_request(self, mock_rate_limiter):
        """Test first request should be allowed."""
        result = mock_rate_limiter.is_allowed(key="user:123", limit=10, window=60)

        assert result["allowed"] is True
        assert result["remaining"] == 9

    def test_is_allowed_within_limit(self, mock_rate_limiter):
        """Test requests within limit should be allowed."""
        for _ in range(5):
            mock_rate_limiter.is_allowed(key="user:456", limit=10, window=60)

        result = mock_rate_limiter.is_allowed(key="user:456", limit=10, window=60)

        assert result["allowed"] is True
        assert result["remaining"] == 4

    def test_is_allowed_exceeds_limit(self, mock_rate_limiter):
        """Test requests exceeding limit should be blocked."""
        for _ in range(10):
            mock_rate_limiter.is_allowed(key="user:789", limit=5, window=60)

        result = mock_rate_limiter.is_allowed(key="user:789", limit=5, window=60)

        assert result["allowed"] is False
        assert result["remaining"] == 0
        assert result["retry_after"] > 0

    def test_is_allowed_resets_after_window(self, mock_rate_limiter):
        """Test limit should reset after window expires."""
        from unittest.mock import patch

        limiter = mock_rate_limiter

        mock_time = datetime.utcnow() - timedelta(seconds=65)

        with patch("pseudocode.utils.rate_limiter.datetime") as mock_datetime:
            mock_datetime.utcnow.return_value = mock_time
            limiter.is_allowed(key="user:111", limit=5, window=60)

        # After window reset, new request should be allowed
        result = limiter.is_allowed(key="user:111", limit=5, window=60)

        assert result["allowed"] is True

    def test_reset_key(self, mock_rate_limiter):
        """Test manual reset of rate limit for a key."""
        mock_rate_limiter.is_allowed(key="user:reset", limit=5, window=60)
        mock_rate_limiter.is_allowed(key="user:reset", limit=5, window=60)

        result = mock_rate_limiter.is_allowed(key="user:reset", limit=5, window=60)

        assert result["allowed"] is False

        mock_rate_limiter.reset_key(key="user:reset")

        result = mock_rate_limiter.is_allowed(key="user:reset", limit=5, window=60)

        assert result["allowed"] is True

    def test_get_usage(self, mock_rate_limiter):
        """Test getting usage statistics."""
        for _ in range(3):
            mock_rate_limiter.is_allowed(key="user:stats", limit=10, window=60)

        usage = mock_rate_limiter.get_usage(key="user:stats")

        assert usage["count"] == 3
        assert usage["limit"] == 10
        assert usage["remaining"] == 7


class TestTokenBucketRateLimiter:
    """Test cases for TokenBucketRateLimiter class."""

    def test_init(self):
        """Test initialization."""
        from pseudocode.utils.rate_limiter import TokenBucketRateLimiter

        limiter = TokenBucketRateLimiter(capacity=10, refill_rate=1, refill_interval=1)

        assert limiter.capacity == 10
        assert limiter.refill_rate == 1
        assert limiter.tokens == 10

    def test_consume_within_capacity(self):
        """Test consuming tokens within capacity."""
        from pseudocode.utils.rate_limiter import TokenBucketRateLimiter

        limiter = TokenBucketRateLimiter(capacity=10, refill_rate=1, refill_interval=1)

        result = limiter.consume(tokens=3)

        assert result["allowed"] is True
        assert limiter.tokens == 7

    def test_consume_exceeds_capacity(self):
        """Test consuming more tokens than available."""
        from pseudocode.utils.rate_limiter import TokenBucketRateLimiter

        limiter = TokenBucketRateLimiter(capacity=10, refill_rate=1, refill_interval=1)

        result = limiter.consume(tokens=15)

        assert result["allowed"] is False
        assert limiter.tokens == 10
        assert result["wait_time"] > 0

    def test_refill_over_time(self):
        """Test tokens refill over time."""
        from pseudocode.utils.rate_limiter import TokenBucketRateLimiter
        from unittest.mock import patch

        mock_time = datetime.utcnow()

        limiter = TokenBucketRateLimiter(capacity=10, refill_rate=5, refill_interval=10)

        initial_tokens = limiter.tokens

        with patch("pseudocode.utils.rate_limiter.datetime") as mock_datetime:
            mock_datetime.utcnow.return_value = mock_time + timedelta(seconds=10)
            result = limiter.consume(tokens=12)

        # After 10 seconds, should have 5 more tokens
        expected_tokens = initial_tokens + 5
        assert limiter.tokens == expected_tokens


class TestRateLimiterConfig:
    """Test cases for RateLimiterConfig class."""

    def test_default_config(self):
        """Test default rate limiting configuration."""
        from pseudocode.utils.rate_limiter import RateLimiterConfig

        config = RateLimiterConfig()

        assert config.general_api_limit == 100
        assert config.create_session_limit == 10
        assert config.submit_answer_limit == 20
        assert config.get_report_limit == 60

    def test_custom_config(self):
        """Test custom rate limiting configuration."""
        from pseudocode.utils.rate_limiter import RateLimiterConfig

        config = RateLimiterConfig(
            general_api_limit=50,
            create_session_limit=5,
            submit_answer_limit=10,
            get_report_limit=30,
        )

        assert config.general_api_limit == 50
        assert config.create_session_limit == 5
        assert config.submit_answer_limit == 10
        assert config.get_report_limit == 30

    def test_get_limit_by_endpoint(self):
        """Test getting limit by endpoint."""
        from pseudocode.utils.rate_limiter import RateLimiterConfig

        config = RateLimiterConfig()

        assert config.get_limit("/api/v1/session/create") == 10
        assert config.get_limit("/api/v1/session/submit") == 20
        assert config.get_limit("/api/v1/report") == 60
        assert config.get_limit("/api/v1/unknown") == 100
