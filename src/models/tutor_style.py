# 导师风格模型伪代码
# 文件路径: models/tutor_style.py

from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel
from sqlalchemy import Column, String, Text, Integer, DateTime, JSON, SQLEnum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 导师风格类型枚举
class TutorStyleType(str, Enum):
    ACADEMIC_DEEP = "academic_deep"  # 学术深挖型
    PRACTICE_ORIENTED = "practice_oriented"  # 实践导向型
    FRIENDLY = "friendly"  # 友好交流型
    HIGH_PRESSURE = "high_pressure"  # 高压盘问型


class TutorStyle(Base):
    """导师风格数据库模型"""
    __tablename__ = "tutor_styles"

    id = Column(String(64), primary_key=True, comment="风格ID，UUID")
    university = Column(String(100), nullable=False, comment="所属院校")
    college = Column(String(100), comment="所属学院")
    major = Column(String(100), comment="所属专业")
    style_type = Column(SQLEnum(TutorStyleType), nullable=False, comment="风格类型")
    name = Column(String(100), nullable=False, comment="风格名称")
    description = Column(Text, comment="风格描述")
    personality = Column(String(200), comment="性格描述")
    questioning_style = Column(String(200), comment="提问风格")
    tone = Column(String(50), comment="语气：formal/casual/friendly/stern")
    follow_up_frequency = Column(Integer, default=50, comment="追问频率：0-100")
    tolerance_level = Column(Integer, default=70, comment="容忍度：0-100")
    system_prompt = Column(Text, comment="系统提示词")
    examples = Column(JSON, comment="示例对话")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    @classmethod
    def create(cls, **kwargs):
        """创建导师风格"""
        style = cls(**kwargs)
        return style

    def get_tts_style(self) -> str:
        """获取TTS风格"""
        style_map = {
            TutorStyleType.ACADEMIC_DEEP: "academic",
            TutorStyleType.FRIENDLY: "friendly",
            TutorStyleType.HIGH_PRESSURE: "high_pressure",
            TutorStyleType.PRACTICE_ORIENTED: "academic"
        }
        return style_map.get(self.style_type, "academic")


class TutorStyleResponse(BaseModel):
    """导师风格响应DTO"""
    id: str
    university: str
    college: Optional[str]
    major: Optional[str]
    style_type: TutorStyleType
    name: str
    description: Optional[str]
    personality: Optional[str]
    questioning_style: Optional[str]
    tone: Optional[str]
    follow_up_frequency: int
    tolerance_level: int

    class Config:
        from_attributes = True


class TutorStyleRepository:
    """导师风格数据访问层"""

    @staticmethod
    def get_by_id(style_id: str) -> Optional[TutorStyle]:
        """根据ID获取导师风格"""
        # 伪代码：实际实现使用数据库查询
        # return session.query(TutorStyle).filter(TutorStyle.id == style_id).first()
        pass

    @staticmethod
    def list_styles(
        university: Optional[str] = None,
        style_type: Optional[TutorStyleType] = None,
        is_active: bool = True
    ) -> List[TutorStyle]:
        """获取导师风格列表"""
        # 伪代码：实际实现使用数据库查询
        # query = session.query(TutorStyle).filter(TutorStyle.is_active == is_active)
        # if university:
        #     query = query.filter(TutorStyle.university == university)
        # if style_type:
        #     query = query.filter(TutorStyle.style_type == style_type)
        # return query.all()
        pass

    @staticmethod
    def get_default_style(style_type: TutorStyleType) -> Optional[TutorStyle]:
        """获取默认风格"""
        # 伪代码：实际实现使用数据库查询
        # return session.query(TutorStyle).filter(
        #     TutorStyle.style_type == style_type,
        #     TutorStyle.university == "default"
        # ).first()
        pass

    @staticmethod
    def create(style: TutorStyle) -> TutorStyle:
        """创建导师风格"""
        # 伪代码：实际实现使用数据库插入
        # session.add(style)
        # session.commit()
        # session.refresh(style)
        return style