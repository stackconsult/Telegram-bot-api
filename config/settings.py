"""
Configuration settings
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # Bot Configuration
    BOT_TOKEN: str
    WEBHOOK_URL: Optional[str] = None
    ADMIN_USER_ID: int
    
    # Database
    DATABASE_URL: str = "sqlite:///./bot.db"
    REDIS_URL: str = "redis://localhost:6379"
    
    # Application
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "production"
    
    class Config:
        env_file = ".env"

settings = Settings()
