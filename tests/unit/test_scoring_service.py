# 评分服务测试
# 文件路径: tests/unit/test_scoring_service.py

import pytest
from unittest.mock import Mock, patch
from pseudocode.services.scoring_service import ScoringService, ScoringConfig
from pseudocode.algorithms.gop_scorer import GOPScorer
from pseudocode.algorithms.fluency_scorer import FluencyScorer
from pseudocode.algorithms.vocabulary_scorer import VocabularyScorer
from pseudocode.algorithms.grammar_scorer import GrammarScorer
from pseudocode.algorithms.university_match_scorer import UniversityMatchScorer


@pytest.fixture
def scorers():
    """Fixture providing all scorer instances"""
    return {
        "gop_scorer": GOPScorer(),
        "fluency_scorer": FluencyScorer(),
        "vocabulary_scorer": VocabularyScorer(),
        "grammar_scorer": GrammarScorer(),
        "university_match_scorer": UniversityMatchScorer(),
    }


@pytest.fixture
def scoring_service(scorers):
    """Fixture providing scoring service instance"""
    return ScoringService(**scorers)


class TestScoringServiceInitialization:
    """Test scoring service initialization"""

    def test_initialization(self, scorers):
        """Test that scoring service initializes correctly"""
        service = ScoringService(**scorers)
        assert service.gop_scorer is not None
        assert service.fluency_scorer is not None
        assert service.vocabulary_scorer is not None
        assert service.grammar_scorer is not None
        assert service.university_match_scorer is not None

    def test_default_weights(self, scorers):
        """Test that default weights are set correctly"""
        service = ScoringService(**scorers)
        assert service.weights["pronunciation"] == 0.25
        assert service.weights["fluency"] == 0.25
        assert service.weights["vocabulary"] == 0.25
        assert service.weights["grammar"] == 0.25
        assert service.weights["university_match"] == 0.0


class TestEvaluate:
    """Test comprehensive evaluation"""

    def test_evaluate_general_mode(self, scoring_service):
        """Test evaluation in general mode (no university)"""
        result = scoring_service.evaluate(
            question="What is your major?",
            answer="I study computer science",
            audio_url="http://example.com/audio.wav",
        )

        assert "overall_score" in result
        assert "dimensions" in result
        assert "feedback" in result
        assert "suggestions" in result
        assert "pronunciation" in result["dimensions"]
        assert "fluency" in result["dimensions"]
        assert "vocabulary" in result["dimensions"]
        assert "grammar" in result["dimensions"]
        assert "university_match" not in result["dimensions"]
        assert isinstance(result["overall_score"], (int, float))
        assert 0 <= result["overall_score"] <= 100

    def test_evaluate_university_mode(self, scoring_service):
        """Test evaluation in university mode"""
        result = scoring_service.evaluate(
            question="Why do you want to study here?",
            answer="I want to study computer science and algorithms",
            audio_url="http://example.com/audio.wav",
            university="西安交通大学",
            major="计算机科学与技术",
        )

        assert "overall_score" in result
        assert "university_match" in result["dimensions"]
        assert isinstance(result["overall_score"], (int, float))
        assert 0 <= result["overall_score"] <= 100

    def test_evaluate_pronunciation_score_present(self, scoring_service):
        """Test that pronunciation score is included"""
        result = scoring_service.evaluate(
            question="Test question",
            answer="Test answer",
            audio_url="http://example.com/audio.wav",
        )
        pron = result["dimensions"]["pronunciation"]
        assert "overall_score" in pron
        assert "phoneme_scores" in pron

    def test_evaluate_fluency_score_present(self, scoring_service):
        """Test that fluency score is included"""
        result = scoring_service.evaluate(
            question="Test question",
            answer="This is a longer test answer. It has multiple sentences.",
            audio_url="http://example.com/audio.wav",
        )
        fluency = result["dimensions"]["fluency"]
        assert "overall_score" in fluency
        assert "speech_rate" in fluency
        assert "avg_speech_length" in fluency
        assert "pause_frequency" in fluency
        assert "pauses" in fluency

    def test_evaluate_vocabulary_score_present(self, scoring_service):
        """Test that vocabulary score is included"""
        result = scoring_service.evaluate(
            question="Test question",
            answer="This is a sophisticated comprehensive answer",
            audio_url="http://example.com/audio.wav",
        )
        vocab = result["dimensions"]["vocabulary"]
        assert "overall_score" in vocab
        assert "diversity" in vocab
        assert "advanced_words" in vocab
        assert "word_count" in vocab

    def test_evaluate_grammar_score_present(self, scoring_service):
        """Test that grammar score is included"""
        result = scoring_service.evaluate(
            question="Test question",
            answer="The quick brown fox jumps over the lazy dog",
            audio_url="http://example.com/audio.wav",
        )
        grammar = result["dimensions"]["grammar"]
        assert "overall_score" in grammar
        assert "errors" in grammar
        assert "sentence_variety" in grammar


class TestEvaluatePronunciation:
    """Test pronunciation evaluation"""

    def test_evaluate_pronunciation(self, scoring_service):
        """Test pronunciation evaluation"""
        result = scoring_service.evaluate_pronunciation(
            audio_url="http://example.com/audio.wav", text="hello world test"
        )

        assert "score" in result
        assert "word_scores" in result
        assert "common_errors" in result
        assert isinstance(result["score"], (int, float))
        assert 0 <= result["score"] <= 100
        assert isinstance(result["word_scores"], list)


class TestEvaluateFluency:
    """Test fluency evaluation"""

    def test_evaluate_fluency(self, scoring_service):
        """Test fluency evaluation"""
        result = scoring_service.evaluate_fluency(
            audio_url="http://example.com/audio.wav",
            text="This is a test. It has multiple parts.",
        )

        assert "score" in result
        assert "speech_rate" in result
        assert "avg_speech_length" in result
        assert "pause_frequency" in result
        assert "pauses" in result
        assert isinstance(result["score"], (int, float))
        assert 0 <= result["score"] <= 100


class TestEvaluateVocabulary:
    """Test vocabulary evaluation"""

    def test_evaluate_vocabulary(self, scoring_service):
        """Test vocabulary evaluation"""
        result = scoring_service.evaluate_vocabulary(
            text="This is a sophisticated comprehensive evaluation"
        )

        assert "score" in result
        assert "diversity" in result
        assert "advanced_words" in result
        assert "word_count" in result
        assert isinstance(result["score"], (int, float))
        assert 0 <= result["score"] <= 100


class TestEvaluateGrammar:
    """Test grammar evaluation"""

    def test_evaluate_grammar(self, scoring_service):
        """Test grammar evaluation"""
        result = scoring_service.evaluate_grammar(
            text="The quick brown fox jumps over the lazy dog"
        )

        assert "score" in result
        assert "errors" in result
        assert "sentence_variety" in result
        assert isinstance(result["score"], (int, float))
        assert 0 <= result["score"] <= 100


class TestScoringConfig:
    """Test scoring configuration"""

    def test_pronunciation_standards(self):
        """Test pronunciation standards"""
        assert ScoringConfig.PRONUNCIATION_STANDARDS["excellent"] == 90
        assert ScoringConfig.PRONUNCIATION_STANDARDS["good"] == 80
        assert ScoringConfig.PRONUNCIATION_STANDARDS["fair"] == 70
        assert ScoringConfig.PRONUNCIATION_STANDARDS["poor"] == 60

    def test_fluency_standards(self):
        """Test fluency standards"""
        assert ScoringConfig.FLUENCY_STANDARDS["excellent"] == 90
        assert ScoringConfig.FLUENCY_STANDARDS["good"] == 80
        assert ScoringConfig.FLUENCY_STANDARDS["fair"] == 70
        assert ScoringConfig.FLUENCY_STANDARDS["poor"] == 60

    def test_vocabulary_standards(self):
        """Test vocabulary standards"""
        assert ScoringConfig.VOCABULARY_STANDARDS["excellent"] == 90
        assert ScoringConfig.VOCABULARY_STANDARDS["good"] == 80
        assert ScoringConfig.VOCABULARY_STANDARDS["fair"] == 70
        assert ScoringConfig.VOCABULARY_STANDARDS["poor"] == 60

    def test_grammar_standards(self):
        """Test grammar standards"""
        assert ScoringConfig.GRAMMAR_STANDARDS["excellent"] == 90
        assert ScoringConfig.GRAMMAR_STANDARDS["good"] == 80
        assert ScoringConfig.GRAMMAR_STANDARDS["fair"] == 70
        assert ScoringConfig.GRAMMAR_STANDARDS["poor"] == 60

    def test_get_score_level_excellent(self):
        """Test get_score_level for excellent score"""
        level = ScoringConfig.get_score_level(95, ScoringConfig.PRONUNCIATION_STANDARDS)
        assert level == "excellent"

    def test_get_score_level_good(self):
        """Test get_score_level for good score"""
        level = ScoringConfig.get_score_level(85, ScoringConfig.PRONUNCIATION_STANDARDS)
        assert level == "good"

    def test_get_score_level_fair(self):
        """Test get_score_level for fair score"""
        level = ScoringConfig.get_score_level(75, ScoringConfig.PRONUNCIATION_STANDARDS)
        assert level == "fair"

    def test_get_score_level_poor(self):
        """Test get_score_level for poor score"""
        level = ScoringConfig.get_score_level(55, ScoringConfig.PRONUNCIATION_STANDARDS)
        assert level == "poor"
