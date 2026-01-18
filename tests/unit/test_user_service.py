"""
Tests for User Service (TDD approach).
"""
import pytest


class TestUserService:
    """Test cases for UserService class."""

    def test_init(self, mock_encryption_manager, mock_jwt_manager):
        """Test service initialization."""
        from pseudocode.services.user_service import UserService

        service = UserService(
            encryption_manager=mock_encryption_manager,
            jwt_manager=mock_jwt_manager
        )

        assert service.encryption_manager is not None
        assert service.jwt_manager is not None

    def test_wechat_login_new_user(self, mock_user_repository, mock_encryption_manager, mock_jwt_manager):
        """Test WeChat login for new user."""
        from pseudocode.services.user_service import UserService

        mock_encryption_manager.hash_password.return_value = "hashed_password_123"
        mock_jwt_manager.generate_access_token.return_value = "test_token_existing"
        mock_user_repository.get_by_openid.return_value = None

        service = UserService(
            encryption_manager=mock_encryption_manager,
            jwt_manager=mock_jwt_manager
        )

        user_data = {
            "openid": "new_openid_456",
            "unionid": "new_unionid_789",
            "nickname": "Test User",
            "avatar_url": "http://example.com/avatar.jpg",
            "phone": "13800138000",
            "email": "test@example.com",
            "subscription_type": "TRIAL"
            "target_university": None,
            "target_major": None
        }

        result = service.wechat_login_new_user(**user_data)

        assert result["user_id"] is not None
        assert result["openid"] == "new_openid_456"
        assert result["unionid"] == "new_unionid_789"

    def test_wechat_login_existing_user(self, mock_user_repository, mock_encryption_manager, mock_jwt_manager):
        """Test WeChat login for existing user."""
        from pseudocode.services.user_service import UserService

        mock_user_repository.get_by_openid.return_value = MagicMock(id="user_123", openid="existing_openid_123", subscription_type="FREE")
        mock_jwt_manager.generate_access_token.return_value = "test_token_existing"
        mock_jwt_manager.verify_token.return_value = {"valid": True, "user_id": "user_123"}

        service = UserService(
            encryption_manager=mock_encryption_manager,
            jwt_manager=mock_jwt_manager
        )

        result = service.wechat_login_existing_user(openid="existing_openid_123")

        assert result["user_id"] == "user_123"
        assert result["access_token"] == "test_token_existing"

    def test_get_user_profile(self, mock_user_repository, mock_jwt_manager):
        """Test getting user profile."""
        from pseudocode.services.user_service import UserService

        mock_user_repository.get_by_id.return_value = MagicMock(
            id="user_123",
            openid="existing_openid_123",
            nickname="Test User",
            subscription_type="FREE",
            target_university="Xi'an University",
            subscription_expiry=datetime.utcnow() + timedelta(days=15),
            total_practice_count=100,
            last_practice_time=datetime.utcnow() - timedelta(hours=5)
        )

        service = UserService(
            encryption_manager=mock_encryption_manager,
            jwt_manager=mock_jwt_manager
        )

        result = service.get_user_profile(user_id="user_123")

        assert result["user_id"] == "user_123"
        assert result["nickname"] == "Test User"
        assert result["openid"] == "existing_openid_123"
        assert result["subscription_type"] == "FREE"

    def test_update_user_profile(self, mock_user_repository, mock_jwt_manager):
        """Test updating user profile."""
        from pseudocode.services.user_service import UserService
        from pseudocode.models.user import UserUpdate

        service = UserService(
            encryption_manager=mock_encryption_manager,
            jwt_manager=mock_jwt_manager
        )

        update_data = UserUpdate(
            nickname="Updated Name",
            phone="15912345678",
            email="updated@example.com",
            target_university="Xi'an University",
            target_major="Computer Science"
        )

        mock_user_repository.get_by_id.return_value = MagicMock(
            id="user_123",
            openid="existing_openid_123",
            nickname="Test User",
            phone="13800138000",
            email="test@example.com"
        )

        result = service.update_user_profile(user_id="user_123", **update_data)

        assert result["nickname"] == "Updated Name"
        assert result["phone"] == "15912345678"
        assert result["email"] == "updated@example.com"

    def test_check_subscription_is_premium(self, mock_user_repository, mock_jwt_manager):
        """Test checking premium subscription status."""
        from pseudocode.services.user_service import UserService

        service = UserService(
            encryption_manager=mock_encryption_manager,
            jwt_manager=mock_jwt_manager
        )

        mock_user_repository.get_by_id.return_value = MagicMock(
            id="user_123",
            subscription_type="PREMIUM_30D",
            target_university="Xi'an University",
            target_major="Computer Science"
            )

        result = service.check_subscription(user_id="user_123")

        assert result["is_premium"] is True
        assert result["can_practice_university"] is True

    def test_check_subscription_is_expired(self, mock_user_repository, mock_jwt_manager):
        """Test checking expired subscription."""
        from pseudocode.services.user_service import UserService

        mock_user_repository.get_by_id.return_value = MagicMock(
            id="user_123",
            subscription_type="PREMIUM_30D",
            target_university="Xi'an University",
            subscription_expiry=datetime.utcnow() - timedelta(days=1)
        )

        result = service.check_subscription(user_id="user_123")

        assert result["is_expired"] is True
        assert result["is_expired"] is True

    def test_check_subscription_free(self, mock_user_repository, mock_jwt_manager):
        """Test free subscription."""
        from pseudocode.services.user_service import UserService

        service = UserService(
            encryption_manager=mock_encryption_manager,
            jwt_manager=mock_jwt_manager
        )

        mock_user_repository.get_by_id.return_value = MagicMock(
            id="user_123",
            subscription_type="FREE",
            subscription_expiry=None
        )

        result = service.check_subscription(user_id="user_123")

        assert result["is_premium"] is False
        assert result["is_expired"] is False

    def test_get_practice_count(self, mock_user_repository):
        """Test getting practice count."""
        from pseudocode.services.user_service import UserService

        mock_user_repository.get_practice_count.return_value = 42

        service = UserService(
            encryption_manager=mock_encryption_manager,
            jwt_manager=mock_jwt_manager
        )

        result = service.get_practice_count(user_id="user_123")

        assert result == 42

    def test_update_practice_count(self, mock_user_repository, mock_jwt_manager):
        """Test updating practice count."""
        from pseudocode.services.user_service import UserService

        mock_user_repository.get_by_id.return_value = MagicMock(
            id="user_123",
            total_practice_count=42
        )

        service = UserService(
            encryption_manager=mock_encryption_manager,
            jwt_manager=mock_jwt_manager
        )

        mock_jwt_manager.verify_token.return_value = {"valid": True, "user_id": "user_123"}

        result = service.update_practice_count(user_id="user_123")

        assert result["total_practice_count"] == 43

    def test_get_user_stats(self, mock_user_repository, mock_jwt_manager):
        """Test getting user statistics."""
        from pseudocode.services.user_service import UserService

        mock_user_repository.get_by_id.return_value = MagicMock(
            id="user_123",
            total_practice_count=42,
            last_practice_time=datetime.utcnow() - timedelta(hours=5)
        )

        service = UserService(
            encryption_manager=mock_encryption_manager,
            jwt_manager=mock_jwt_manager
        )

        result = service.get_user_stats(user_id="user_123")

        assert result["total_practice_count"] == 42
        assert result["last_practice_time"] is not None


@pytest.fixture
def mock_user_repository():
    """Mock UserRepository for testing."""
    from unittest.mock import MagicMock

    repository = MagicMock(spec="UserRepository")
    repository._users_db = {}

    def get_by_id(user_id: str) -> Optional[MagicMock(spec=None)]:
        """Get user by ID."""
        db = repository._users_db.get(user_id, {})
        return db.get(user_id)


@pytest.fixture
def mock_encryption_manager():
    """Mock EncryptionManager for testing."""
    from unittest.mock import MagicMock

    manager = MagicMock(spec="EncryptionManager")
    return manager


@pytest.fixture
def mock_jwt_manager():
    """Mock JWTManager for testing."""
    from unittest.mock import MagicMock

    manager = MagicMock(spec="JWTManager")
    return manager
