from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = Field(default="sqlite+pysqlite:///./app.db", alias="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    backend_cors_origins_raw: str = Field(
        default="http://localhost:3000",
        alias="BACKEND_CORS_ORIGINS",
    )
    demo_mode: bool = Field(default=True, alias="DEMO_MODE")
    legal_disclaimer_text: str = Field(
        default="This tool supports lawful due diligence only.",
        alias="LEGAL_DISCLAIMER_TEXT",
    )
    parcel_connector: str = Field(default="auto", alias="PARCEL_CONNECTOR")
    uldk_base_url: str = Field(default="https://uldk.gugik.gov.pl", alias="ULDK_BASE_URL")
    uldk_timeout_seconds: float = Field(default=20.0, alias="ULDK_TIMEOUT_SECONDS")
    map_style_url: str = Field(
        default="https://demotiles.maplibre.org/style.json",
        alias="MAP_STYLE_URL",
    )

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: Any) -> Any:
        if isinstance(value, str) and value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        return value

    @property
    def backend_cors_origins(self) -> list[str]:
        stripped = self.backend_cors_origins_raw.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            inner = stripped[1:-1].strip()
            if not inner:
                return []
            return [item.strip().strip("\"'") for item in inner.split(",") if item.strip()]
        return [item.strip() for item in stripped.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
