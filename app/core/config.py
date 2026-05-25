"""
Configuration settings for the FastAPI application
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Basic settings
    PORT: int = 8000
    PROJECT_NAME: str = "FastAPI Example"
    PROJECT_DESCRIPTION: str = "A comprehensive FastAPI example application"
    VERSION: str = "0.1.0"
    DEBUG: bool = Field(default=False)

    # API settings
    API_V1_STR: str = "/api/v1"

    # Security settings
    SECRET_KEY: str = Field(default="your-secret-key-change-this-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database settings
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./app.db",
        description="Database URL. Use postgresql+asyncpg://user:pass@localhost/db for PostgreSQL",
    )

    # CORS settings
    ALLOWED_HOSTS: list[str] = ["*"]

    # Environment
    ENVIRONMENT: str = Field(default="development")

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
    }


# Create settings instance
settings = Settings()
