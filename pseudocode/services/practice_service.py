# 练习服务伪代码
# 文件路径: services/practice_service.py

from typing import Optional, List, Dict, Any
from datetime import datetime
from models.practice import (
    PracticeSession, PracticeTurn,
    SessionCreate, SessionResponse, TurnResponse,
    PracticeMode, PressureLevel, SessionStatus, PracticeRepository
)
from models.user import User, UserRepository
from models.question import Question, QuestionRepository
from models.tutor_style import TutorStyle, TutorStyleRepository
from services.question_service import QuestionService, QuestionCategoryManager
from services.scoring_service import ScoringService
from ai.asr_service import ASRService
from ai.tts_service import TTSService
from ai.llm_service import LLMService


class PracticeService:
    """练习服务"""

    def __init__(
        self,
        question_service: QuestionService,
        scoring_service: ScoringService,
        asr_service: ASRService,
        tts_service: TTSService,
        llm_service: LLMService
    ):
        self.question_service = question_service
        self.scoring_service = scoring_service
        self.asr_service = asr_service
        self.tts_service = tts_service
        self.llm_service = llm_service

    def create_session(self, user_id: str, session_data: SessionCreate) -> Dict[str, Any]:
        """
        创建练习会话
        """
        # 1. 验证用户权限
        user = UserRepository.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        if session_data.mode == PracticeMode.UNIVERSITY and not user.is_premium():
            raise ValueError("Premium subscription required for university mode")

        # 2. 获取导师风格
        tutor_style = None
        if session_data.tutor_style_id:
            tutor_style = TutorStyleRepository.get_by_id(session_data.tutor_style_id)

        # 3. 创建会话
        session = PracticeSession.create(
            user_id=user_id,
            mode=session_data.mode,
            pressure_level=session_data.pressure_level,
            university=session_data.university,
            major=session_data.major,
            tutor_style_id=session_data.tutor_style_id,
            max_questions=session_data.max_questions
        )
        PracticeRepository.create_session(session)

        # 4. 生成第一道题目
        first_question = self.question_service.get_next_question(
            user_id=user_id,
            university=session_data.university,
            major=session_data.major,
            question_count=0
        )

        if first_question is None:
            raise ValueError("No questions available")

        # 5. 合成题目语音
        question_audio_url = self.tts_service.synthesize(
            text=first_question.content,
            style="academic"
        )

        # 6. 返回会话信息
        return {
            "session_id": session.id,
            "mode": session.mode,
            "pressure_level": session.pressure_level,
            "university": session.university,
            "major": session.major,
            "tutor_style": {
                "id": tutor_style.id if tutor_style else None,
                "name": tutor_style.name if tutor_style else None
            },
            "first_question": {
                "id": first_question.id,
                "content": first_question.content,
                "audio_url": question_audio_url
            },
            "websocket_url": f"wss://api.empenglish.com/api/v1/practice/sessions/{session.id}/ws"
        }

    def submit_answer(
        self,
        session_id: str,
        turn_id: str,
        audio_url: str,
        duration: int
    ) -> Dict[str, Any]:
        """
        提交答案
        """
        # 1. 获取会话和轮次
        session = PracticeRepository.get_session_by_id(session_id)
        if session is None:
            raise ValueError("Session not found")

        if session.status != SessionStatus.ONGOING:
            raise ValueError("Session is not ongoing")

        # 2. ASR转写
        asr_result = self.asr_service.transcribe(audio_url=audio_url)

        # 3. 获取题目
        turn = PracticeRepository.get_turn_by_id(turn_id)
        if turn is None:
            raise ValueError("Turn not found")

        # 4. 评分
        score_result = self.scoring_service.evaluate(
            question=turn.question,
            answer=asr_result["text"],
            audio_url=audio_url,
            university=session.university,
            major=session.major
        )

        # 5. 生成反馈
        feedback = self.llm_service.generate_feedback(
            question=turn.question,
            answer=asr_result["text"],
            score=score_result
        )

        # 6. 合成反馈语音
        feedback_audio_url = self.tts_service.synthesize(
            text=feedback,
            style=self._get_tts_style(session.pressure_level)
        )

        # 7. 生成追问
        follow_up_questions = self.llm_service.generate_follow_up(
            question=turn.question,
            answer=asr_result["text"],
            pressure_level=session.pressure_level,
            tutor_style_id=session.tutor_style_id
        )

        # 8. 更新轮次
        turn.update_score(score_result)
        turn.user_answer_text = asr_result["text"]
        turn.asr_result = asr_result["text"]
        turn.feedback = feedback
        turn.feedback_audio_url = feedback_audio_url
        turn.follow_up_questions = follow_up_questions
        PracticeRepository.update_turn(turn)

        # 9. 更新会话
        session.increment_question()
        PracticeRepository.update_session(session)

        # 10. 检查是否完成
        if session.is_finished():
            self._complete_session(session_id)

        # 11. 返回结果
        return {
            "turn_id": turn_id,
            "score": score_result,
            "feedback": {
                "text": feedback,
                "audio_url": feedback_audio_url
            },
            "follow_up_questions": follow_up_questions,
            "is_finished": session.is_finished()
        }

    def get_next_question(self, session_id: str) -> Dict[str, Any]:
        """
        获取下一道题目
        """
        # 1. 获取会话
        session = PracticeRepository.get_session_by_id(session_id)
        if session is None:
            raise ValueError("Session not found")

        # 2. 获取历史题目
        turns = PracticeRepository.get_turns_by_session(session_id)
        previous_questions = [turn.question_id for turn in turns]

        # 3. 生成下一道题目
        next_question = self.question_service.get_next_question(
            user_id=session.user_id,
            university=session.university,
            major=session.major,
            previous_questions=previous_questions,
            question_count=session.question_count
        )

        if next_question is None:
            return None

        # 4. 合成语音
        question_audio_url = self.tts_service.synthesize(
            text=next_question.content,
            style=self._get_tts_style(session.pressure_level)
        )

        # 5. 创建新轮次
        turn = PracticeTurn.create(
            session_id=session_id,
            turn_number=session.question_count + 1,
            question_id=next_question.id,
            question=next_question.content
        )
        PracticeRepository.create_turn(turn)

        return {
            "turn_id": turn.id,
            "question": {
                "id": next_question.id,
                "content": next_question.content,
                "audio_url": question_audio_url
            }
        }

    def get_session(self, session_id: str) -> SessionResponse:
        """
        获取会话详情
        """
        session = PracticeRepository.get_session_by_id(session_id)
        if session is None:
            raise ValueError("Session not found")
        return SessionResponse.model_validate(session)

    def list_sessions(
        self,
        user_id: str,
        mode: Optional[PracticeMode] = None,
        status: Optional[SessionStatus] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        获取会话列表
        """
        sessions, total = PracticeRepository.list_sessions(
            user_id=user_id,
            mode=mode,
            status=status,
            page=page,
            page_size=page_size
        )

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "sessions": [SessionResponse.model_validate(s) for s in sessions]
        }

    def abort_session(self, session_id: str):
        """
        中止会话
        """
        session = PracticeRepository.get_session_by_id(session_id)
        if session is None:
            raise ValueError("Session not found")

        session.abort()
        PracticeRepository.update_session(session)

    def _complete_session(self, session_id: str):
        """
        完成会话
        """
        session = PracticeRepository.get_session_by_id(session_id)
        if session is None:
            raise ValueError("Session not found")

        # 1. 计算综合得分
        turns = PracticeRepository.get_turns_by_session(session_id)
        scores = [turn.overall_score for turn in turns if turn.overall_score is not None]
        overall_score = sum(scores) / len(scores) if scores else 0

        # 2. 完成会话
        session.complete()
        session.overall_score = overall_score
        PracticeRepository.update_session(session)

        # 3. 生成报告
        from services.report_service import ReportService
        report_service = ReportService(self.scoring_service)
        report_service.generate_report(session_id)

    def _get_tts_style(self, pressure_level: int) -> str:
        """
        获取TTS风格
        """
        style_map = {
            1: "friendly",
            2: "academic",
            3: "high_pressure"
        }
        return style_map.get(pressure_level, "academic")


class WebSocketPracticeHandler:
    """WebSocket练习处理器"""

    def __init__(self, practice_service: PracticeService):
        self.practice_service = practice_service

    async def handle_message(self, session_id: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理WebSocket消息
        """
        message_type = message.get("type")

        if message_type == "answer":
            # 处理答案提交
            return self.practice_service.submit_answer(
                session_id=session_id,
                turn_id=message["turn_id"],
                audio_url=message["audio_url"],
                duration=message["duration"]
            )
        elif message_type == "next_question":
            # 获取下一题
            return self.practice_service.get_next_question(session_id=session_id)
        elif message_type == "abort":
            # 中止会话
            self.practice_service.abort_session(session_id=session_id)
            return {"type": "session_aborted", "session_id": session_id}
        else:
            raise ValueError(f"Unknown message type: {message_type}")

    async def send_question(self, session_id: str, websocket):
        """
        发送题目
        """
        question_data = self.practice_service.get_next_question(session_id)
        if question_data:
            await websocket.send_json({
                "type": "question",
                **question_data
            })

    async def send_score(self, score_data: Dict[str, Any], websocket):
        """
        发送评分结果
        """
        await websocket.send_json({
            "type": "score",
            **score_data
        })

    async def send_session_end(self, session_id: str, report_id: str, websocket):
        """
        发送会话结束
        """
        session = self.practice_service.get_session(session_id)

        await websocket.send_json({
            "type": "session_end",
            "session_id": session_id,
            "report_id": report_id,
            "overall_score": session.overall_score,
            "statistics": {
                "total_turns": session.question_count,
                "total_duration": session.duration
            }
        })