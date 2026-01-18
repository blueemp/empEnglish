# 用户模型实现代码
# 文件路径: models/user.py

from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SubscriptionType(str, Enum):
    FREE = "free"
    TRIAL = "trial"
    PREMIUM_15D = "premium_15d"
    PREMIUM_30D = "premium_30d"
    ANNUAL = "annual"


class User(Base):
    """用户数据库模型"""

    __tablename__ = "users"

    id = Column(String(64), primary_key=True, comment="用户ID，UUID")
    openid = Column(String(128), unique=True, nullable=False, comment="微信OpenID")
    unionid = Column(String(128), unique=True, comment="微信UnionID")
    nickname = Column(String(100), comment="昵称")
    avatar_url = Column(String(500), comment="头像URL")
    phone = Column(String(20), comment="手机号")
    email = Column(String(100), comment="邮箱")
    target_university = Column(String(100), comment="目标院校")
    target_college = Column(String(100), comment="目标学院")
    target_major = Column(String(100), comment="目标专业")
    subscription_type = Column(
        SQLEnum(SubscriptionType), default=SubscriptionType.FREE, comment="订阅类型"
    )
    subscription_expiry = Column(DateTime, comment="订阅到期时间")
    total_practice_count = Column(Integer, default=0, comment="总练习次数")
    last_practice_time = Column(DateTime, comment="最后练习时间")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间"
    )
    deleted_at = Column(DateTime, comment="删除时间")

    @classmethod
    def create(cls, **kwargs):
        """创建用户"""
        user = cls(**kwargs)
        return user

    def update(self, **kwargs):
        """更新用户信息"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def is_premium(self):
        """检查是否为付费用户"""
        if self.subscription_type == SubscriptionType.FREE:
            return False
        if self.subscription_expiry and self.subscription_expiry < datetime.utcnow():
            return False
        return True

    def can_practice_university(self):
        """检查是否可以练习院校定制模式"""
        return self.is_premium()

    def needs_daily_report(self):
        """检查是否需要生成每日报告"""
        return True


class UserCreate(BaseModel):
    """用户创建DTO"""

    openid: str
    unionid: Optional[str] = None
    nickname: str
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    target_university: Optional[str] = None
    target_college: Optional[str] = None
    target_major: Optional[str] = None
    subscription_type: SubscriptionType = SubscriptionType.FREE


class UserUpdate(BaseModel):
    """用户更新DTO"""

    nickname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    target_university: Optional[str] = None
    target_college: Optional[str] = None
    target_major: Optional[str] = None


class UserResponse(BaseModel):
    """用户响应DTO"""

    id: str
    openid: str
    unionid: Optional[str] = None
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    target_university: Optional[str] = None
    target_college: Optional[str] = None
    target_major: Optional[str] = None
    subscription_type: SubscriptionType
    subscription_expiry: Optional[datetime] = None
    total_practice_count: int
    last_practice_time: Optional[datetime] = None
    created_at: datetime


class Config:
    from_attributes = True


class UserRepository:
    """用户数据访问层"""

    _users_db = {}

    @staticmethod
    def _get_db_session():
        """获取数据库会话（模拟）"""
        return UserRepository._users_db

    @staticmethod
    def get_by_id(user_id: str) -> Optional[User]:
        """根据ID获取用户"""
        db = UserRepository._get_db_session()
        return db.get(user_id)

    @staticmethod
    def get_by_openid(openid: str) -> Optional[User]:
        """根据OpenID获取用户"""
        db = UserRepository._get_db_session()
        return next((u for u in db.values() if u.openid == openid), None)

    @staticmethod
    def create(user: User) -> User:
        """创建用户"""
        db = UserRepository._get_db_session()
        user.id = f"user_{len(db) + 1}"
        user.created_at = datetime.utcnow()
        db[user.id] = user
        return user

    @staticmethod
    def update(user_id: str, **kwargs):
        """更新用户"""
        db = UserRepository._get_db_session()
        user = db.get(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            user.updated_at = datetime.utcnow()
        return user

    @staticmethod
    def delete(user_id: str) -> bool:
        """软删除用户"""
        db = UserRepository._get_db_session()
        user = db.get(user_id)
        if user:
            user.deleted_at = datetime.utcnow()
            user.is_active = False
        return True

    @staticmethod
    def list(limit: int = 100, offset: int = 0) -> List[User]:
        """获取用户列表"""
        db = UserRepository._get_db_session()
        users = list(db.values())[offset : offset + limit]
        return [u for u in users if u.deleted_at is None]
