from typing import List
from pydantic import RedisDsn, field_validator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
    )

    REDIS_URL: RedisDsn
    DATABASE_URL: PostgresDsn
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
    
settings = Settings() # pyright: ignore[reportCallIssue]