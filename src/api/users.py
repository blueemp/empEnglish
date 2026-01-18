"""Users router."""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from src.utils.config import settings
from src.utils.database import get_db
from src.models.user import User

router = APIRouter()


class UserProfileResponse(BaseModel):
    """User profile response."""

    id: str
    openid: str
    subscription_type: str
    nickname: str | None = None
    avatar_url: str | None = None
    target_university: str | None = None
    target_major: str | None = None
    total_practice_count: int
    is_premium: bool


class SubscriptionCheckResponse(BaseModel):
    """Subscription check response."""

    subscription_type: str
    is_premium: bool
    is_expired: bool
    subscription_expiry: str | None = None


@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile():
    """
    Get user profile.

    Requires authentication header with JWT token.
    """
    # TODO: Implement JWT authentication dependency
    # from src.api.dependencies import get_current_user

    # Mock response for now
    return UserProfileResponse(
        id="user123",
        openid="mock_openid",
        subscription_type="PREMIUM_15D",
        nickname="Test User",
        avatar_url=None,
        target_university="西安交通大学",
        target_major="计算机科学与技术",
        total_practice_count=50,
        is_premium=True,
    )


@router.put("/profile", response_model=UserProfileResponse)
async def update_user_profile():
    """
    Update user profile.

    Requires authentication.
    """
    # TODO: Implement update logic
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Profile update not yet implemented",
    )


@router.get("/subscription", response_model=SubscriptionCheckResponse)
async def check_subscription():
    """
    Check user subscription status.

    Requires authentication.
    """
    # TODO: Implement subscription check
    return SubscriptionCheckResponse(
        subscription_type="PREMIUM_15D",
        is_premium=True,
        is_expired=False,
        subscription_expiry="2026-02-17T20:00:00Z",
    )
