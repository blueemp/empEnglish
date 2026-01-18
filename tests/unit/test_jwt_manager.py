"""
Tests for JWT Manager (TDD approach).
First, write failing tests, then implement code to pass them.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock
import jwt


class TestJWTManager:
    """Test cases for JWTManager class."""

    def test_init_with_default_algorithm(self, test_config):
        """Test JWT manager initialization with default algorithm."""
        from pseudocode.utils.jwt_manager import JWTManager

        manager = JWTManager(
            secret_key=test_config["jwt"]["secret_key"],
            algorithm=test_config["jwt"]["algorithm"],
        )

        assert manager.secret_key == test_config["jwt"]["secret_key"]
        assert manager.algorithm == "HS256"

    def test_generate_access_token(self, test_config):
        """Test access token generation."""
        from pseudocode.utils.jwt_manager import JWTManager

        manager = JWTManager(
            secret_key=test_config["jwt"]["secret_key"],
            algorithm=test_config["jwt"]["algorithm"],
        )

        token = manager.generate_access_token(
            user_id="test_user_123", payload={"nickname": "Test User"}
        )

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_access_token_valid(self, test_config):
        """Test decoding valid access token."""
        from pseudocode.utils.jwt_manager import JWTManager

        manager = JWTManager(
            secret_key=test_config["jwt"]["secret_key"],
            algorithm=test_config["jwt"]["algorithm"],
        )

        token = manager.generate_access_token(
            user_id="test_user_123", payload={"nickname": "Test User"}
        )

        decoded = manager.decode_token(token)

        assert decoded is not None
        assert decoded["user_id"] == "test_user_123"
        assert decoded["nickname"] == "Test User"
        assert decoded["type"] == "access"

    def test_decode_token_invalid_signature(self, test_config):
        """Test decoding token with invalid signature."""
        from pseudocode.utils.jwt_manager import JWTManager

        manager = JWTManager(
            secret_key=test_config["jwt"]["secret_key"],
            algorithm=test_config["jwt"]["algorithm"],
        )

        manager_wrong = JWTManager(secret_key="wrong-secret-key", algorithm="HS256")

        token = manager.generate_access_token(user_id="test_user_123", payload={})

        with pytest.raises(jwt.InvalidTokenError):
            manager_wrong.decode_token(token)

    def test_decode_token_expired(self, test_config):
        """Test decoding expired token."""
        from pseudocode.utils.jwt_manager import JWTManager

        manager = JWTManager(
            secret_key=test_config["jwt"]["secret_key"],
            algorithm=test_config["jwt"]["algorithm"],
        )

        # Manually create expired token
        payload = {
            "user_id": "test_user_123",
            "type": "access",
            "exp": datetime.utcnow() - timedelta(hours=1),
        }
        token = jwt.encode(payload, test_config["jwt"]["secret_key"], algorithm="HS256")

        with pytest.raises(jwt.ExpiredSignatureError):
            manager.decode_token(token)

    def test_verify_token_valid(self, test_config):
        """Test token verification with valid token."""
        from pseudocode.utils.jwt_manager import JWTManager

        manager = JWTManager(
            secret_key=test_config["jwt"]["secret_key"],
            algorithm=test_config["jwt"]["algorithm"],
        )

        token = manager.generate_access_token(user_id="test_user_123", payload={})

        result = manager.verify_token(token)

        assert result["valid"] is True
        assert result["user_id"] == "test_user_123"
        assert result["type"] == "access"

    def test_verify_token_invalid(self, test_config):
        """Test token verification with invalid token."""
        from pseudocode.utils.jwt_manager import JWTManager

        manager = JWTManager(
            secret_key=test_config["jwt"]["secret_key"],
            algorithm=test_config["jwt"]["algorithm"],
        )

        result = manager.verify_token("invalid.token.here")

        assert result["valid"] is False
        assert "error" in result

    def test_generate_refresh_token(self, test_config):
        """Test refresh token generation."""
        from pseudocode.utils.jwt_manager import JWTManager

        manager = JWTManager(
            secret_key=test_config["jwt"]["secret_key"],
            algorithm=test_config["jwt"]["algorithm"],
        )

        token = manager.generate_refresh_token(user_id="test_user_123")

        assert token is not None
        assert isinstance(token, str)

        decoded = manager.decode_token(token)
        assert decoded["type"] == "refresh"

    def test_refresh_token_expires_in_days(self, test_config):
        """Test refresh token expires in correct time."""
        from pseudocode.utils.jwt_manager import JWTManager

        manager = JWTManager(
            secret_key=test_config["jwt"]["secret_key"],
            algorithm=test_config["jwt"]["algorithm"],
        )

        token = manager.generate_refresh_token(user_id="test_user_123")
        decoded = manager.decode_token(token)

        expected_expiry = datetime.utcnow() + timedelta(days=7)
        actual_expiry = datetime.fromtimestamp(decoded["exp"])

        # Allow 1 second difference
        assert abs((expected_expiry - actual_expiry).total_seconds()) < 2
