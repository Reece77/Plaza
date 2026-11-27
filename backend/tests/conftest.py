from __future__ import annotations

import os
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BACKEND_DIR.parent
DATA_DIR = BACKEND_DIR / "plaza" / "data"

# Never call the Anthropic API in tests (CLAUDE.md section 10).
os.environ["PLAZA_LLM_ADAPTER"] = "mock"
os.environ.pop("ANTHROPIC_API_KEY", None)
os.environ.setdefault("PLAZA_SQLITE_SYNC", "OFF")

from plaza.loader import load_game_data  # noqa: E402
from plaza.sim.data_models import GameData  # noqa: E402


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--update-state-cache",
        action="store_true",
        default=False,
        help="Re-record tests/fixtures/state_cache.json (record the reason in CHANGELOG.md)",
    )


@pytest.fixture(scope="session")
def data() -> GameData:
    return load_game_data(DATA_DIR)


@pytest.fixture
def save_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "saves"
    monkeypatch.setenv("PLAZA_SAVE_DIR", str(path))
    from plaza.config import get_settings

    get_settings.cache_clear()
    yield path
    get_settings.cache_clear()
