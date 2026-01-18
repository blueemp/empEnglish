# 题目模型伪代码
# 文件路径: models/question.py

from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, JSON, SQLEnum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 题目类型枚举
class QuestionType(str, Enum):
    GENERAL = "general"
    UNIVERSITY = "university"
    MAJOR = "major"


# 难度等级枚举
class DifficultyLevel(int, Enum):
    EASY = 1
    BASIC = 2
    MEDIUM = 3
    HARD = 4
    EXPERT = 5


# 题类枚举
class QuestionCategory(str, Enum):
    INTRODUCTION = "introduction"  # 自我介绍
    FAMILY = "family"  # 家庭
    EDUCATION = "education"  # 教育背景
    RESEARCH = "research"  # 研究经历
    INTEREST = "interest"  # 研究兴趣
    MOTIVATION = "motivation"  # 报考动机
    CAREER = "career"  # 职业规划
    GENERAL = "general"  # 通用


class Question(Base):
    """题目数据库模型"""
    __tablename__ = "questions"

    id = Column(String(64), primary_key=True, comment="题目ID，UUID")
    type = Column(
        SQLEnum(QuestionType),
        nullable=False,
        comment="题目类型"
    )
    university = Column(String(100), comment="所属院校")
    college = Column(String(100), comment="所属学院")
    major = Column(String(100), comment="所属专业")
    category = Column(
        SQLEnum(QuestionCategory),
        nullable=False,
        comment="题类"
    )
    difficulty = Column(Integer, default=3, comment="难度等级：1-5")
    content = Column(Text, nullable=False, comment="题目内容")
    reference_answer = Column(Text, comment="参考答案")
    tags = Column(JSON, comment="标签列表")
    keywords = Column(JSON, comment="关键词列表，用于追问")
    style_tags = Column(JSON, comment="导师风格标签")
    usage_count = Column(Integer, default=0, comment="使用次数")
    avg_score = Column(Integer, comment="平均得分")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_premium = Column(Boolean, default=False, comment="是否为付费题目")
    created_by = Column(String(64), comment="创建人ID")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    deleted_at = Column(DateTime, comment="删除时间")

    @classmethod
    def create(cls, **kwargs):
        """创建题目"""
        question = cls(**kwargs)
        return question

    def update_usage(self, score: Optional[float] = None):
        """更新使用统计"""
        self.usage_count += 1
        if score is not None:
            # 更新平均得分
            if self.avg_score is None:
                self.avg_score = score
            else:
                self.avg_score = (self.avg_score * (self.usage_count - 1) + score) / self.usage_count


class QuestionCreate(BaseModel):
    """题目创建DTO"""
    type: QuestionType
    university: Optional[str] = None
    college: Optional[str] = None
    major: Optional[str] = None
    category: QuestionCategory
    difficulty: int = 3
    content: str
    reference_answer: Optional[str] = None
    tags: Optional[List[str]] = []
    keywords: Optional[List[str]] = []
    style_tags: Optional[List[str]] = []
    is_premium: bool = False


class QuestionResponse(BaseModel):
    """题目响应DTO"""
    id: str
    type: QuestionType
    university: Optional[str]
    college: Optional[str]
    major: Optional[str]
    category: QuestionCategory
    difficulty: int
    content: str
    reference_answer: Optional[str]
    tags: Optional[List[str]]
    keywords: Optional[List[str]]
    style_tags: Optional[List[str]]
    is_premium: bool
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionRecommend(BaseModel):
    """题目推荐DTO"""
    id: str
    type: QuestionType
    university: Optional[str]
    major: Optional[str]
    category: QuestionCategory
    difficulty: int
    content: str
    match_score: float  # 匹配度分数
    reason: str  # 推荐理由


class QuestionRepository:
    """题目数据访问层"""

    @staticmethod
    def get_by_id(question_id: str) -> Optional[Question]:
        """根据ID获取题目"""
        # 伪代码：实际实现使用数据库查询
        # return session.query(Question).filter(Question.id == question_id).first()
        pass

    @staticmethod
    def list_questions(
        type: Optional[QuestionType] = None,
        university: Optional[str] = None,
        major: Optional[str] = None,
        category: Optional[QuestionCategory] = None,
        difficulty: Optional[int] = None,
        is_active: bool = True,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[List[Question], int]:
        """获取题目列表"""
        # 伪代码：实际实现使用数据库查询
        # query = session.query(Question).filter(Question.is_active == is_active)
        # if type:
        #     query = query.filter(Question.type == type)
        # if university:
        #     query = query.filter(Question.university == university)
        # if major:
        #     query = query.filter(Question.major == major)
        # if category:
        #     query = query.filter(Question.category == category)
        # if difficulty:
        #     query = query.filter(Question.difficulty == difficulty)
        #
        # total = query.count()
        # questions = query.offset((page - 1) * page_size).limit(page_size).all()
        # return questions, total
        pass

    @staticmethod
    def get_recommend_questions(
        user_id: str,
        university: Optional[str] = None,
        major: Optional[str] = None,
        previous_questions: Optional[List[str]] = None,
        count: int = 10
    ) -> List[Question]:
        """获取推荐题目"""
        # 伪代码：实际实现使用推荐算法
        # 1. 根据用户目标院校/专业筛选
        # 2. 使用向量搜索找到相似题目
        # 3. 排除已答题目
        # 4. 根据用户历史表现调整难度
        pass

    @staticmethod
    def get_next_question(
        user_id: str,
        university: Optional[str] = None,
        major: Optional[str] = None,
        previous_questions: Optional[List[str]] = None,
        question_count: int = 0
    ) -> Optional[Question]:
        """获取下一道题目"""
        # 伪代码：实际实现使用题目推荐算法
        # 1. 根据练习次数选择题类
        # 2. 根据用户水平选择难度
        # 3. 排除已答题目
        # 4. 返回推荐题目
        pass

    @staticmethod
    def create(question: Question) -> Question:
        """创建题目"""
        # 伪代码：实际实现使用数据库插入
        # session.add(question)
        # session.commit()
        # session.refresh(question)
        return question

    @staticmethod
    def update(question: Question) -> Question:
        """更新题目"""
        # 伪代码：实际实现使用数据库更新
        # session.merge(question)
        # session.commit()
        return question