from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str = ""
    gemini_api_key: str = ""
    playwright_headless: bool = True
    allowed_origins: str = "http://localhost:3000"
    rate_limit_per_minute: int = 5
    rate_limit_window_seconds: int = 60

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    @property
    def allowed_origins_list(self) -> list[str]:
        return [item.strip() for item in self.allowed_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
