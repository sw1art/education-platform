"""File with settings and configs for the project"""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    REAL_DATABASE_URL: str = Field(
        "postgresql+asyncpg://postgres:postgres@db:5432/education_db",
        env="REAL_DATABASE_URL"
        )
    APP_PORT: int = Field(
        8000, 
        env="APP_PORT"
        )
    SECRET_KEY: str = Field(
        "secret_key", 
        env="SECRET_KEY"
        )
    ALGORITHM: str = Field(
        "HS256", 
        env="ALGORITHM"
        )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        30, 
        env="ACCESS_TOKEN_EXPIRE_MINUTES"
        )
    SENTRY_URL: str = Field(
        "", 
        env="SENTRY_URL"
        )
    TEST_DATABASE_URL: str = Field(
        "postgresql+asyncpg://postgres_test:postgres_test@test_db:5433/postgres_test", 
        env="TEST_DATABASE_URL"
        )
    DEBUG: bool = Field(
        False,
        env="DEBUG"
        )
    REDIS_URL: str = Field(
        "redis://localhost:6379/0",
        env="REDIS_URL"
        )
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"),
        env_file_encoding="utf-8"
    )

settings = Settings()