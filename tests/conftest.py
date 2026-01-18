"""
Shared test configuration and fixtures for empEnglish test suite.
"""

import pytest
import os
from typing import Generator
from unittest.mock import MagicMock
import tempfile
import shutil


@pytest.fixture(scope="session")
def test_config():
    """Test configuration dictionary."""
    return {
        "app": {"name": "empenglish-test", "version": "1.0.0", "debug": True},
        "jwt": {
            "secret_key": "test-secret-key-for-jwt-token-generation-only",
            "algorithm": "HS256",
            "access_token_expire_hours": 2,
            "refresh_token_expire_days": 7,
        },
        "encryption": {"secret_key": "test-encryption-key-32-bytes-long"},
        "database": {"url": "sqlite:///test.db"},
        "redis": {"url": "redis://localhost:6379/1", "enabled": False},
        "llm": {
            "provider": "mock",
            "model": "test-model",
            "api_key": "test-api-key",
            "temperature": 0.7,
            "max_tokens": 1000,
        },
    }


@pytest.fixture(scope="session")
def temp_dir() -> Generator[str, None, None]:
    """Temporary directory for test files."""
    temp_path = tempfile.mkdtemp(prefix="empenglish_test_")
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture(scope="function")
def mock_jwt_manager(test_config):
    """Mock JWT manager for testing."""
    from pseudocode.utils.jwt_manager import JWTManager

    return JWTManager(
        secret_key=test_config["jwt"]["secret_key"],
        algorithm=test_config["jwt"]["algorithm"],
    )


@pytest.fixture(scope="function")
def sample_user_data():
    """Sample user data for testing."""
    return {
        "openid": "test_openid_123",
        "unionid": "test_unionid_456",
        "nickname": "Test User",
        "avatar": "https://example.com/avatar.jpg",
        "phone": "13800138000",
        "email": "test@example.com",
        "subscription_type": "FREE",
        "target_university": "Xi'an Jiaotong University",
        "target_major": "Computer Science",
    }


@pytest.fixture(scope="function")
def auth_token(mock_jwt_manager):
    """Generate a valid auth token for testing."""
    token = mock_jwt_manager.generate_access_token(
        user_id="test_user_id", payload={"nickname": "Test User"}
    )
    return token
