from typing import List
from pydantic import AnyUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
    )

    REDIS_URL: AnyUrl = 'redis://127.0.0.1:6379'
    API_KEY: str | None = None

    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "https://guessemon.vercel.app",
        "https://guessamon.xyz",
        "https://www.guessamon.xyz",
    ]

    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def split_csv(cls, v):
        if isinstance(v, str):
            return [s.strip() for s in v.split(',') if s.strip()]
        return v
    
settings = Settings()