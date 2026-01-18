# 评分模型伪代码
# 文件路径: models/scoring.py

from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DECIMAL, JSON, ForeignKey, SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# 评分维度枚举
class ScoreDimension(str, Enum):
    PRONUNCIATION = "pronunciation"
    FLUENCY = "fluency"
    VOCABULARY = "vocabulary"
    GRAMMAR = "grammar"
    UNIVERSITY_MATCH = "university_match"


class ScoringRecord(Base):
    """评分记录数据库模型"""
    __tablename__ = "scoring_records"

    id = Column(String(64), primary_key=True, comment="评分记录ID，UUID")
    turn_id = Column(String(64), ForeignKey("practice_turns.id"), nullable=False, comment="轮次ID")
    user_id = Column(String(64), ForeignKey("users.id"), nullable=False, comment="用户ID")
    dimension = Column(SQLEnum(ScoreDimension), nullable=False, comment="评分维度")
    score = Column(DECIMAL(5, 2), nullable=False, comment="得分")
    details = Column(JSON, comment="评分详情")
    suggestions = Column(JSON, comment="建议列表")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    # 关系
    turn = relationship("PracticeTurn", back_populates="scoring_records")
    user = relationship("User", back_populates="scoring_records")

    @classmethod
    def create(cls, **kwargs):
        """创建评分记录"""
        record = cls(**kwargs)
        return record


class PhonemeError(Base):
    """发音错误数据库模型"""
    __tablename__ = "phoneme_errors"

    id = Column(String(64), primary_key=True, comment="错误ID，UUID")
    turn_id = Column(String(64), ForeignKey("practice_turns.id"), nullable=False, comment="轮次ID")
    word = Column(String(50), nullable=False, comment="单词")
    correct_phoneme = Column(String(20), comment="正确音素")
    actual_phoneme = Column(String(20), comment="实际音素")
    position = Column(Integer, comment="位置")
    score = Column(DECIMAL(5, 2), comment="得分")
    suggestion = Column(String(200), comment="建议")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    # 关系
    turn = relationship("PracticeTurn", back_populates="phoneme_errors")

    @classmethod
    def create(cls, **kwargs):
        """创建发音错误记录"""
        error = cls(**kwargs)
        return error


class ScoreDetails(BaseModel):
    """评分详情DTO"""
    overall_score: float
    dimensions: dict
    feedback: str
    suggestions: List[str]


class PronunciationDetails(BaseModel):
    """发音评分详情DTO"""
    score: float
    word_scores: List[dict]
    common_errors: List[dict]


class FluencyDetails(BaseModel):
    """流利度评分详情DTO"""
    score: float
    speech_rate: float
    avg_speech_length: float
    pause_frequency: float
    pauses: List[dict]


class VocabularyDetails(BaseModel):
    """词汇评分详情DTO"""
    score: float
    diversity: float
    advanced_words: List[str]
    word_count: int


class GrammarDetails(BaseModel):
    """语法评分详情DTO"""
    score: float
    errors: List[dict]
    sentence_variety: float


class UniversityMatchDetails(BaseModel):
    """院校匹配度评分详情DTO"""
    score: float
    relevance: float
    professional_terms: List[str]
    suggestions: List[str]


class ScoringRepository:
    """评分数据访问层"""

    @staticmethod
    def create_record(record: ScoringRecord) -> ScoringRecord:
        """创建评分记录"""
        # 伪代码：实际实现使用数据库插入
        # session.add(record)
        # session.commit()
        # session.refresh(record)
        return record

    @staticmethod
    def create_phoneme_error(error: PhonemeError) -> PhonemeError:
        """创建发音错误记录"""
        # 伪代码：实际实现使用数据库插入
        # session.add(error)
        # session.commit()
        # session.refresh(error)
        return error

    @staticmethod
    def get_records_by_turn(turn_id: str) -> List[ScoringRecord]:
        """获取轮次的评分记录"""
        # 伪代码：实际实现使用数据库查询
        # return session.query(ScoringRecord).filter(
        #     ScoringRecord.turn_id == turn_id
        # ).all()
        pass

    @staticmethod
    def get_phoneme_errors_by_turn(turn_id: str) -> List[PhonemeError]:
        """获取轮次的发音错误"""
        # 伪代码：实际实现使用数据库查询
        # return session.query(PhonemeError).filter(
        #     PhonemeError.turn_id == turn_id
        # ).all()
        pass

    @staticmethod
    def get_user_score_history(
        user_id: str,
        dimension: Optional[ScoreDimension] = None,
        days: int = 30
    ) -> List[dict]:
        """获取用户评分历史"""
        # 伪代码：实际实现使用数据库查询
        pass