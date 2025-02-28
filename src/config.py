from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn = "postgresql://postgres:postgres@db:5432/postgres"
    TELEGRAM_TOKEN: str

    class Config:
        env_file = ".env"


settings = Settings()