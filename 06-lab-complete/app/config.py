"""Production config — 12-Factor: tất cả từ environment variables."""
import os
import logging
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    environment: str = Field(default="development")
    debug: bool = Field(default=False)

    # App
    app_name: str = Field(default="Production AI Agent")
    app_version: str = Field(default="1.0.0")

    # LLM
    openai_api_key: str = Field(default="")
    llm_model: str = Field(default="gpt-4o-mini")

    # Security
    agent_api_key: str = Field(default="dev-key-change-me")
    jwt_secret: str = Field(default="dev-jwt-secret")
    allowed_origins: str = Field(default="*")

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    # Rate limiting
    rate_limit_per_minute: int = Field(default=20)

    # Budget
    daily_budget_usd: float = Field(default=5.0)

    # Storage
    redis_url: str = Field(default="redis://localhost:6379/0")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @field_validator("agent_api_key", "jwt_secret", mode="after")
    @classmethod
    def check_production_secrets(cls, v: str, info):
        # We can't access other fields easily in a simple validator without `info.data`, 
        # but we can do a post-init check.
        return v

def validate_settings(settings_obj: Settings) -> Settings:
    if settings_obj.environment == "production":
        if settings_obj.agent_api_key == "dev-key-change-me":
            raise ValueError("AGENT_API_KEY must be set in production!")
        if settings_obj.jwt_secret == "dev-jwt-secret":
            raise ValueError("JWT_SECRET must be set in production!")
    if not settings_obj.openai_api_key:
        logger.warning("OPENAI_API_KEY not set — using mock LLM")
    return settings_obj

settings = validate_settings(Settings())
