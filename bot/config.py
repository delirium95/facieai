from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(BASE_DIR / '.env'), env_file_encoding='utf-8', extra="allow")

    telegram_bot_token: str = Field(alias="TELEGRAM_BOT_TOKEN")
    backend_base_url: str = Field(alias="BACKEND_BASE_URL")


config = Settings()