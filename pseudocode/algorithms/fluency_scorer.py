# 流利度评分器实现代码
# 文件路径: algorithms/fluency_scorer.py

from typing import Dict, Any, List


class FluencyScorer:
    """Fluency scorer"""

    MIN_SPEECH_RATE = 80
    OPTIMAL_SPEECH_RATE = 140
    MAX_SPEECH_RATE = 220

    MIN_PAUSE_DURATION = 0.2
    MAX_PAUSE_DURATION = 3.0

    OPTIMAL_PAUSE_RATIO = 0.15
    MAX_PAUSE_RATIO = 0.4

    def calculate_fluency_score(self, audio_url: str, text: str) -> Dict[str, Any]:
        """Calculate fluency score.

        Args:
            audio_url: Audio file URL
            text: Transcript text

        Returns:
            Dict containing fluency metrics
        """
        words = text.split()
        word_count = len(words)

        audio_duration = word_count * 0.5 if word_count > 0 else 1.0

        if word_count == 0 or audio_duration <= 0:
            return {
                "overall_score": 0,
                "speech_rate": 0,
                "avg_speech_length": 0,
                "pause_frequency": 0,
                "pauses": [],
            }

        speech_rate = round((word_count / audio_duration) * 60, 2)
        pauses = self._detect_pauses(text)
        pause_count = len(pauses)
        pause_frequency = (
            round(pause_count / (audio_duration / 60), 2) if audio_duration > 0 else 0
        )

        sentences = [s.strip() for s in text.split(".") if s.strip()]
        avg_speech_length = (
            round(sum(len(s.split()) for s in sentences) / len(sentences), 2)
            if sentences
            else 0
        )

        score = self._calculate_fluency_score(speech_rate, pause_frequency)
        overall_score = round(score, 2)

        return {
            "overall_score": overall_score,
            "speech_rate": speech_rate,
            "avg_speech_length": avg_speech_length,
            "pause_frequency": pause_frequency,
            "pauses": pauses,
        }

    def _detect_pauses(self, transcript: str) -> List[Dict[str, Any]]:
        """Detect pauses in speech."""
        pauses = []
        sentences = [s.strip() for s in transcript.split(".") if s.strip()]

        for i in range(len(sentences) - 1):
            pauses.append({"position": i, "duration": 0.5, "type": "sentence_boundary"})

        return pauses

    def _calculate_fluency_score(
        self, speech_rate: float, pause_frequency: float
    ) -> float:
        """Calculate overall fluency score."""
        rate_score = self._score_speech_rate(speech_rate)
        pause_score = self._score_pause_frequency(pause_frequency)

        overall_score = rate_score * 0.5 + pause_score * 0.5
        return max(0, min(100, overall_score))

    def _score_speech_rate(self, rate: float) -> float:
        """Score speech rate."""
        if rate < self.MIN_SPEECH_RATE:
            return (rate / self.MIN_SPEECH_RATE) * 60
        elif rate > self.MAX_SPEECH_RATE:
            return (self.MAX_SPEECH_RATE / rate) * 60
        else:
            return 100

    def _score_pause_frequency(self, frequency: float) -> float:
        """Score pause frequency."""
        ideal_freq = 2.0
        max_freq = 5.0

        if frequency <= ideal_freq:
            return 100
        elif frequency <= max_freq:
            return 100 - ((frequency - ideal_freq) / (max_freq - ideal_freq)) * 40
        else:
            return 60
