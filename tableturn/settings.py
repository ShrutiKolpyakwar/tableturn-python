"""
One settings object, read once at start-up.
Nothing is hard-coded. Every field has a default;
the environment can change it.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = Field("sqlite:///./tableturn.db", min_length=1)
    default_quote_minutes: int = Field(40, ge=1)
    seed_dir: str = Field("seed", min_length=1)
    host: str = Field("0.0.0.0", min_length=1)
    port: int = Field(8080, ge=1, le=65535)