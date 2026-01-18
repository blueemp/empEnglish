# 练习模型伪代码
# 文件路径: models/practice.py

from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Text, DateTime, DECIMAL, JSON, ForeignKey, SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# 练习模式枚举
class PracticeMode(str, Enum):
    GENERAL = "general"
    UNIVERSITY = "university"


# 压力等级枚举
class PressureLevel(int, Enum):
    GENTLE = 1  # 温和鼓励型
    NORMAL = 2  # 正常严谨型
    HIGH = 3  # 高压盘问型


# 会话状态枚举
class SessionStatus(str, Enum):
    ONGOING = "ongoing"
    COMPLETED = "completed"
    ABORTED = "aborted"


class PracticeSession(Base):
    """练习会话数据库模型"""
    __tablename__ = "practice_sessions"

    id = Column(String(64), primary_key=True, comment="会话ID，UUID")
    user_id = Column(String(64), ForeignKey("users.id"), nullable=False, comment="用户ID")
    mode = Column(SQLEnum(PracticeMode), nullable=False, comment="练习模式")
    pressure_level = Column(Integer, default=2, comment="压力等级：1-3")
    university = Column(String(100), comment="目标院校")
    major = Column(String(100), comment="目标专业")
    tutor_style_id = Column(String(64), ForeignKey("tutor_styles.id"), comment="导师风格ID")
    status = Column(SQLEnum(SessionStatus), default=SessionStatus.ONGOING, comment="状态")
    question_count = Column(Integer, default=0, comment="已答题目数")
    max_questions = Column(Integer, default=10, comment="最大题目数")
    start_time = Column(DateTime, default=datetime.utcnow, comment="开始时间")
    end_time = Column(DateTime, comment="结束时间")
    duration = Column(Integer, comment="持续时间（秒）")
    overall_score = Column(DECIMAL(5, 2), comment="综合得分")
    report_id = Column(String(64), comment="报告ID")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # 关系
    user = relationship("User", back_populates="sessions")
    tutor_style = relationship("TutorStyle", back_populates="sessions")
    turns = relationship("PracticeTurn", back_populates="session", cascade="all, delete-orphan")

    @classmethod
    def create(cls, **kwargs):
        """创建会话"""
        session = cls(**kwargs)
        return session

    def increment_question(self):
        """增加题目计数"""
        self.question_count += 1

    def is_finished(self):
        """检查是否完成"""
        return self.question_count >= self.max_questions

    def complete(self):
        """完成会话"""
        self.status = SessionStatus.COMPLETED
        self.end_time = datetime.utcnow()
        self.duration = int((self.end_time - self.start_time).total_seconds())

    def abort(self):
        """中止会话"""
        self.status = SessionStatus.ABORTED
        self.end_time = datetime.utcnow()
        self.duration = int((self.end_time - self.start_time).total_seconds())


class PracticeTurn(Base):
    """练习轮次数据库模型"""
    __tablename__ = "practice_turns"

    id = Column(String(64), primary_key=True, comment="轮次ID，UUID")
    session_id = Column(String(64), ForeignKey("practice_sessions.id"), nullable=False, comment="会话ID")
    turn_number = Column(Integer, nullable=False, comment="轮次序号")
    question_id = Column(String(64), ForeignKey("questions.id"), nullable=False, comment="题目ID")
    question = Column(Text, nullable=False, comment="题目内容")
    user_answer_audio_url = Column(String(500), comment="用户回答音频URL")
    user_answer_text = Column(Text, comment="用户回答文本")
    asr_result = Column(Text, comment="ASR转写结果")
    pronunciation_score = Column(DECIMAL(5, 2), comment="发音得分")
    fluency_score = Column(DECIMAL(5, 2), comment="流利度得分")
    vocabulary_score = Column(DECIMAL(5, 2), comment="词汇得分")
    grammar_score = Column(DECIMAL(5, 2), comment="语法得分")
    university_match_score = Column(DECIMAL(5, 2), comment="院校匹配度得分")
    overall_score = Column(DECIMAL(5, 2), comment="综合得分")
    feedback = Column(Text, comment="反馈内容")
    feedback_audio_url = Column(String(500), comment="反馈音频URL")
    follow_up_questions = Column(JSON, comment="追问列表")
    is_recommended = Column(Boolean, default=False, comment="是否推荐重练")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    # 关系
    session = relationship("PracticeSession", back_populates="turns")
    question = relationship("Question", back_populates="turns")

    @classmethod
    def create(cls, **kwargs):
        """创建轮次"""
        turn = cls(**kwargs)
        return turn

    def update_score(self, score_data: dict):
        """更新评分"""
        self.overall_score = score_data.get("overall_score")
        self.pronunciation_score = score_data.get("pronunciation_score")
        self.fluency_score = score_data.get("fluency_score")
        self.vocabulary_score = score_data.get("vocabulary_score")
        self.grammar_score = score_data.get("grammar_score")
        self.university_match_score = score_data.get("university_match_score")


class SessionCreate(BaseModel):
    """会话创建DTO"""
    mode: PracticeMode
    pressure_level: int = 2
    university: Optional[str] = None
    major: Optional[str] = None
    tutor_style_id: Optional[str] = None
    max_questions: int = 10


class SessionResponse(BaseModel):
    """会话响应DTO"""
    id: str
    user_id: str
    mode: PracticeMode
    pressure_level: int
    university: Optional[str]
    major: Optional[str]
    status: SessionStatus
    question_count: int
    max_questions: int
    start_time: datetime
    end_time: Optional[datetime]
    duration: Optional[int]
    overall_score: Optional[float]
    report_id: Optional[str]

    class Config:
        from_attributes = True


class TurnResponse(BaseModel):
    """轮次响应DTO"""
    id: str
    session_id: str
    turn_number: int
    question: str
    overall_score: Optional[float]
    pronunciation_score: Optional[float]
    fluency_score: Optional[float]
    vocabulary_score: Optional[float]
    grammar_score: Optional[float]
    university_match_score: Optional[float]
    feedback: Optional[str]
    follow_up_questions: Optional[List[str]]
    created_at: datetime

    class Config:
        from_attributes = True


class PracticeRepository:
    """练习数据访问层"""

    @staticmethod
    def get_session_by_id(session_id: str) -> Optional[PracticeSession]:
        """根据ID获取会话"""
        # 伪代码：实际实现使用数据库查询
        # return session.query(PracticeSession).filter(PracticeSession.id == session_id).first()
        pass

    @staticmethod
    def create_session(session: PracticeSession) -> PracticeSession:
        """创建会话"""
        # 伪代码：实际实现使用数据库插入
        # session.add(session)
        # session.commit()
        # session.refresh(session)
        return session

    @staticmethod
    def update_session(session: PracticeSession) -> PracticeSession:
        """更新会话"""
        # 伪代码：实际实现使用数据库更新
        # session.merge(session)
        # session.commit()
        return session

    @staticmethod
    def create_turn(turn: PracticeTurn) -> PracticeTurn:
        """创建轮次"""
        # 伪代码：实际实现使用数据库插入
        # session.add(turn)
        # session.commit()
        # session.refresh(turn)
        return turn

    @staticmethod
    def update_turn(turn: PracticeTurn) -> PracticeTurn:
        """更新轮次"""
        # 伪代码：实际实现使用数据库更新
        # session.merge(turn)
        # session.commit()
        return turn

    @staticmethod
    def list_sessions(
        user_id: str,
        mode: Optional[PracticeMode] = None,
        status: Optional[SessionStatus] = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[List[PracticeSession], int]:
        """获取会话列表"""
        # 伪代码：实际实现使用数据库查询
        pass

    @staticmethod
    def get_active_session(user_id: str) -> Optional[PracticeSession]:
        """获取用户活跃会话"""
        # 伪代码：实际实现使用数据库查询
        # return session.query(PracticeSession).filter(
        #     PracticeSession.user_id == user_id,
        #     PracticeSession.status == SessionStatus.ONGOING
        # ).first()
        pass