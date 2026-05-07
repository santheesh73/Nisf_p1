from functools import lru_cache
import json
from pathlib import Path
from typing import Annotated

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings.sources.types import NoDecode

BACKEND_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = BACKEND_ROOT / ".env"
UNEXPECTED_ENV_FILES = [BACKEND_ROOT / "app" / ".env"]


class Settings(BaseSettings):
    app_name: str = "NISF Backend"
    app_env: str = "local"
    debug: bool = True
    database_url: str = "postgresql+psycopg://nisf:nisf@localhost:5432/nisf"
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "nisf"
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    allowed_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://localhost:5174",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
            "http://127.0.0.1:3000",
            "https://your-frontend-domain.com",
        ]
    )
    llm_provider: str = "local"
    groq_api_key: str | None = None
    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    huggingface_api_key: str | None = None
    groq_model: str = "llama-3.3-70b-versatile"
    openai_model: str = "gpt-4o-mini"
    gemini_model: str = "gemini-1.5-flash"
    huggingface_text_model: str = "mistralai/Mistral-7B-Instruct-v0.3"
    local_model: str = "nisf-deterministic-local"
    sentiment_model: str = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    emotion_model: str = "j-hartmann/emotion-english-distilroberta-base"
    groq_timeout_seconds: float = 20.0
    groq_max_retries: int = 1
    allow_llm_fallback: bool | None = None
    max_request_bytes: int = 20000
    jwt_secret_key: str | None = None
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 1440
    auth_enabled: bool = True

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def split_allowed_origins(cls, value):
        if isinstance(value, str):
            stripped = value.strip()
            if stripped.startswith("["):
                try:
                    parsed = json.loads(stripped)
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        "ALLOWED_ORIGINS must be valid JSON list syntax like "
                        '["https://your-frontend-domain.com"] or a comma-separated string.'
                    ) from exc
                if isinstance(parsed, list):
                    return [str(origin).strip() for origin in parsed if str(origin).strip()]
                raise ValueError(
                    "ALLOWED_ORIGINS JSON value must be a list of origin strings."
                )
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("app_env", "llm_provider", mode="before")
    @classmethod
    def normalize_lowercase_settings(cls, value):
        if isinstance(value, str):
            return value.strip().lower()
        return value

    @field_validator("app_env")
    @classmethod
    def validate_app_env(cls, value: str) -> str:
        if value not in {"local", "production"}:
            raise ValueError("APP_ENV must be either 'local' or 'production'.")
        return value

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"release", "prod", "production", "false", "0", "no", "off"}:
                return False
            if normalized in {"debug", "dev", "development", "true", "1", "yes", "on"}:
                return True
        return value

    @model_validator(mode="after")
    def validate_production_settings(self):
        if self.allow_llm_fallback is None:
            self.allow_llm_fallback = self.app_env == "local"
        if self.app_env == "production":
            if self.debug:
                raise ValueError("DEBUG=false is required when APP_ENV=production.")
            if self.llm_provider == "groq" and not self.groq_api_key:
                raise ValueError("GROQ_API_KEY is required when APP_ENV=production and LLM_PROVIDER=groq.")
            if self.auth_enabled and not self.jwt_secret_key:
                raise ValueError("JWT_SECRET_KEY is required when APP_ENV=production and AUTH_ENABLED=true.")
            if not self.auth_enabled:
                raise ValueError("AUTH_ENABLED=false is unsafe and not allowed when APP_ENV=production.")
        return self

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


def find_unexpected_env_files() -> list[Path]:
    return [path for path in UNEXPECTED_ENV_FILES if path.exists()]
