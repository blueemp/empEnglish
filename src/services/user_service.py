# 用户服务伪代码
# 文件路径: services/user_service.py

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from models.user import User, UserCreate, UserUpdate, UserResponse, UserRepository
from utils.jwt_manager import JWTManager
from utils.encryption_manager import EncryptionManager


class UserService:
    """用户服务"""

    def __init__(self, jwt_manager: JWTManager, encryption_manager: EncryptionManager):
        self.jwt_manager = jwt_manager
        self.encryption_manager = encryption_manager

    def wechat_login(self, code: str) -> Dict[str, Any]:
        """
        微信登录
        """
        # 1. 调用微信API获取openid和session_key
        wechat_response = self._get_wechat_user_info(code)
        openid = wechat_response["openid"]
        unionid = wechat_response.get("unionid")
        session_key = wechat_response["session_key"]

        # 2. 查询用户是否存在
        user = UserRepository.get_by_openid(openid)

        # 3. 如果不存在，创建新用户
        if user is None:
            user_data = {
                "openid": openid,
                "unionid": unionid,
                "subscription_type": "FREE"
            }
            user = User.create(**user_data)
            UserRepository.create(user)

        # 4. 生成JWT token
        access_token = self.jwt_manager.generate_access_token(user.id)
        refresh_token = self.jwt_manager.generate_refresh_token(user.id)

        # 5. 返回登录结果
        return {
            "user_id": user.id,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": 7200,
            "user": UserResponse.model_validate(user)
        }

    def get_user_profile(self, user_id: str) -> UserResponse:
        """
        获取用户信息
        """
        user = UserRepository.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        return UserResponse.model_validate(user)

    def update_user_profile(self, user_id: str, update_data: UserUpdate) -> UserResponse:
        """
        更新用户信息
        """
        user = UserRepository.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        # 更新字段
        update_dict = update_data.model_dump(exclude_unset=True)
        user.update(**update_dict)

        # 保存到数据库
        UserRepository.update(user)

        return UserResponse.model_validate(user)

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        刷新访问令牌
        """
        # 验证刷新令牌
        payload = self.jwt_manager.verify_token(refresh_token)

        if payload["type"] != "refresh":
            raise ValueError("Invalid refresh token")

        # 生成新的访问令牌
        new_access_token = self.jwt_manager.refresh_access_token(refresh_token)

        return {
            "access_token": new_access_token,
            "expires_in": 7200
        }

    def check_subscription(self, user_id: str) -> Dict[str, Any]:
        """
        检查订阅状态
        """
        user = UserRepository.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        is_premium = user.is_premium()
        is_expired = False

        if user.subscription_expiry and user.subscription_expiry < datetime.utcnow():
            is_expired = True

        return {
            "subscription_type": user.subscription_type,
            "is_premium": is_premium,
            "is_expired": is_expired,
            "subscription_expiry": user.subscription_expiry
        }

    def update_practice_count(self, user_id: str):
        """
        更新练习次数
        """
        user = UserRepository.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        user.total_practice_count += 1
        user.last_practice_time = datetime.utcnow()

        UserRepository.update(user)

    def _get_wechat_user_info(self, code: str) -> Dict[str, Any]:
        """
        调用微信API获取用户信息
        """
        # 伪代码：实际实现需要调用微信API
        # import requests
        # response = requests.get(
        #     f"https://api.weixin.qq.com/sns/jscode2session",
        #     params={
        #         "appid": WECHAT_APP_ID,
        #         "secret": WECHAT_APP_SECRET,
        #         "js_code": code,
        #         "grant_type": "authorization_code"
        #     }
        # )
        # return response.json()

        # 模拟返回
        return {
            "openid": "mock_openid",
            "unionid": "mock_unionid",
            "session_key": "mock_session_key"
        }


class UserPermissionChecker:
    """用户权限检查器"""

    @staticmethod
    def can_practice_general(user: User) -> bool:
        """检查是否可以练习通用模式"""
        return True  # 所有用户都可以练习通用模式

    @staticmethod
    def can_practice_university(user: User) -> bool:
        """检查是否可以练习院校定制模式"""
        return user.is_premium()

    @staticmethod
    def can_export_report(user: User) -> bool:
        """检查是否可以导出报告"""
        return user.is_premium()

    @staticmethod
    def can_use_high_pressure_mode(user: User) -> bool:
        """检查是否可以使用高压模式"""
        return user.is_premium()

    @staticmethod
    def can_use_follow_up(user: User) -> bool:
        """检查是否可以使用追问功能"""
        return user.is_premium()

    @staticmethod
    def can_view_advanced_feedback(user: User) -> bool:
        """检查是否可以查看高级反馈"""
        return user.is_premium()

    @staticmethod
    def check_daily_limit(user: User) -> Dict[str, Any]:
        """检查每日练习限制"""
        # 伪代码：实际实现需要查询今日练习次数
        today_count = 0  # 从数据库查询

        limits = {
            "FREE": 1,
            "TRIAL": 5,
            "PREMIUM_15D": 10,
            "PREMIUM_30D": 10,
            "ANNUAL": 10
        }

        max_count = limits.get(user.subscription_type, 1)
        remaining = max(0, max_count - today_count)

        return {
            "today_count": today_count,
            "max_count": max_count,
            "remaining": remaining,
            "can_practice": remaining > 0
        }