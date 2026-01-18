# 评分服务实现代码
# 文件路径: services/scoring_service.py

from typing import Dict, Any, Optional, List


class ScoringService:
    """评分服务"""

    def __init__(
        self,
        gop_scorer,
        fluency_scorer,
        vocabulary_scorer,
        grammar_scorer,
        university_match_scorer,
    ):
        self.gop_scorer = gop_scorer
        self.fluency_scorer = fluency_scorer
        self.vocabulary_scorer = vocabulary_scorer
        self.grammar_scorer = grammar_scorer
        self.university_match_scorer = university_match_scorer

        self.weights = {
            "pronunciation": 0.25,
            "fluency": 0.25,
            "vocabulary": 0.25,
            "grammar": 0.25,
            "university_match": 0.0,
        }

    def evaluate(
        self,
        question: str,
        answer: str,
        audio_url: str,
        university: Optional[str] = None,
        major: Optional[str] = None,
    ) -> Dict[str, Any]:
        """综合评分"""
        pronunciation_score = self.gop_scorer.calculate_gop_score(audio_url, answer)
        fluency_score = self.fluency_scorer.calculate_fluency_score(audio_url, answer)
        vocabulary_score = self.vocabulary_scorer.calculate_vocabulary_score(answer)
        grammar_score = self.grammar_scorer.calculate_grammar_score(answer)

        university_match_score = None
        if university and major:
            university_match_score = self.university_match_scorer.calculate_match_score(
                answer=answer, university=university, major=major
            )
            self.weights["university_match"] = 0.2
            self.weights["pronunciation"] = 0.2
            self.weights["fluency"] = 0.2
            self.weights["vocabulary"] = 0.2
            self.weights["grammar"] = 0.2

        overall_score = self._calculate_overall_score(
            pronunciation_score["overall_score"],
            fluency_score["overall_score"],
            vocabulary_score["overall_score"],
            grammar_score["overall_score"],
            university_match_score["score"] if university_match_score else None,
        )

        suggestions = self._generate_suggestions(
            pronunciation_score,
            fluency_score,
            vocabulary_score,
            grammar_score,
            university_match_score,
        )

        dimensions = {
            "pronunciation": pronunciation_score,
            "fluency": fluency_score,
            "vocabulary": vocabulary_score,
            "grammar": grammar_score,
        }

        if university_match_score:
            dimensions["university_match"] = university_match_score

        feedback = self._generate_feedback(dimensions, overall_score)

        return {
            "overall_score": overall_score,
            "dimensions": dimensions,
            "feedback": feedback,
            "suggestions": suggestions,
        }

    def evaluate_pronunciation(self, audio_url: str, text: str) -> Dict[str, Any]:
        """发音评分"""
        result = self.gop_scorer.calculate_gop_score(audio_url, text)

        phoneme_errors = []
        for word_score in result["phoneme_scores"]:
            if word_score["score"] < 70:
                phoneme_errors.append(
                    {
                        "word": word_score["phoneme"],
                        "score": word_score["score"],
                        "suggestion": f"Work on pronouncing '{word_score['phoneme']}' more clearly",
                    }
                )

        return {
            "score": result["overall_score"],
            "word_scores": result["phoneme_scores"],
            "common_errors": phoneme_errors,
        }

    def evaluate_fluency(self, audio_url: str, text: str) -> Dict[str, Any]:
        """流利度评分"""
        result = self.fluency_scorer.calculate_fluency_score(audio_url, text)

        return {
            "score": result["overall_score"],
            "speech_rate": result["speech_rate"],
            "avg_speech_length": result["avg_speech_length"],
            "pause_frequency": result["pause_frequency"],
            "pauses": result["pauses"],
        }

    def evaluate_vocabulary(self, text: str) -> Dict[str, Any]:
        """词汇评分"""
        result = self.vocabulary_scorer.calculate_vocabulary_score(text)

        return {
            "score": result["overall_score"],
            "diversity": result["diversity"],
            "advanced_words": result["advanced_words"],
            "word_count": result["word_count"],
        }

    def evaluate_grammar(self, text: str) -> Dict[str, Any]:
        """语法评分"""
        result = self.grammar_scorer.calculate_grammar_score(text)

        return {
            "score": result["overall_score"],
            "errors": result["errors"],
            "sentence_variety": result["sentence_variety"],
        }

    def _calculate_overall_score(
        self,
        pronunciation: float,
        fluency: float,
        vocabulary: float,
        grammar: float,
        university_match: Optional[float] = None,
    ) -> float:
        """计算综合得分"""
        scores = {
            "pronunciation": pronunciation,
            "fluency": fluency,
            "vocabulary": vocabulary,
            "grammar": grammar,
        }

        if university_match is not None:
            scores["university_match"] = university_match

        overall = sum(scores[dim] * self.weights[dim] for dim in scores)
        return round(overall, 2)

    def _generate_suggestions(
        self,
        pronunciation: Dict[str, Any],
        fluency: Dict[str, Any],
        vocabulary: Dict[str, Any],
        grammar: Dict[str, Any],
        university_match: Optional[Dict[str, Any]] = None,
    ) -> List[str]:
        """生成建议"""
        suggestions = []

        if pronunciation["overall_score"] < 80:
            suggestions.append(
                "Practice your pronunciation, especially on difficult sounds"
            )

        if fluency["overall_score"] < 80:
            if fluency["pause_frequency"] > 2:
                suggestions.append("Try to reduce pause frequency by practicing more")
            if fluency["speech_rate"] < 120:
                suggestions.append("Work on increasing your speaking rate slightly")

        if vocabulary["overall_score"] < 80:
            if vocabulary["diversity"] < 50:
                suggestions.append(
                    "Use more varied vocabulary to improve your expression"
                )
            if len(vocabulary["advanced_words"]) < 2:
                suggestions.append("Try to incorporate more advanced vocabulary")

        if grammar["overall_score"] < 80:
            suggestions.append("Review grammar rules to improve accuracy")

        if university_match and university_match["score"] < 80:
            suggestions.extend(university_match.get("suggestions", []))

        if not suggestions:
            suggestions.append("Keep practicing to maintain your good performance!")

        return suggestions

    def _generate_feedback(
        self, dimensions: Dict[str, Any], overall_score: float
    ) -> str:
        """生成反馈"""
        if overall_score >= 90:
            return "Excellent! Your answer is well-structured and clearly articulated."
        elif overall_score >= 80:
            return "Good answer! Your pronunciation and grammar are solid."
        elif overall_score >= 70:
            return "Decent answer. There are some areas for improvement."
        elif overall_score >= 60:
            return "Your answer shows understanding, but needs more practice."
        else:
            return "Your answer needs significant improvement. Keep practicing!"

    def get_user_score_trend(
        self, user_id: str, dimension: Optional[str] = None, days: int = 30
    ) -> Dict[str, Any]:
        """获取用户评分趋势"""
        history = []

        dates = [item["date"] for item in history]
        scores = [item["score"] for item in history]

        return {
            "dates": dates,
            "scores": scores,
            "average": sum(scores) / len(scores) if scores else 0,
            "trend": self._calculate_trend(scores),
        }

    def _calculate_trend(self, scores: List[float]) -> str:
        """计算趋势"""
        if len(scores) < 2:
            return "stable"

        recent_avg = sum(scores[-5:]) / min(5, len(scores))
        earlier_avg = sum(scores[:-5]) / max(1, len(scores) - 5)

        if recent_avg > earlier_avg + 5:
            return "improving"
        elif recent_avg < earlier_avg - 5:
            return "declining"
        else:
            return "stable"


class ScoringConfig:
    """评分配置"""

    PRONUNCIATION_STANDARDS = {"excellent": 90, "good": 80, "fair": 70, "poor": 60}

    FLUENCY_STANDARDS = {"excellent": 90, "good": 80, "fair": 70, "poor": 60}

    VOCABULARY_STANDARDS = {"excellent": 90, "good": 80, "fair": 70, "poor": 60}

    GRAMMAR_STANDARDS = {"excellent": 90, "good": 80, "fair": 70, "poor": 60}

    SPEECH_RATE_IDEAL = (120, 150)
    PAUSE_FREQUENCY_IDEAL = 2
    AVG_SPEECH_LENGTH_IDEAL = 3

    DIVERSITY_IDEAL = 50
    ADVANCED_WORDS_THRESHOLD = 2

    @classmethod
    def get_score_level(cls, score: float, standards: Dict[str, int]) -> str:
        """获取得分等级"""
        if score >= standards["excellent"]:
            return "excellent"
        elif score >= standards["good"]:
            return "good"
        elif score >= standards["fair"]:
            return "fair"
        else:
            return "poor"
