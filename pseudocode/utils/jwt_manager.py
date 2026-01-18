# JWT管理器伪代码
# 文件路径: utils/jwt_manager.py

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import jwt


class JWTManager:
    """JWT管理器"""

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        """
        初始化JWT管理器

        Args:
            secret_key: 密钥
            algorithm: 算法
        """
        self.secret_key = secret_key
        self.algorithm = algorithm

        # Token配置
        self.access_token_expire_hours = 2
        self.refresh_token_expire_days = 7

    def generate_access_token(
        self, user_id: str, payload: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        生成访问令牌

        Args:
            user_id: 用户ID
            payload: 额外载荷

        Returns:
            访问令牌
        """
        now = datetime.utcnow()

        # 构建默认载荷
        default_payload = {
            "user_id": user_id,
            "type": "access",
            "iat": now,
            "exp": now + timedelta(hours=self.access_token_expire_hours),
        }

        # 合并额外载荷
        if payload:
            default_payload.update(payload)

        # 生成令牌
        token = jwt.encode(default_payload, self.secret_key, algorithm=self.algorithm)

        return token

    def generate_refresh_token(self, user_id: str) -> str:
        """
        生成刷新令牌

        Args:
            user_id: 用户ID

        Returns:
            刷新令牌
        """
        now = datetime.utcnow()

        payload = {
            "user_id": user_id,
            "type": "refresh",
            "iat": now,
            "exp": now + timedelta(days=self.refresh_token_expire_days),
        }

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

        return token

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        验证令牌

        Args:
            token: 令牌

        Returns:
            验证结果字典 {"valid": bool, "user_id": str, "type": str, "error": str | None}

        Raises:
            Exception: 令牌无效或过期
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return {
                "valid": True,
                "user_id": payload.get("user_id"),
                "type": payload.get("type"),
                "error": None,
            }
        except jwt.ExpiredSignatureError:
            return {
                "valid": False,
                "user_id": None,
                "type": None,
                "error": "Token expired",
            }
        except jwt.InvalidTokenError as e:
            return {"valid": False, "user_id": None, "type": None, "error": str(e)}

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        解码并验证令牌

        Args:
            token: 令牌

        Returns:
            载荷（如果有效）或None（如果无效）

        Raises:
            jwt.ExpiredSignatureError: 令牌过期
            jwt.InvalidTokenError: 令牌无效
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("Token expired")
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError("Invalid token")

    def refresh_access_token(self, refresh_token: str) -> str:
        """
        刷新访问令牌

        Args:
            refresh_token: 刷新令牌

        Returns:
            新的访问令牌

        Raises:
            Exception: 刷新令牌无效
        """
        # 验证刷新令牌
        payload = self.verify_token(refresh_token)

        if payload["type"] != "refresh":
            raise Exception("Invalid refresh token")

        # 生成新的访问令牌
        return self.generate_access_token(payload["user_id"])

    def get_user_id_from_token(self, token: str) -> str:
        """
        从令牌中获取用户ID

        Args:
            token: 令牌

        Returns:
            用户ID
        """
        payload = self.verify_token(token)
        return payload["user_id"]

    def is_token_expired(self, token: str) -> bool:
        """
        检查令牌是否过期

        Args:
            token: 令牌

        Returns:
            是否过期
        """
        try:
            self.verify_token(token)
            return False
        except Exception as e:
            if "expired" in str(e).lower():
                return True
            return True

    def decode_token_without_verification(self, token: str) -> Optional[Dict[str, Any]]:
        """
        不验证签名地解码令牌（仅用于调试）

        Args:
            token: 令牌

        Returns:
            载荷
        """
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload
        except Exception:
            return None


class JWTConfig:
    """JWT配置"""

    # 算法列表
    ALGORITHMS = ["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]

    # 推荐算法
    RECOMMENDED_ALGORITHM = "HS256"

    # 令牌过期时间配置
    ACCESS_TOKEN_EXPIRE = {
        "short": {"hours": 1},
        "normal": {"hours": 2},
        "long": {"hours": 4},
    }

    REFRESH_TOKEN_EXPIRE = {
        "short": {"days": 3},
        "normal": {"days": 7},
        "long": {"days": 30},
    }

    @classmethod
    def get_algorithm_info(cls, algorithm: str) -> Dict[str, Any]:
        """
        获取算法信息

        Args:
            algorithm: 算法名称

        Returns:
            算法信息
        """
        info = {
            "HS256": {"name": "HMAC SHA-256", "type": "symmetric"},
            "HS384": {"name": "HMAC SHA-384", "type": "symmetric"},
            "HS512": {"name": "HMAC SHA-512", "type": "symmetric"},
            "RS256": {"name": "RSA SHA-256", "type": "asymmetric"},
            "RS384": {"name": "RSA SHA-384", "type": "asymmetric"},
            "RS512": {"name": "RSA SHA-512", "type": "asymmetric"},
        }
        return info.get(algorithm, {})

    @classmethod
    def is_symmetric_algorithm(cls, algorithm: str) -> bool:
        """
        检查是否为对称算法

        Args:
            algorithm: 算法名称

        Returns:
            是否为对称算法
        """
        info = cls.get_algorithm_info(algorithm)
        return info.get("type") == "symmetric"
