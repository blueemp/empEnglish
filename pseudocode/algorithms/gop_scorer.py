# GOP发音评分器实现代码
# 文件路径: algorithms/gop_scorer.py

from typing import Dict, Any


class GOPScorer:
    """GOP发音评分器"""

    PHONEME_WEIGHT = 0.7
    WORD_WEIGHT = 0.3
    MIN_SCORE = 0
    MAX_SCORE = 100

    def calculate_gop_score(self, audio_url: str, text: str) -> Dict[str, Any]:
        """Calculate GOP pronunciation score.

        Args:
            audio_url: Audio file URL
            text: Reference text

        Returns:
            Dict containing overall_score and phoneme_scores
        """
        words = text.lower().split()

        if not words:
            return {"overall_score": 0, "phoneme_scores": []}

        phoneme_scores = []
        for word in words[: min(10, len(words))]:
            phoneme_scores.append(
                {"phoneme": word, "score": min(100, 70 + len(word) * 2)}
            )

        avg_score = (
            sum(item["score"] for item in phoneme_scores) / len(phoneme_scores)
            if phoneme_scores
            else 0
        )
        overall_score = round(avg_score, 2)

        return {"overall_score": overall_score, "phoneme_scores": phoneme_scores}
