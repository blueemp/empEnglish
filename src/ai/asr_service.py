# ASR服务实现代码（Mock版本，用于测试）
# 文件路径: ai/asr_service.py

from typing import Dict, Any, Optional, List
import asyncio
from unittest.mock import MagicMock, AsyncMock


class ASRConfig:
    """ASR配置"""

    DEFAULT_LANGUAGE = "en"
    DEFAULT_MODEL_SIZE = "base"
    DEFAULT_DEVICE = "cpu"

    # 语言代码映射
    LANGUAGES = {
        "en": "English",
        "zh": "Chinese",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "ja": "Japanese",
        "ko": "Korean"
    }

    # 模型大小配置
    MODEL_SIZES = {
        "tiny": {"parameters": 39M, "speed": "realtime"},
        "base": {"parameters": 74M, "speed": "realtime"},
        "small": {"parameters": 244M, "speed": "realtime"},
        "medium": {"parameters": 769M, "speed": "realtime"},
        "large": {"parameters": 1550M, "speed": "realtime"},
        "large-v2": {"parameters": 3050M, "speed": "realtime"},
        "large-v3": {"parameters": 8265M, "speed": "realtime"}
    }

    VAD_CONFIG = {
        "threshold": 0.5,
        "min_speech_ms": 250,
        "min_silence_ms": 2000
    }


class ASRService:
    """ASR服务（Mock版本）"""

    def __init__(self, model_size: str = "base", device: str = "cpu", config: Optional[ASRConfig] = None):
        """
        初始化ASR服务

        Args:
            model_size: 模型大小
            device: 设备
            config: 配置（可选）
        """
        self.config = config or ASRConfig()
        self.model_size = model_size
        self.device = device

        self.sample_rate = self.config.get_sample_rate() or 16000

    def _download_audio(self, audio_url: str) -> str:
        """下载音频文件（Mock）"""
        return f"/tmp/temp_audio_{audio_url.split('/')[-1]}.wav"

    def transcribe(
        self,
        audio_url: str,
        language: str = "en",
        beam_size: int = 5,
        vad_filter: bool = True
    ) -> Dict[str, Any]:
        """
        语音转写

        Args:
            audio_url: 音频文件URL
            language: 语言
            beam_size: beam大小
            vad_filter: 是否使用VAD过滤

        Returns:
            转写结果
        """
        return {
            "text": f"Mock transcribed text for {audio_url}",
            "language": language,
            "confidence": 0.95,
            "duration": 15.5
        }

    async def transcribe_async(
        self,
        audio_url: str,
        language: str = "en"
        beam_size: int = 5
    ) -> Dict[str, Any]:
        """异步语音转写"""
        await asyncio.sleep(0.1)
        return {
            "text": f"Mock async transcribed text for {audio_url}",
            "language": language,
            "confidence": 0.95
        }

    def transcribe_stream(self, audio_stream: Any, language: str = "en") -> Dict[str, Any]:
        """流式语音转写"""
        return {
            "text": "Mock streaming transcription",
            "language": language
            "is_final": False
        }

    def batch_transcribe(
        self,
        audio_urls: List[str],
        language: str = "en",
        vad_filter: bool = False
    ) -> List[Dict[str, Any]]:
        """批量语音转写"""
        results = []
        for url in audio_urls:
            results.append({
                "text": f"Mock batch transcription for {url}",
                "language": language,
                "confidence": 0.95
            })
        return results

    def get_supported_languages(self) -> List[str]:
        """获取支持的语言列表"""
        return list(ASRConfig.LANGUAGES.keys())

    def get_supported_model_sizes(self) -> List[str]:
        """获取支持的模型大小列表"""
        return list(ASRConfig.MODEL_SIZES.keys())

    def check_audio_format(self, audio_url: str) -> bool:
        """检查音频格式（Mock）"""
        return audio_url.endswith(('.wav', '.mp3', '.m4a'))

    def get_audio_duration(self, audio_path: str) -> float:
        """获取音频时长（Mock）"""
        return 15.0

    def detect_language(self, audio_url: str) -> str:
        """检测音频语言（Mock）"""
        return ASRConfig.DEFAULT_LANGUAGE
