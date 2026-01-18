# AI Services Knowledge Base

**Generated:** 2026-01-17
**Status:** Pseudocode Only

## OVERVIEW

AI/ML integration layer for speech processing, LLM reasoning, and interview orchestration.

## WHERE TO LOOK

| Service | File | Purpose |
|---------|------|---------|
| ASR | asr_service.py | Whisper speech recognition with VAD, streaming, and batch support |
| TTS | tts_service.py | Edge-TTS/VITS synthesis with 3 voice styles (academic/friendly/high-pressure) |
| LLM | llm_service.py | Qwen/DeepSeek for questions, feedback, follow-ups, and expression enhancement |
| Agent | agent_service.py | LangGraph orchestration: 8-node state machine for multi-turn interviews |

## CONVENTIONS

**ASR:** `language="en"` default. WhisperModel sizes: tiny/base/small/medium/large-v3. VAD parameters: threshold=0.5, min_speech=250ms, min_silence=2000ms.

**TTS:** Edge-TTS voices mapped to styles: academic (male_us, -10% rate), friendly (female_us), high_pressure (male_us, +20% rate). Async-only `synthesize()`, sync wrapper via `synthesize_sync()`.

**LLM:** LangChain `ChatOpenAI` with temperature=0.7, max_tokens=1000. Models: qwen2.5-7b (general), qwen2.5-72b (complex), deepseek-r1 (reasoning).

**Agent:** LangGraph `StateGraph` with `TypedDict` state. Workflow: generate_question → transcribe → score → generate_feedback → synthesize → follow_up → check_completion → generate_report.

**Mock Data:** `temp_audio.wav` (ASR), `minio://audio/tts/{style}/temp.mp3` (TTS).
