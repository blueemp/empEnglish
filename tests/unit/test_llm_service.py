"""
Tests for LLM Service (TDD approach).
"""
import pytest


class TestLLMConfig:
    """Test cases for LLMConfig class."""

    def test_default_config(self):
        """Test default LLM configuration."""
        from pseudocode.ai.llm_service import LLMConfig

        config = LLMConfig()

        assert config.default_provider == "qwen"
        assert config.default_model == "qwen2.5-7b"
        assert config.default_temperature == 0.7
        assert config.default_max_tokens == 1000

    def test_provider_mapping(self):
        """Test provider model mapping."""
        from pseudocode.ai.llm_service import LLMConfig

        config = LLMConfig()

        assert config.PROVIDER_MODELS["qwen"]["7b"] == "qwen2.5-7b"
        assert config.PROVIDER_MODELS["qwen"]["72b"] == "qwen2.5-72b"
        assert config.PROVIDER_MODELS["deepseek"]["r1"] == "deepseek-r1"


class TestLLMService:
    """Test cases for LLMService class."""

    def test_init_with_config(self, test_config):
        """Test initialization with config."""
        from pseudocode.ai.llm_service import LLMService, LLMConfig

        config = LLMConfig()
        service = LLMService(config=config)

        assert service.config is not None

    def test_init_default_config(self):
        """Test initialization with default config."""
        from pseudocode.ai.llm_service import LLMService

        service = LLMService()

        assert service.config.default_provider == "qwen"
        assert service.config.default_model == "qwen2.5-7b"

    def test_generate_question(self, mock_llm_service):
        """Test question generation."""
        mock_llm_service.llm.generate.return_value = "Tell me about yourself"

        result = mock_llm_service.generate_question(
            question_type="SELF_INTRODUCTION",
            difficulty=3,
            target_university="Xi'an Jiaotong University",
            target_major="Computer Science"
        )

        assert "question" in result
        assert result["question"] is not None
        assert "Tell me" in result["question"]
        assert "yourself" in result["question"]

    def test_generate_feedback(self, mock_llm_service):
        """Test feedback generation."""
        mock_llm_service.llm.generate.return_value = "Good pronunciation, but try to slow down"

        result = mock_llm_service.generate_feedback(
            question="What is your name?",
            answer="My name is John",
            score_details={
                "pronunciation": {"score": 85.5},
                "fluency": {"score": 78.0}
            }
        )

        assert "feedback" in result
        assert "Good" in result["feedback"]
        assert "pronunciation" in result["feedback"]

    def test_generate_follow_up(self, mock_llm_service):
        """Test follow-up question generation."""
        mock_llm_service.llm.generate.return_value = "Can you elaborate on your previous answer?"

        result = mock_llm_service.generate_follow_up(
            question="What is your name?",
            answer="My name is John"
            conversation_history=[{"role": "user", "content": "My name is John"}]
        )

        assert "follow_up" in result
        assert "Can you" in result["follow_up"]
        assert "elaborate" in result["follow_up"]

    def test_enhance_expression(self, mock_llm_service):
        """Test expression enhancement."""
        mock_llm_service.llm.generate.return_value = "I think this is a wonderful opportunity to share my research."

        result = mock_llm_service.enhance_expression(
            text="This is good",
            target_style="academic"
        )

        assert "enhanced" in result
        assert "wonderful" in result["enhanced"]
        assert "opportunity" in result["enhanced"]

    def test_switch_model(self, mock_llm_service):
        """Test switching LLM models."""
        from pseudocode.ai.llm_service import LLMConfig

        config = LLMConfig()

        result = mock_llm_service.switch_model(model="qwen2.5-72b")

        assert result["previous_model"] == "qwen2.5-7b"
        assert result["new_model"] == "qwen2.5-72b"

    def test_get_current_model(self, mock_llm_service):
        """Test getting current model."""
        from pseudocode.ai.llm_service import LLMConfig

        config = LLMConfig()

        result = mock_llm_service.get_current_model()

        assert "provider" in result
        assert "model" in result


@pytest.fixture
def mock_llm_service():
    """Mock LLMService for testing."""
    from unittest.mock import MagicMock
    from pseudocode.ai.llm_service import LLMService, LLMConfig

    service = MagicMock(spec=LLMService)
    service.config = LLMConfig()
    return service
