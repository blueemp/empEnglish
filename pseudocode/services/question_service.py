# 题库服务伪代码
# 文件路径: services/question_service.py

from typing import Optional, List, Dict, Any
from models.question import (
    Question, QuestionCreate, QuestionResponse, QuestionRecommend,
    QuestionType, QuestionCategory, QuestionRepository
)


class QuestionService:
    """题库服务"""

    def __init__(self):
        pass

    def get_question_by_id(self, question_id: str) -> QuestionResponse:
        """
        根据ID获取题目
        """
        question = QuestionRepository.get_by_id(question_id)
        if question is None:
            raise ValueError("Question not found")
        return QuestionResponse.model_validate(question)

    def list_questions(
        self,
        type: Optional[QuestionType] = None,
        university: Optional[str] = None,
        major: Optional[str] = None,
        category: Optional[QuestionCategory] = None,
        difficulty: Optional[int] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        获取题目列表
        """
        questions, total = QuestionRepository.list_questions(
            type=type,
            university=university,
            major=major,
            category=category,
            difficulty=difficulty,
            page=page,
            page_size=page_size
        )

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "questions": [QuestionResponse.model_validate(q) for q in questions]
        }

    def get_recommend_questions(
        self,
        user_id: str,
        university: Optional[str] = None,
        major: Optional[str] = None,
        previous_questions: Optional[List[str]] = None,
        count: int = 10
    ) -> List[QuestionRecommend]:
        """
        获取推荐题目
        """
        questions = QuestionRepository.get_recommend_questions(
            user_id=user_id,
            university=university,
            major=major,
            previous_questions=previous_questions,
            count=count
        )

        # 生成推荐信息
        recommendations = []
        for question in questions:
            match_score = self._calculate_match_score(question, university, major)
            reason = self._generate_recommendation_reason(question, match_score)

            recommendations.append(QuestionRecommend(
                id=question.id,
                type=question.type,
                university=question.university,
                major=question.major,
                category=question.category,
                difficulty=question.difficulty,
                content=question.content,
                match_score=match_score,
                reason=reason
            ))

        return recommendations

    def get_next_question(
        self,
        user_id: str,
        university: Optional[str] = None,
        major: Optional[str] = None,
        previous_questions: Optional[List[str]] = None,
        question_count: int = 0
    ) -> Optional[QuestionResponse]:
        """
        获取下一道题目
        """
        question = QuestionRepository.get_next_question(
            user_id=user_id,
            university=university,
            major=major,
            previous_questions=previous_questions,
            question_count=question_count
        )

        if question is None:
            return None

        return QuestionResponse.model_validate(question)

    def create_question(self, question_data: QuestionCreate, created_by: str) -> QuestionResponse:
        """
        创建题目（管理员）
        """
        question = Question.create(**question_data.model_dump(), created_by=created_by)
        QuestionRepository.create(question)
        return QuestionResponse.model_validate(question)

    def update_question(self, question_id: str, question_data: QuestionCreate) -> QuestionResponse:
        """
        更新题目（管理员）
        """
        question = QuestionRepository.get_by_id(question_id)
        if question is None:
            raise ValueError("Question not found")

        # 更新字段
        update_dict = question_data.model_dump(exclude_unset=True)
        question.update(**update_dict)

        QuestionRepository.update(question)
        return QuestionResponse.model_validate(question)

    def update_question_usage(self, question_id: str, score: Optional[float] = None):
        """
        更新题目使用统计
        """
        question = QuestionRepository.get_by_id(question_id)
        if question is None:
            raise ValueError("Question not found")

        question.update_usage(score)
        QuestionRepository.update(question)

    def _calculate_match_score(self, question: Question, university: Optional[str], major: Optional[str]) -> float:
        """
        计算匹配度分数
        """
        score = 0.0

        # 院校匹配
        if question.university and university:
            if question.university == university:
                score += 0.5
            else:
                score += 0.1

        # 专业匹配
        if question.major and major:
            if question.major == major:
                score += 0.4
            else:
                score += 0.1

        # 题目类型匹配
        if question.type == QuestionType.UNIVERSITY:
            score += 0.1

        return min(score, 1.0)

    def _generate_recommendation_reason(self, question: Question, match_score: float) -> str:
        """
        生成推荐理由
        """
        if match_score >= 0.9:
            return "与你的目标院校和专业高度相关"
        elif match_score >= 0.7:
            return "与你的目标专业相关"
        elif match_score >= 0.5:
            return "适合你的当前水平"
        else:
            return "通用练习题目"


class QuestionCategoryManager:
    """题类管理器"""

    # 题类顺序（按练习流程）
    CATEGORY_ORDER = [
        QuestionCategory.INTRODUCTION,
        QuestionCategory.FAMILY,
        QuestionCategory.EDUCATION,
        QuestionCategory.RESEARCH,
        QuestionCategory.INTEREST,
        QuestionCategory.MOTIVATION,
        QuestionCategory.CAREER,
        QuestionCategory.GENERAL
    ]

    @classmethod
    def get_next_category(cls, current_category: Optional[QuestionCategory]) -> QuestionCategory:
        """
        获取下一个题类
        """
        if current_category is None:
            return cls.CATEGORY_ORDER[0]

        try:
            index = cls.CATEGORY_ORDER.index(current_category)
            next_index = (index + 1) % len(cls.CATEGORY_ORDER)
            return cls.CATEGORY_ORDER[next_index]
        except ValueError:
            return QuestionCategory.GENERAL

    @classmethod
    def get_category_by_turn(cls, turn_number: int) -> QuestionCategory:
        """
        根据轮次获取题类
        """
        index = turn_number % len(cls.CATEGORY_ORDER)
        return cls.CATEGORY_ORDER[index]