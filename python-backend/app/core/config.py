"""Application configuration loaded from environment variables."""

from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the analytics API.

    Values can be supplied through environment variables or a local ``.env`` file.
    Comma-separated origins are normalized into a list for FastAPI middleware.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="AI Analytics Platform API", alias="APP_NAME")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, ge=1, le=65535, alias="PORT")
    api_key: str | None = Field(default=None, alias="API_KEY")
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"], alias="CORS_ORIGINS")
    model_artifact_path: str = Field(
        default="python-backend/artifacts/regression_pipeline.joblib",
        alias="MODEL_ARTIFACT_PATH",
    )
    model_target_column: str = Field(default="target", alias="MODEL_TARGET_COLUMN")
    anomaly_contamination: float = Field(default=0.05, gt=0, lt=0.5, alias="ANOMALY_CONTAMINATION")
    max_records_per_request: int = Field(default=10000, ge=1, le=100000, alias="MAX_RECORDS_PER_REQUEST")
    max_texts_per_request: int = Field(default=1000, ge=1, le=10000, alias="MAX_TEXTS_PER_REQUEST")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_origins(cls, value: Any) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        if isinstance(value, list):
            return value
        raise TypeError("CORS_ORIGINS must be a comma-separated string or a list")

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("LOG_LEVEL must be a standard Python logging level")
        return normalized


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings object for dependency injection."""

    return Settings()
