from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = "Cloud Companion"
    APP_VERSION: str = "0.1.0"
    DESCRIPTION: str = "AI-Powered Cloud Resource Troubleshooting Assistant"
    DEBUG: bool = Field(default=False, description="Enable debug mode")

    API_V1_PREFIX: str = "/api/v1"
    BASE_URL: str = Field(default="http://localhost:8000")

    SERVER_HOST: str = Field(default="0.0.0.0")
    SERVER_PORT: int = Field(default=8000)

    ALLOWED_HOSTS: List[str] = Field(default=["*"])
    CORS_ORIGINS: List[str] = Field(default=["*"])

    LOG_LEVEL: str = Field(default="INFO")

    @field_validator("ALLOWED_HOSTS", "CORS_ORIGINS", mode="before")
    @classmethod
    def parse_comma_separated(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            return [item.strip() for item in v.split(",")]
        return v

    NEO4J_URI: str = Field(default="bolt://localhost:7687")
    NEO4J_USER: str = Field(default="neo4j")
    NEO4J_PASSWORD: str = Field(default="")
    NEO4J_DATABASE: str = Field(default="neo4j")

    @field_validator("NEO4J_PASSWORD")
    @classmethod
    def validate_neo4j_password(cls, v: str) -> str:
        if not v:
            raise ValueError("NEO4J_PASSWORD cannot be empty")
        return v

    WEAVIATE_URL: str = Field(default="http://localhost:8080")
    WEAVIATE_API_KEY: str = Field(default="")

    ENCRYPTION_KEY: str = Field(default="")

    @field_validator("ENCRYPTION_KEY")
    @classmethod
    def validate_encryption_key(cls, v: str) -> str:
        if not v:
            raise ValueError("ENCRYPTION_KEY must be set for secure operations")
        return v

    LLM_PROVIDER: str = Field(default="ollama")
    LLM_MODEL: str = Field(default="llama2")
    LLM_API_KEY: str = Field(default="")
    LLM_BASE_URL: str = Field(default="http://localhost:11434")
    LLM_TEMPERATURE: float = Field(default=0.7, ge=0.0, le=2.0)
    LLM_MAX_TOKENS: int = Field(default=2048, gt=0)

    AWS_REGION: str = Field(default="us-east-1")
    AZURE_SUBSCRIPTION_ID: str = Field(default="")
    GCP_PROJECT_ID: str = Field(default="")

    API_KEY_EXPIRY_DAYS: int = Field(default=90, gt=0)

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
