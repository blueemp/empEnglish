"""Questions router."""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class QuestionListResponse(BaseModel):
    """Question list response."""

    total: int
    page: int
    page_size: int
    questions: list


class QuestionDetailResponse(BaseModel):
    """Question detail response."""

    id: str
    type: str
    university: Optional[str]
    major: Optional[str]
    category: str
    difficulty: int
    content: str
    reference_answer: Optional[str]
    is_premium: bool


class RecommendationResponse(BaseModel):
    """Question recommendation response."""

    id: str
    type: str
    university: Optional[str]
    major: Optional[str]
    category: str
    difficulty: int
    content: str
    match_score: float
    reason: str


@router.get("", response_model=QuestionListResponse)
async def list_questions(
    page: int = 1,
    page_size: int = 20,
    category: Optional[str] = None,
    university: Optional[str] = None,
    major: Optional[str] = None,
):
    """
    List questions with pagination and filtering.
    """
    # TODO: Implement actual database query
    # For now, return mock data
    return QuestionListResponse(
        total=100,
        page=page,
        page_size=page_size,
        questions=[
            {
                "id": f"q{i}",
                "type": "general",
                "university": None,
                "major": None,
                "category": "introduction",
                "difficulty": 3,
                "content": f"Question {i} about introduction",
                "reference_answer": "Sample answer for introduction",
                "is_premium": False,
            }
            for i in range(page_size)
        ],
    )


@router.get("/{question_id}", response_model=QuestionDetailResponse)
async def get_question_by_id(question_id: str):
    """
    Get question details by ID.
    """
    # TODO: Implement database lookup
    if question_id == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )

    return QuestionDetailResponse(
        id=question_id,
        type="general",
        university=None,
        major=None,
        category="introduction",
        difficulty=3,
        content="Tell me about yourself.",
        reference_answer="My name is [your name]. I'm a student from [university].",
        is_premium=False,
    )


@router.get("/recommendations", response_model=list[RecommendationResponse])
async def get_recommendations():
    """
    Get recommended questions for user.

    Requires authentication.
    """
    # TODO: Implement recommendation algorithm
    return [
        RecommendationResponse(
            id="rec1",
            type="university",
            university="西安交通大学",
            major="计算机科学与技术",
            category="education",
            difficulty=4,
            content="Why did you choose this major?",
            match_score=0.95,
            reason="与你的目标院校和专业高度相关",
        ),
        RecommendationResponse(
            id="rec2",
            type="general",
            university=None,
            major=None,
            category="research",
            difficulty=3,
            content="Describe your research experience.",
            match_score=0.6,
            reason="适合你的当前水平",
        ),
    ]
