"""
Tests for User Model (TDD approach).
"""
import pytest
from datetime import datetime, timedelta
from enum import Enum
import uuid


class TestSubscriptionType:
    """Test cases for SubscriptionType enum."""

    def test_free_exists(self):
        """Test FREE subscription type."""
        from pseudocode.models.user import SubscriptionType

        assert SubscriptionType.FREE.value == "FREE"

    def test_trial_exists(self):
        """Test TRIAL subscription type."""
        from pseudocode.models.user import SubscriptionType

        assert SubscriptionType.TRIAL.value == "TRIAL"

    def test_premium_15d_exists(self):
        """Test PREMIUM_15D subscription type."""
        from pseudocode.models.user import SubscriptionType

        assert SubscriptionType.PREMIUM_15D.value == "PREMIUM_15D"

    def test_premium_30d_exists(self):
        """Test PREMIUM_30D subscription type."""
        from pseudocode.models.user import SubscriptionType

        assert SubscriptionType.PREMIUM_30D.value == "PREMIUM_30D"

    def test_annual_exists(self):
        """Test ANNUAL subscription type."""
        from pseudocode.models.user import SubscriptionType

        assert SubscriptionType.ANNUAL.value == "ANNUAL"


class TestUser:
    """Test cases for User SQLAlchemy model."""

    def test_model_attributes(self):
        """Test User model has required attributes."""
        from pseudocode.models.user import User

        user = User(
            id=str(uuid.uuid4()),
            openid="test_openid",
            nickname="Test User",
            subscription_type=SubscriptionType.FREE.value,
            created_at=datetime.utcnow()
        )

        assert hasattr(user, 'id')
        assert hasattr(user, 'openid')
        assert hasattr(user, 'nickname')
        assert hasattr(user, 'subscription_type')
        assert hasattr(user, 'created_at')

    def test_subscription_types(self):
        """Test all subscription types are valid."""
        from pseudocode.models.user import SubscriptionType

        valid_types = [
            SubscriptionType.FREE,
            SubscriptionType.TRIAL,
            SubscriptionType.PREMIUM_15D,
            SubscriptionType.PREMIUM_30D,
            SubscriptionType.ANNUAL
        ]

        for sub_type in valid_types:
            assert isinstance(sub_type, Enum)

    def test_user_with_premium_subscription(self):
        """Test user with premium subscription."""
        from pseudocode.models.user import User, SubscriptionType

        user = User(
            id=str(uuid.uuid4()),
            openid="premium_openid",
            subscription_type=SubscriptionType.PREMIUM_30D.value,
            subscription_expires_at=datetime.utcnow() + timedelta(days=30),
            created_at=datetime.utcnow()
        )

        assert user.subscription_type == "PREMIUM_30D"
        assert user.subscription_expires_at is not None

    def test_user_with_free_subscription(self):
        """Test user with free subscription has no expiration."""
        from pseudocode.models.user import User, SubscriptionType

        user = User(
            id=str(uuid.uuid4()),
            openid="free_openid",
            subscription_type=SubscriptionType.FREE.value,
            created_at=datetime.utcnow()
        )

        assert user.subscription_type == "FREE"
        assert user.subscription_expires_at is None

    def test_soft_delete_attribute(self):
        """Test user has soft delete attribute."""
        from pseudocode.models.user import User

        user = User(
            id=str(uuid.uuid4()),
            openid="test_openid",
            created_at=datetime.utcnow(),
            deleted_at=None
        )

        assert user.deleted_at is None


class TestUserCreate:
    """Test cases for UserCreate Pydantic model."""

    def test_valid_user_create(self, sample_user_data):
        """Test creating valid user from data."""
        from pseudocode.models.user import UserCreate

        user_data = sample_user_data
        user_create = UserCreate(**user_data)

        assert user_create.openid == "test_openid_123"
        assert user_create.nickname == "Test User"
        assert user_create.subscription_type == "FREE"

    def test_missing_openid(self):
        """Test validation fails without openid."""
        from pseudocode.models.user import UserCreate
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            UserCreate(
                nickname="Test User",
                subscription_type="FREE"
            )

    def test_invalid_subscription_type(self, sample_user_data):
        """Test validation fails with invalid subscription type."""
        from pseudocode.models.user import UserCreate
        from pydantic import ValidationError

        invalid_data = sample_user_data.copy()
        invalid_data["subscription_type"] = "INVALID_TYPE"

        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)


class TestUserUpdate:
    """Test cases for UserUpdate Pydantic model."""

    def test_valid_update(self):
        """Test valid user update data."""
        from pseudocode.models.user import UserUpdate

        update_data = {
            "nickname": "Updated Nickname",
            "target_university": "Xi'an University"
            "target_major": "Computer Science"
        }

        user_update = UserUpdate(**update_data)

        assert user_update.nickname == "Updated Nickname"
        assert user_update.target_university == "Xi'an University"

    def test_empty_update(self):
        """Test update with empty data."""
        from pseudocode.models.user import UserUpdate

        update_data = {}
        user_update = UserUpdate(**update_data)

        assert user_update.nickname is None
        assert user_update.target_university is None


class TestUserResponse:
    """Test cases for UserResponse Pydantic model."""

    def test_user_response_from_model(self, sample_user_data):
        """Test creating response from user data."""
        from pseudocode.models.user import UserResponse

        response_data = {
            **sample_user_data,
            "id": "user_123",
            "created_at": datetime.utcnow().isoformat()
        }

        response = UserResponse(**response_data)

        assert response.id == "user_123"
        assert response.nickname == "Test User"
        assert response.openid == "test_openid_123"


class TestUserRepository:
    """Test cases for UserRepository class."""

    def test_create_user(self, sample_user_data):
        """Test creating a user."""
        from pseudocode.models.user import UserRepository, User

        user = UserRepository.create(
            openid="test_openid",
            nickname="Test User",
            subscription_type="FREE"
        )

        assert user is not None
        assert user.openid == "test_openid"

    def test_get_by_id(self, sample_user_data):
        """Test getting user by ID."""
        from pseudocode.models.user import UserRepository, User

        user = UserRepository.create(
            openid="test_openid",
            nickname="Test User",
            subscription_type="FREE"
        )

        found_user = UserRepository.get_by_id(user.id)

        assert found_user is not None
        assert found_user.id == user.id

    def test_get_by_openid(self, sample_user_data):
        """Test getting user by openid."""
        from pseudocode.models.user import UserRepository, User

        user = UserRepository.create(
            openid="test_openid_unique",
            nickname="Test User",
            subscription_type="FREE"
        )

        found_user = UserRepository.get_by_openid("test_openid_unique")

        assert found_user is not None
        assert found_user.openid == "test_openid_unique"

    def test_update_user(self, sample_user_data):
        """Test updating user."""
        from pseudocode.models.user import UserRepository, User

        user = UserRepository.create(
            openid="test_openid",
            nickname="Original Name",
            subscription_type="FREE"
        )

        updated_user = UserRepository.update(
            user_id=user.id,
            nickname="Updated Name"
        )

        assert updated_user.nickname == "Updated Name"

    def test_delete_user(self, sample_user_data):
        """Test soft deleting user."""
        from pseudocode.models.user import UserRepository, User

        user = UserRepository.create(
            openid="test_openid",
            nickname="Test User",
            subscription_type="FREE"
        )

        result = UserRepository.delete(user.id)

        assert result is True

        deleted_user = UserRepository.get_by_id(user.id)
        assert deleted_user is not None
        assert deleted_user.deleted_at is not None

    def test_list_users(self):
        """Test listing users."""
        from pseudocode.models.user import UserRepository

        user1 = UserRepository.create(
            openid="open1", nickname="User 1", subscription_type="FREE"
        )
        user2 = UserRepository.create(
            openid="open2", nickname="User 2", subscription_type="FREE"
        )

        users = UserRepository.list(limit=10, offset=0)

        assert len(users) >= 2
