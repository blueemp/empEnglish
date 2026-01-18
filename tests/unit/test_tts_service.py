"""
Tests for TTS Service (TDD approach).
"""

import pytest


class TestTTSConfig:
    """Test cases for TTSConfig class."""

    def test_default_config(self):
        """Test default TTS configuration."""
        from pseudocode.ai.tts_service import TTSConfig

        config = TTSConfig()

        assert config.default_service == "edge-tts"
        assert config.default_voice == "male_us"
        assert config.default_rate == 1.0
        assert config.default_style == "friendly"

    def test_voice_mapping(self):
        """Test voice style mapping."""
        from pseudocode.ai.tts_service import TTSConfig

        config = TTSConfig()

        assert config.VOICES["academic"] == {"name": "male_us", "rate": -0.1}
        assert config.VOICES["friendly"] == {"name": "female_us", "rate": 1.0}
        assert config.VOICES["high_pressure"] == {"name": "male_us", "rate": 1.2}

    def test_get_voice_by_style(self):
        """Test getting voice by style."""
        from pseudocode.ai.tts_service import TTSConfig

        assert TTSConfig.get_voice_by_style(1) == {"name": "male_us", "rate": -0.1}
        assert TTSConfig.get_voice_by_style(2) == {"name": "female_us", "rate": 1.0}
        assert TTSConfig.get_voice_by_style(3) == {"name": "male_us", "rate": 1.2}


class TestTTSService:
    """Test cases for TTSService class."""

    def test_init_with_config(self):
        """Test initialization with config."""
        from pseudocode.ai.tts_service import TTSService, TTSConfig

        config = TTSConfig()
        service = TTSService(config=config)

        assert service.config is not None
        assert service.config.default_service == "edge-tts"

    def test_synthesize_simple(self, mock_tts_service):
        """Test simple synthesis."""
        mock_tts_service.synthesize.return_value = "http://mock.audio/tts.mp3"

        result = mock_tts_service.synthesize(text="Hello world", style="friendly")

        assert "audio_url" in result
        assert result["audio_url"] == "http://mock.audio/tts.mp3"
        assert result["duration"] > 0

    def test_synthesize_with_style_1(self, mock_tts_service):
        """Test synthesis with style 1 (academic)."""
        mock_tts_service.synthesize.return_value = "http://mock.audio/tts_academic.mp3"

        result = mock_tts_service.synthesize(text="Please introduce yourself", style=1)

        assert "audio_url" in result
        assert result["duration"] > 0

    def test_synthesize_with_style_2(self, mock_tts_service):
        """Test synthesis with style 2 (friendly)."""
        mock_tts_service.synthesize.return_value = "http://mock.audio/tts_friendly.mp3"

        result = mock_tts_service.synthesize(
            text="Tell me about your research", style=2
        )

        assert "audio_url" in result

    def test_synthesize_with_style_3(self, mock_tts_service):
        """Test synthesis with style 3 (high pressure)."""
        mock_tts_service.synthesize.return_value = "http://mock.audio/tts_pressure.mp3"

        result = mock_tts_service.synthesize(
            text="Why do you want to work here", style=3
        )

        assert "audio_url" in result
        assert result["duration"] > 0

    def test_synthesize_invalid_style(self, mock_tts_service):
        """Test synthesis with invalid style."""
        from pseudocode.ai.tts_service import TTSService
        from pydantic import ValidationError

        service = TTSService(config=TTSConfig())

        with pytest.raises(ValidationError):
            service.synthesize(text="Test text", style=999)

    def test_synthesize_empty_text(self, mock_tts_service):
        """Test synthesis with empty text."""
        from pydantic import ValidationError

        service = TTSService(config=TTSConfig())

        with pytest.raises(ValidationError):
            service.synthesize(text="", style=1)

    def test_synthesize_async(self, mock_tts_service):
        """Test async synthesis."""
        from pseudocode.ai.tts_service import TTSService
        import asyncio

        mock_tts_service.synthesize.return_value = "http://mock.audio/tts_async.mp3"

        async def run_async():
            result = await mock_tts_service.synthesize_async(
                text="Hello", style="friendly"
            )
            return result

        result = asyncio.run(run_async())

        assert "audio_url" in result

    def test_batch_synthesize(self, mock_tts_service):
        """Test batch synthesis."""
        texts = ["First sentence", "Second sentence", "Third sentence"]
        style = 1

        mock_tts_service.batch_synthesize.return_value = [
            {"audio_url": f"http://mock.audio/tts_{i}.mp3"} for i in range(len(texts))
        ]

        results = mock_tts_service.batch_synthesize(texts=texts, style=style)

        assert len(results) == 3
        assert all("audio_url" in r for r in results)

    def test_batch_synthesize_different_styles(self, mock_tts_service):
        """Test batch synthesis with different styles."""
        texts = ["A", "B", "C"]
        styles = [1, 2, 3]

        mock_tts_service.batch_synthesize.return_value = [
            {"audio_url": f"http://mock.audio/{t}_synthesis.mp3"} for t in texts
        ]

        results = mock_tts_service.batch_synthesize(texts=texts, styles=styles)

        assert len(results) == 9

    def test_get_supported_voices(self, mock_tts_service):
        """Test getting supported voices."""
        mock_tts_service.get_supported_voices.return_value = ["male_us", "female_us"]

        voices = mock_tts_service.get_supported_voices()

        assert len(voices) == 2
        assert "male_us" in voices
        assert "female_us" in voices


@pytest.fixture
def mock_tts_service():
    """Mock TTSService for testing."""
    from unittest.mock import MagicMock
    from pseudocode.ai.tts_service import TTSService, TTSConfig

    service = MagicMock(spec=TTSService)

    service.config = TTSConfig()
    return service
