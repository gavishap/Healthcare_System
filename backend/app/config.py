from functools import lru_cache
from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore", env_file_encoding="utf-8")
    openai_api_key: SecretStr = SecretStr("")
    ncbi_api_key: SecretStr = SecretStr("")
    openai_model: str = "gpt-4.1-mini"
    ncbi_email: str = ""
    database_url: SecretStr = SecretStr(
        "postgresql+psycopg://evidence:evidence_local@127.0.0.1:55432/evidence"
    )
    app_access_token: SecretStr = SecretStr("")
    allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    max_records: int = 16
    source_timeout_seconds: float = 15
    run_timeout_seconds: float = 150
    max_active_runs: int = 2

    def model_name(self) -> str:
        return self.openai_model.strip() or "gpt-4.1-mini"


@lru_cache
def get_settings() -> Settings:
    return Settings()
