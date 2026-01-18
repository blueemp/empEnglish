# Agent服务伪代码
# 文件路径: ai/agent_service.py

from typing import Dict, Any, List, Optional, TypedDict
from langgraph.graph import StateGraph, END
from services.question_service import QuestionService
from services.scoring_service import ScoringService
from ai.asr_service import ASRService
from ai.tts_service import TTSService
from ai.llm_service import LLMService


class InterviewState(TypedDict):
    """面试状态"""
    user_id: str
    session_id: str
    university: Optional[str]
    major: Optional[str]
    pressure_level: int
    tutor_style_id: Optional[str]

    # 当前轮次
    current_question: Optional[str]
    current_question_id: Optional[str]
    user_answer: Optional[str]
    user_answer_audio_url: Optional[str]

    # 评分结果
    score: Optional[Dict[str, Any]]
    feedback: Optional[str]
    feedback_audio_url: Optional[str]

    # 追问
    follow_up_questions: List[str]

    # 对话历史
    conversation_history: List[Dict[str, Any]]

    # 统计
    question_count: int
    max_questions: int

    # 状态
    is_finished: bool

    # 报告
    report: Optional[Dict[str, Any]]


class InterviewAgent:
    """面试Agent"""

    def __init__(
        self,
        question_service: QuestionService,
        scoring_service: ScoringService,
        asr_service: ASRService,
        tts_service: TTSService,
        llm_service: LLMService
    ):
        """
        初始化面试Agent

        Args:
            question_service: 题库服务
            scoring_service: 评分服务
            asr_service: ASR服务
            tts_service: TTS服务
            llm_service: LLM服务
        """
        self.question_service = question_service
        self.scoring_service = scoring_service
        self.asr_service = asr_service
        self.tts_service = tts_service
        self.llm_service = llm_service

        # 构建工作流
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """
        构建Agent工作流

        Returns:
            工作流图
        """
        graph = StateGraph(InterviewState)

        # 添加节点
        graph.add_node("generate_question", self._generate_question)
        graph.add_node("transcribe_audio", self._transcribe_audio)
        graph.add_node("score_answer", self._score_answer)
        graph.add_node("generate_feedback", self._generate_feedback)
        graph.add_node("synthesize_feedback_audio", self._synthesize_feedback_audio)
        graph.add_node("generate_follow_up", self._generate_follow_up)
        graph.add_node("check_completion", self._check_completion)
        graph.add_node("generate_report", self._generate_report)

        # 添加边
        graph.set_entry_point("generate_question")
        graph.add_edge("generate_question", "transcribe_audio")
        graph.add_edge("transcribe_audio", "score_answer")
        graph.add_edge("score_answer", "generate_feedback")
        graph.add_edge("generate_feedback", "synthesize_feedback_audio")
        graph.add_edge("synthesize_feedback_audio", "generate_follow_up")
        graph.add_edge("generate_follow_up", "check_completion")

        # 条件边
        graph.add_conditional_edges(
            "check_completion",
            self._should_continue,
            {
                "continue": "generate_question",
                "end": "generate_report"
            }
        )
        graph.add_edge("generate_report", END)

        return graph.compile()

    def _generate_question(self, state: InterviewState) -> InterviewState:
        """
        生成题目节点

        Args:
            state: 当前状态

        Returns:
            更新后的状态
        """
        # 获取题目
        question = self.question_service.get_next_question(
            user_id=state["user_id"],
            university=state["university"],
            major=state["major"],
            previous_questions=[t["question"] for t in state["conversation_history"]],
            question_count=state["question_count"]
        )

        # 更新状态
        state["current_question"] = question.content
        state["current_question_id"] = question.id

        # 添加到历史
        state["conversation_history"].append({
            "turn_id": len(state["conversation_history"]) + 1,
            "question": question.content,
            "question_id": question.id,
            "answer": None,
            "score": None
        })

        return state

    def _transcribe_audio(self, state: InterviewState) -> InterviewState:
        """
        语音转写节点

        Args:
            state: 当前状态

        Returns:
            更新后的状态
        """
        if state["user_answer_audio_url"]:
            # 调用ASR服务
            result = self.asr_service.transcribe(
                audio_url=state["user_answer_audio_url"],
                language="en"
            )
            state["user_answer"] = result["text"]

        return state

    def _score_answer(self, state: InterviewState) -> InterviewState:
        """
        评分节点

        Args:
            state: 当前状态

        Returns:
            更新后的状态
        """
        # 调用评分服务
        score_result = self.scoring_service.evaluate(
            question=state["current_question"],
            answer=state["user_answer"],
            audio_url=state["user_answer_audio_url"],
            university=state["university"],
            major=state["major"]
        )

        state["score"] = score_result

        # 更新历史
        state["conversation_history"][-1]["answer"] = state["user_answer"]
        state["conversation_history"][-1]["score"] = score_result

        return state

    def _generate_feedback(self, state: InterviewState) -> InterviewState:
        """
        生成反馈节点

        Args:
            state: 当前状态

        Returns:
            更新后的状态
        """
        # 使用LLM生成反馈
        feedback = self.llm_service.generate_feedback(
            question=state["current_question"],
            answer=state["user_answer"],
            score=state["score"]
        )

        state["feedback"] = feedback

        return state

    def _synthesize_feedback_audio(self, state: InterviewState) -> InterviewState:
        """
        合成反馈语音节点

        Args:
            state: 当前状态

        Returns:
            更新后的状态
        """
        if state["feedback"]:
            # 根据压力等级选择风格
            style = self._get_tts_style(state["pressure_level"])

            audio_url = self.tts_service.synthesize(
                text=state["feedback"],
                style=style
            )

            state["feedback_audio_url"] = audio_url

        return state

    def _generate_follow_up(self, state: InterviewState) -> InterviewState:
        """
        生成追问节点

        Args:
            state: 当前状态

        Returns:
            更新后的状态
        """
        # 使用LLM生成追问
        follow_up = self.llm_service.generate_follow_up(
            question=state["current_question"],
            answer=state["user_answer"],
            pressure_level=state["pressure_level"],
            tutor_style_id=state["tutor_style_id"]
        )

        state["follow_up_questions"] = follow_up

        return state

    def _check_completion(self, state: InterviewState) -> InterviewState:
        """
        检查完成节点

        Args:
            state: 当前状态

        Returns:
            更新后的状态
        """
        state["question_count"] += 1

        if state["question_count"] >= state["max_questions"]:
            state["is_finished"] = True
        else:
            state["is_finished"] = False

        return state

    def _should_continue(self, state: InterviewState) -> str:
        """
        决定是否继续

        Args:
            state: 当前状态

        Returns:
            下一步动作
        """
        if state["is_finished"]:
            return "end"
        else:
            return "continue"

    def _generate_report(self, state: InterviewState) -> InterviewState:
        """
        生成报告节点

        Args:
            state: 当前状态

        Returns:
            更新后的状态
        """
        # 汇总所有评分
        scores = [turn["score"] for turn in state["conversation_history"] if turn["score"]]

        overall_score = sum(s["overall_score"] for s in scores) / len(scores) if scores else 0

        # 生成报告
        report = {
            "session_id": state["session_id"],
            "overall_score": overall_score,
            "conversation_history": state["conversation_history"],
            "suggestions": [s["suggestions"] for s in scores if "suggestions" in s]
        }

        state["report"] = report

        return state

    def _get_tts_style(self, pressure_level: int) -> str:
        """
        获取TTS风格

        Args:
            pressure_level: 压力等级

        Returns:
            TTS风格
        """
        style_map = {
            1: "friendly",
            2: "academic",
            3: "high_pressure"
        }
        return style_map.get(pressure_level, "academic")

    def run(self, initial_state: InterviewState) -> InterviewState:
        """
        运行Agent

        Args:
            initial_state: 初始状态

        Returns:
            最终状态
        """
        return self.graph.invoke(initial_state)

    def run_step(self, state: InterviewState, action: str) -> InterviewState:
        """
        运行单步

        Args:
            state: 当前状态
            action: 动作类型

        Returns:
            更新后的状态
        """
        if action == "generate_question":
            return self._generate_question(state)
        elif action == "transcribe_audio":
            return self._transcribe_audio(state)
        elif action == "score_answer":
            return self._score_answer(state)
        elif action == "generate_feedback":
            return self._generate_feedback(state)
        elif action == "synthesize_feedback_audio":
            return self._synthesize_feedback_audio(state)
        elif action == "generate_follow_up":
            return self._generate_follow_up(state)
        elif action == "check_completion":
            return self._check_completion(state)
        elif action == "generate_report":
            return self._generate_report(state)
        else:
            return state


class AgentFactory:
    """Agent工厂"""

    @staticmethod
    def create_interview_agent(
        question_service: QuestionService,
        scoring_service: ScoringService,
        asr_service: ASRService,
        tts_service: TTSService,
        llm_service: LLMService
    ) -> InterviewAgent:
        """
        创建面试Agent

        Args:
            question_service: 题库服务
            scoring_service: 评分服务
            asr_service: ASR服务
            tts_service: TTS服务
            llm_service: LLM服务

        Returns:
            面试Agent
        """
        return InterviewAgent(
            question_service=question_service,
            scoring_service=scoring_service,
            asr_service=asr_service,
            tts_service=tts_service,
            llm_service=llm_service
        )

    @staticmethod
    def create_initial_state(
        user_id: str,
        session_id: str,
        university: Optional[str] = None,
        major: Optional[str] = None,
        pressure_level: int = 2,
        tutor_style_id: Optional[str] = None,
        max_questions: int = 10
    ) -> InterviewState:
        """
        创建初始状态

        Args:
            user_id: 用户ID
            session_id: 会话ID
            university: 院校
            major: 专业
            pressure_level: 压力等级
            tutor_style_id: 导师风格ID
            max_questions: 最大题目数

        Returns:
            初始状态
        """
        return {
            "user_id": user_id,
            "session_id": session_id,
            "university": university,
            "major": major,
            "pressure_level": pressure_level,
            "tutor_style_id": tutor_style_id,
            "current_question": None,
            "current_question_id": None,
            "user_answer": None,
            "user_answer_audio_url": None,
            "score": None,
            "feedback": None,
            "feedback_audio_url": None,
            "follow_up_questions": [],
            "conversation_history": [],
            "question_count": 0,
            "max_questions": max_questions,
            "is_finished": False,
            "report": None
        }