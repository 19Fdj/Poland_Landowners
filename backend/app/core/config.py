from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = Field(default="sqlite+pysqlite:///./app.db", alias="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    backend_cors_origins: list[str] = Field(default=["http://localhost:3000"], alias="BACKEND_CORS_ORIGINS")
    demo_mode: bool = Field(default=True, alias="DEMO_MODE")
    legal_disclaimer_text: str = Field(
        default="This tool supports lawful due diligence only.",
        alias="LEGAL_DISCLAIMER_TEXT",
    )
    map_style_url: str = Field(
        default="https://demotiles.maplibre.org/style.json",
        alias="MAP_STYLE_URL",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

