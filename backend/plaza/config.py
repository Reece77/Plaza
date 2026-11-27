"""Runtime settings (paths, environment variables). Never imported by `plaza.sim`.

Adapted from Partner Track's `ptk/config.py`: the prefix is `PLAZA_`, and the data folder is
`backend/plaza/data`.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PACKAGE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = PACKAGE_DIR.parent
REPO_DIR = BACKEND_DIR.parent
SQLITE_SYNC_ENV = "PLAZA_SQLITE_SYNC"  # OFF skips fsync for throwaway saves (tests)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PLAZA_",
        env_file=(REPO_DIR / ".env", BACKEND_DIR / ".env"),
        extra="ignore",
    )

    save_dir: Path = REPO_DIR / "saves"
    # The built front end (frontend/dist) the API serves on its own port, so the launcher
    # needs one server; unset, the API serves only /api (Vite serves the front end).
    frontend_dir: Path | None = None
    data_dir: Path = PACKAGE_DIR / "data"
    # PLAZA_LLM_ADAPTER forces "claude", "templates" or "mock" (tests use mock); the key comes
    # from ANTHROPIC_API_KEY in the environment or .env and is never stored or returned.
    llm_adapter: str | None = None
    anthropic_api_key: str | None = Field(
        default=None, validation_alias=AliasChoices("ANTHROPIC_API_KEY", "PLAZA_ANTHROPIC_API_KEY")
    )

    def resolved_save_dir(self) -> Path:
        """Relative PLAZA_SAVE_DIR values are resolved against the repository root."""
        path = self.save_dir
        return path if path.is_absolute() else (REPO_DIR / path).resolve()


@lru_cache
def get_settings() -> Settings:
    return Settings()
