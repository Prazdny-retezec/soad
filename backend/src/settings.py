import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = os.environ.get("DATABASE_URL")
    secret: str = os.environ.get("SECRET")

    # load settings from .env file
    model_config = SettingsConfigDict(env_file=".env")
