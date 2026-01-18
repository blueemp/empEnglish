# 语法评分器实现代码
# 文件路径: algorithms/grammar_scorer.py

from typing import Dict, Any, List
import re


class GrammarError:
    """Grammar error"""

    def __init__(
        self, error_type: str, position: int, correct_form: str, error_text: str
    ):
        self.error_type = error_type
        self.position = position
        self.correct_form = correct_form
        self.error_text = error_text


class GrammarScorer:
    """Grammar scorer"""

    ERROR_TYPES = {
        "subject_verb_agreement": "主谓不一致",
        "tense_error": "时态错误",
        "article_error": "冠词错误",
        "preposition_error": "介词错误",
        "sentence_structure": "句子结构错误",
        "punctuation_error": "标点错误",
    }

    def calculate_grammar_score(self, text: str) -> Dict[str, Any]:
        """Calculate grammar score.

        Args:
            text: Transcript text

        Returns:
            Dict containing grammar metrics
        """
        errors = self._detect_grammar_errors(text)

        if not errors:
            return {"overall_score": 100, "errors": [], "sentence_variety": 1.0}

        sentences = self._split_sentences(text)
        sentence_variety = self._calculate_sentence_variety(sentences)

        error_list = []
        for error in errors:
            error_list.append(
                {
                    "error_type": error.error_type,
                    "position": error.position,
                    "correct_form": error.correct_form,
                    "error_text": error.error_text,
                }
            )

        error_count = len(errors)
        sentence_count = len(sentences) if sentences else 1

        base_score = max(0, 100 - (error_count / sentence_count) * 30)
        variety_bonus = min(10, sentence_variety * 10)

        overall_score = round(base_score + variety_bonus, 2)
        overall_score = max(0, min(100, overall_score))

        return {
            "overall_score": overall_score,
            "errors": error_list,
            "sentence_variety": sentence_variety,
        }

    def _detect_grammar_errors(self, transcript: str) -> List[GrammarError]:
        """Detect grammar errors (simplified version)."""
        errors = []

        sentences = self._split_sentences(transcript)

        basic_patterns = [
            (r"\b(he|she|it)\s+\b(is|are|was)", "subject_verb_agreement"),
            (r"\b(am|is|are)\s+not\b", "negation_error"),
            (r"\bthe\s+(cat|dog|car)s\b", "noun_verb_agreement"),
            (r"\ba\b(an|the)\s+cat\b", "article_error"),
        ]

        for sentence_idx, sentence in enumerate(sentences):
            for pattern, error_type in basic_patterns:
                matches = list(re.finditer(pattern, sentence, re.IGNORECASE))
                for match in matches:
                    errors.append(
                        GrammarError(
                            error_type=error_type,
                            position=sentence_idx,
                            correct_form="",
                            error_text=match.group(),
                        )
                    )

        return errors

    def _split_sentences(self, transcript: str) -> List[str]:
        """Split text into sentences."""
        sentences = [s.strip() for s in transcript.split(".") if s.strip()]
        return sentences

    def _calculate_sentence_variety(self, sentences: List[str]) -> float:
        """Calculate sentence variety."""
        if len(sentences) < 3:
            return 0.5

        sentence_lengths = [len(s.split()) for s in sentences]
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        variance = sum((l - avg_length) ** 2 for l in sentence_lengths) / len(
            sentence_lengths
        )

        if variance > 5:
            return 1.0
        elif variance > 2:
            return 0.8
        else:
            return 0.6
