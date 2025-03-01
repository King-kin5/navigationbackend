# src\core\config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, Field, field_validator, SecretStr
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
   
    # Application settings
    SECRET_KEY: str
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
   
    @field_validator('ENVIRONMENT')
    def validate_environment(cls, v: str) -> str:
        """Validate environment setting"""
        allowed = {'development', 'testing', 'production'}
        if v not in allowed:
            raise ValueError(f'Environment must be one of: {", ".join(allowed)}')
        return v



@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()

# Create settings instance
settings = get_settings()