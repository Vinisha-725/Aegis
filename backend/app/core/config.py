from __future__ import annotations

from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ─────────────────────────────────────────────────────────────────
    environment: str = "development"
    log_level: str = "INFO"
    secret_key: str = "CHANGE_ME_super_secret_key_at_least_32_chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # ── Database ─────────────────────────────────────────────────────────────
    postgres_user: str = "aegis"
    postgres_password: str = "aegis_dev_password"
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "aegis_db"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url_sync(self) -> str:
        """Synchronous URL used by Alembic."""
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # ── GitHub OAuth ──────────────────────────────────────────────────────────
    github_client_id: str = ""
    github_client_secret: str = ""
    github_redirect_uri: str = "http://localhost:3000/auth/callback"
    github_token: str = ""

    # ── Anthropic ─────────────────────────────────────────────────────────────
    anthropic_api_key: str = ""

    # ── Solana ────────────────────────────────────────────────────────────────
    solana_network: str = "devnet"
    solana_rpc_url: str = "https://api.devnet.solana.com"

    # ── Frontend ──────────────────────────────────────────────────────────────
    next_public_app_url: str = "http://localhost:3000"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
