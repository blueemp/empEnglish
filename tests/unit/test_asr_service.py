"""
Tests for ASR Service (TDD approach).
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch


class TestASRConfig:
    """Test cases for ASRConfig class."""

    def test_default_config(self):
        """Test default ASR configuration."""
        from pseudocode.ai.asr_service import ASRConfig

        config = ASRConfig()

        assert config.default_language == "en"
        assert config.default_model_size == "base"
        assert config.beam_size == 5
        assert config.vad_threshold == 0.5
        assert config.vad_min_speech_ms == 250
        assert config.vad_min_silence_ms == 2000

    def test_language_mapping(self):
        """Test language code mapping."""
        from pseudocode.ai.asr_service import ASRConfig

        config = ASRConfig()

        assert config.LANGUAGES["en"] == "English"
        assert config.LANGUAGES["zh"] == "Chinese"

    def test_model_sizes(self):
        """Test available model sizes."""
        from pseudocode.ai.asr_service import ASRConfig

        config = ASRConfig()

        assert "tiny" in config.MODEL_SIZES
        assert "base" in config.MODEL_SIZES
        assert "small" in config.MODEL_SIZES
        assert "medium" in config.MODEL_SIZES
        assert "large-v3" in config.MODEL_SIZES


class TestASRService:
    """Test cases for ASRService class."""

    def test_init_default_config(self):
        """Test initialization with default config."""
        from pseudocode.ai.asr_service import ASRService, ASRConfig

        service = ASRService(config=ASRConfig())

        assert service.config is not None
        assert service.config.default_language == "en"
        assert service.config.default_model_size == "base"

    def test_init_custom_config(self):
        """Test initialization with custom config."""
        from pseudocode.ai.asr_service import ASRService, ASRConfig

        custom_config = ASRConfig()
        custom_config.default_language = "zh"

        service = ASRService(config=custom_config)

        assert service.config.default_language == "zh"

    def test_transcribe_simple(self, mock_asr_service):
        """Test simple transcription."""
        mock_asr_service.whisper_model = MagicMock()

        result = mock_asr_service.transcribe(
            audio_url="http://example.com/audio.wav", language="en"
        )

        assert "text" in result
        assert result["text"] is not None
        assert result["language"] == "en"
        assert result["confidence"] > 0
        assert result["confidence"] <= 1

    def test_transcribe_with_beam_size(self, mock_asr_service):
        """Test transcription with custom beam size."""
        mock_asr_service.whisper_model = MagicMock()

        result = mock_asr_service.transcribe(
            audio_url="http://example.com/audio.wav", language="en", beam_size=10
        )

        assert "text" in result

    def test_transcribe_invalid_language(self, mock_asr_service):
        """Test transcription with invalid language."""
        from pseudocode.ai.asr_service import ASRConfig

        service = ASRService(config=ASRConfig())
        service.whisper_model = MagicMock()

        with pytest.raises(ValueError):
            service.transcribe(
                audio_url="http://example.com/audio.wav", language="invalid_language"
            )

    def test_transcribe_async(self, mock_asr_service):
        """Test async transcription."""
        mock_asr_service.whisper_model = MagicMock()

        result = mock_asr_service.transcribe_async(
            audio_url="http://example.com/audio.wav", language="en"
        )

        assert isinstance(result, dict)

    def test_transcribe_stream(self, mock_asr_service):
        """Test streaming transcription."""
        mock_asr_service.whisper_model = MagicMock()
        mock_stream = MagicMock()

        result = mock_asr_service.transcribe_stream(
            audio_stream=mock_stream, language="en"
        )

        assert "text" in result

    def test_batch_transcribe(self, mock_asr_service):
        """Test batch transcription."""
        mock_asr_service.whisper_model = MagicMock()

        audio_urls = [
            "http://example.com/audio1.wav",
            "http://example.com/audio2.wav",
            "http://example.com/audio3.wav",
        ]

        results = mock_asr_service.batch_transcribe(
            audio_urls=audio_urls, language="en"
        )

        assert len(results) == 3

    def test_batch_transcribe_with_vad(self, mock_asr_service):
        """Test batch transcription with VAD enabled."""
        mock_asr_service.whisper_model = MagicMock()

        audio_urls = [
            "http://example.com/audio1.wav",
            "http://example.com/audio2.wav",
        ]

        results = mock_asr_service.batch_transcribe(
            audio_urls=audio_urls, language="en", vad_filter=True
        )

        assert len(results) == 3

    def test_get_supported_languages(self, mock_asr_service):
        """Test getting supported languages."""
        from pseudocode.ai.asr_service import ASRConfig

        languages = ASRConfig.LANGUAGES

        assert "en" in languages
        assert "zh" in languages
        assert len(languages) > 0

    def test_get_supported_model_sizes(self, mock_asr_service):
        """Test getting supported model sizes."""
        from pseudocode.ai.asr_service import ASRConfig

        model_sizes = ASRConfig.MODEL_SIZES

        assert "tiny" in model_sizes
        assert "base" in model_sizes
        assert len(model_sizes) > 0
