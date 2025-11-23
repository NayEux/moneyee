from pydantic_settings import BaseSettings
from pydantic import AnyUrl
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Moneyee Advisor"
    secret_key: str = "changeme-secret"
    access_token_expire_minutes: int = 60 * 24
    algorithm: str = "HS256"
    database_url: AnyUrl | str = "sqlite:///./app.db"
    allow_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
