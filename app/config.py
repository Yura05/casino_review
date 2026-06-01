"""Konfiguracja aplikacji — wczytywana ze zmiennych środowiskowych / pliku .env."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    database_url: str = (
        "postgresql+psycopg2://postgres:postgres@localhost:5432/casino_review"
    )

    # Site
    site_name: str = "Casino Review"
    site_url: str = "http://localhost:8000"

    # Dev
    debug: bool = True


settings = Settings()
