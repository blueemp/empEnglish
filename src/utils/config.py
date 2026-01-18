"""Application configuration."""

import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "empEnglish"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    model_config = SettingsConfigDict(
        extra="ignore"
    )  # Ignore extra environment variables

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "mysql+pymysql://user:password@localhost/empenglish"
    )

    # JWT
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY", "your-secret-key-change-in-production"
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Redis (for caching and rate limiting)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_TTL: int = 3600  # 1 hour

    # AI Services
    # ASR (Automatic Speech Recognition)
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "base")
    WHISPER_DEVICE: str = os.getenv("WHISPER_DEVICE", "cpu")

    # TTS (Text to Speech)
    TTS_ENGINE: str = os.getenv("TTS_ENGINE", "edge-tts")
    TTS_VOICE: str = os.getenv("TTS_VOICE", "en-US-AriaNeural")

    # LLM (Large Language Model)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "qwen")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "qwen-turbo")
    LLM_API_KEY: Optional[str] = os.getenv("LLM_API_KEY")
    LLM_BASE_URL: Optional[str] = os.getenv("LLM_BASE_URL")

    # WeChat
    WECHAT_APP_ID: str = os.getenv("WECHAT_APP_ID", "")
    WECHAT_APP_SECRET: str = os.getenv("WECHAT_APP_SECRET", "")

    # MinIO (object storage)
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_BUCKET: str = os.getenv("MINIO_BUCKET", "empenglish-audio")

    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_LOGIN_PER_HOUR: int = 10
    RATE_LIMIT_SUBMIT_PER_MINUTE: int = 20


# Global settings instance
settings = Settings()
