"""
Configuration for the NGS360 Chat Service.

Standalone settings (env / .env), independent of the REST API's config module so
this service has no import coupling to APIServer.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # LLM gateway (Anthropic-compatible endpoint is <base>/anthropic).
    LLM_BASE_URL: str = ""
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "claude-opus-4-8"

    # Shared with the REST API so its JWTs verify here.
    JWT_SECRET_KEY: str = "change-this-secret-key-in-production"
    JWT_ALGORITHM: str = "HS256"

    # REST API base used by the agent's data-lookup tools.
    NGS360_API_URL: str = "http://localhost:3000/api/v1"

    # CORS allowed origin (the frontend).
    CLIENT_ORIGIN: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
