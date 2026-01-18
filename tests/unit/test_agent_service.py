"""
Tests for Agent Service (TDD approach).
"""
import pytest


class TestInterviewAgent:
    """Test cases for InterviewAgent class."""

    def test_agent_factory_default(self):
        """Test AgentFactory with default config."""
        from pseudocode.ai.agent_service import AgentFactory

        agent = AgentFactory.create()

        assert agent is not None
        assert agent.config is not None
        assert agent.config.default_mode == "GENERAL"
        assert agent.config.default_pressure_level == 2

    def test_agent_factory_custom_config(self):
        """Test AgentFactory with custom config."""
        from pseudocode.ai.agent_service import AgentFactory, AgentConfig

        config = AgentConfig()
        config.default_mode = "UNIVERSITY"
        config.default_pressure_level = 3

        agent = AgentFactory.create(config=config)

        assert agent.config.default_mode == "UNIVERSITY"
        assert agent.config.default_pressure_level == 3

    def test_initial_state(self):
        """Test initial state creation."""
        from pseudocode.ai.agent_service import InterviewAgent

        initial_state = InterviewAgent.get_initial_state()

        assert "user_id" in initial_state
        assert "current_question" in initial_state
        assert "current_turn" in initial_state
        assert "total_score" in initial_state
        assert "turns" in initial_state
        assert "completed" in initial_state
        assert "error_message" in initial_state

    def test_generate_question_node(self, mock_agent):
        """Test generate_question node."""
        from pseudocode.ai.agent_service import InterviewAgent

        mock_agent.question_service.generate_question.return_value = "Tell me about yourself"

        mock_agent._call_mock_services.return_value = {"text": "Tell me about yourself"}

        state = {
            "user_id": "test_user",
            "current_question": "Previous question",
            "turns": []
        }

        new_state = mock_agent.generate_question_node(state=state)

        assert new_state["current_question"] == "Tell me about yourself"
        assert "turns" in new_state

    def test_transcribe_audio_node(self, mock_agent):
        """Test transcribe_audio node."""
        from pseudocode.ai.agent_service import InterviewAgent

        mock_agent.asr_service.transcribe.return_value = {"text": "Hello world"}

        state = {
            "user_id": "test_user",
            "current_turn": {"audio_url": "http://example.com/audio.wav"},
            "turns": []
        }

        new_state = mock_agent.transcribe_audio(state=state)

        assert "transcription" in new_state
        assert new_state["transcription"]["text"] == "Hello world"

    def test_score_answer_node(self, mock_agent):
        """Test score_answer node."""
        from pseudocode.ai.agent_service import InterviewAgent

        state = {
            "user_id": "test_user",
            "current_question": "Tell me about yourself",
            "user_answer": "I am John",
            "turns": []
        }

        mock_result = {
            "pronunciation": {"score": 85},
            "fluency": {"score": 75},
            "vocabulary": {"score": 80},
            "grammar": {"score": 90},
            "overall": 82.5
        }

        mock_agent.scoring_service.evaluate.return_value = mock_result

        new_state = mock_agent.score_answer(state=state)

        assert new_state["overall_score"] == 82.5
        assert "score_details" in new_state

    def test_generate_feedback_node(self, mock_agent):
        """Test generate_feedback node."""
        from pseudocode.ai.agent_service import InterviewAgent

        state = {
            "user_id": "test_user",
            "current_question": "Tell me about yourself",
            "user_answer": "I am John",
            "overall_score": 82.5
            "score_details": {
                "pronunciation": {"score": 85},
                "fluency": {"score": 75}
            }
        }

        mock_feedback = "Good pronunciation, but speak more slowly."

        mock_agent.llm_service.generate_feedback.return_value = mock_feedback

        new_state = mock_agent.generate_feedback(state=state)

        assert new_state["current_feedback"] == mock_feedback

    def test_synthesize_feedback_node(self, mock_agent):
        """Test synthesize_feedback node."""
        from pseudocode.ai.agent_service import InterviewAgent

        state = {
            "user_id": "test_user",
            "current_feedback": "Good pronunciation",
            "turns": []
        }

        mock_tts_service.synthesize.return_value = "http://mock.audio/feedback.mp3"

        mock_agent.tts_service.synthesize.return_value = mock_tts_service.synthesize.return_value

        new_state = mock_agent.synthesize_feedback(state=state)

        assert new_state["feedback_audio_url"] == "http://mock.audio/feedback.mp3"

    def test_generate_follow_up_node(self, mock_agent):
        """Test generate_follow_up node."""
        from pseudocode.ai.agent_service import InterviewAgent

        state = {
            "user_id": "test_user",
            "current_question": "Tell me about yourself",
            "user_answer": "I am John",
            "turns": []
        }

        mock_follow_up = "Can you tell me more?"

        mock_agent.llm_service.generate_follow_up.return_value = mock_follow_up

        new_state = mock_agent.generate_follow_up(state=state)

        assert new_state["current_follow_up"] == mock_follow_up

    def test_check_completion_node(self, mock_agent):
        """Test check_completion node (not completed)."""
        from pseudocode.ai.agent_service import InterviewAgent

        state = {
            "user_id": "test_user",
            "turns": [1, 2, 3, 4]
        }

        new_state = mock_agent.check_completion(state=state)

        assert new_state["completed"] is False
        assert len(new_state["turns"]) == 5

    def test_check_completion_node_max_turns(self, mock_agent):
        """Test check_completion node (max turns reached)."""
        from pseudocode.ai.agent_service import InterviewAgent

        state = {
            "user_id": "test_user",
            "turns": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        }

        new_state = mock_agent.check_completion(state=state)

        assert new_state["completed"] is True
        assert new_state["session_status"] == "COMPLETED"

    def test_generate_report_node(self, mock_agent):
        """Test generate_report node."""
        from pseudocode.ai.agent_service import InterviewAgent

        state = {
            "user_id": "test_user",
            "turns": [1, 2, 3],
            "completed": True,
            "total_score": 85.5
        }

        mock_report = "Overall good performance. Focus on improving fluency."

        mock_agent.report_service.generate.return_value = mock_report

        new_state = mock_agent.generate_report(state=state)

        assert new_state["report"] == mock_report
        assert new_state["session_status"] == "COMPLETED"


@pytest.fixture
def mock_agent():
    """Mock InterviewAgent for testing."""
    from unittest.mock import MagicMock
    from pseudocode.ai.agent_service import InterviewAgent

    agent = MagicMock(spec=InterviewAgent)
    return agent
