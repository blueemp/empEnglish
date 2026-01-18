# 词汇评分器实现代码
# 文件路径: algorithms/vocabulary_scorer.py

from typing import Dict, Any, List
import re


class VocabularyScorer:
    """Vocabulary scorer"""

    BASIC_WORDS = set(
        ["the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "of", "is"]
    )
    ADVANCED_WORDS = set(
        [
            "analyze",
            "evaluate",
            "implement",
            "comprehensive",
            "sophisticated",
            "perspective",
            "consequently",
            "furthermore",
            "nevertheless",
        ]
    )
    ACADEMIC_WORDS = set(
        [
            "hypothesis",
            "methodology",
            "theoretical",
            "empirical",
            "quantitative",
            "qualitative",
            "subsequently",
        ]
    )

    def calculate_vocabulary_score(self, text: str) -> Dict[str, Any]:
        """Calculate vocabulary score.

        Args:
            text: Transcript text

        Returns:
            Dict containing vocabulary metrics
        """
        words = self._extract_words(text)

        if not words:
            return {
                "overall_score": 0,
                "diversity": 0,
                "advanced_words": [],
                "word_count": 0,
            }

        word_count = len(words)
        unique_words = len(set(words))
        advanced_words_found = self._identify_advanced_words(words)
        word_diversity = self._calculate_diversity(words)

        score = self._calculate_vocabulary_score(
            word_count, unique_words, advanced_words_found, word_diversity
        )
        overall_score = round(score, 2)

        return {
            "overall_score": overall_score,
            "diversity": round(word_diversity, 2),
            "advanced_words": advanced_words_found,
            "word_count": word_count,
        }

    def _extract_words(self, transcript: str) -> List[str]:
        """Extract words from transcript."""
        words = re.findall(r"\b[a-zA-Z]+\b", transcript.lower())
        return [w for w in words if len(w) > 1]

    def _identify_advanced_words(self, words: List[str]) -> List[str]:
        """Identify advanced vocabulary."""
        advanced_words = []
        for word in words:
            if word in self.ADVANCED_WORDS or word in self.ACADEMIC_WORDS:
                advanced_words.append(word)
        return advanced_words

    def _calculate_diversity(self, words: List[str]) -> float:
        """Calculate vocabulary diversity."""
        if not words:
            return 0

        unique_words = set(words)
        total_words = len(words)

        if total_words <= 10:
            return 0

        return (len(unique_words) / total_words) * 100

    def _calculate_vocabulary_score(
        self, word_count: int, unique: int, advanced: List[str], diversity: float
    ) -> float:
        """Calculate overall vocabulary score."""
        if word_count < 10:
            base_score = 30
        elif word_count < 30:
            base_score = 60
        else:
            base_score = 80

        diversity_bonus = min(20, diversity * 0.2)
        advanced_bonus = min(20, len(advanced) * 2)

        score = base_score + diversity_bonus + advanced_bonus
        return min(100, max(0, score))
