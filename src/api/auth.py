"""Authentication router."""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from src.utils.jwt_manager import JWTManager
from src.utils.config import settings

router = APIRouter()
jwt_manager = JWTManager(secret_key=settings.JWT_SECRET_KEY)


class WechatLoginRequest(BaseModel):
    """WeChat login request."""

    code: str


class TokenRefreshRequest(BaseModel):
    """Token refresh request."""

    refresh_token: str


class LoginResponse(BaseModel):
    """Login response."""

    user_id: str
    access_token: str
    refresh_token: str
    expires_in: int


@router.post(
    "/wechat/login", response_model=LoginResponse, status_code=status.HTTP_200_OK
)
async def wechat_login(request: WechatLoginRequest):
    """
    WeChat login endpoint.

    Calls WeChat API to get openid and session_key,
    then generates JWT tokens.
    """
    try:
        # In production, call actual WeChat API
        # import requests
        # response = requests.post(
        #     "https://api.weixin.qq.com/sns/jscode2session",
        #     params={
        #         "appid": settings.WECHAT_APP_ID,
        #         "secret": settings.WECHAT_APP_SECRET,
        #         "js_code": request.code,
        #         "grant_type": "authorization_code"
        #     }
        # )
        # wechat_data = response.json()
        # openid = wechat_data["openid"]

        # For now, use mock openid
        openid = "mock_openid_" + request.code

        # Generate JWT tokens
        access_token = jwt_manager.generate_access_token(openid)
        refresh_token = jwt_manager.generate_refresh_token(openid)

        return LoginResponse(
            user_id=openid,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"WeChat login failed: {str(e)}",
        )


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(request: TokenRefreshRequest):
    """
    Refresh access token using refresh token.
    """
    try:
        payload = jwt_manager.verify_token(request.refresh_token)

        # Verify it's a refresh token
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token"
            )

        # Generate new access token
        new_access_token = jwt_manager.generate_access_token(payload["user_id"])

        return {
            "access_token": new_access_token,
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token refresh failed: {str(e)}",
        )
