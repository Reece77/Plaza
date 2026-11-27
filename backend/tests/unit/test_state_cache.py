"""The state cache (TST M30's pattern): the state digest of the pure sim at fixed months for
seeds 1-3, recorded in tests/fixtures/state_cache.json. Re-record with
`uv run pytest tests/unit/test_state_cache.py --update-state-cache` and the reason in
CHANGELOG.md. The repeat check (two plays agree) runs either way."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from simcore.state import state_digest

from plaza.sim.data_models import GameData
from tests.support import play

CACHE = Path(__file__).resolve().parents[1] / "fixtures" / "state_cache.json"
SEEDS = (1, 2, 3)
TURNS = (0, 11, 59, 119, 239, 359)


def digests(data: GameData, seed: int) -> dict[str, str]:
    played = play(data, seed, max(TURNS) + 1)
    return {str(t): state_digest(played.results[t].new_state) for t in TURNS}


def test_state_cache(data: GameData, request: pytest.FixtureRequest) -> None:
    got = {str(seed): digests(data, seed) for seed in SEEDS}
    assert got == {str(seed): digests(data, seed) for seed in SEEDS}, "two plays differ"
    if request.config.getoption("--update-state-cache"):
        CACHE.write_text(json.dumps(got, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    assert CACHE.is_file(), "no state cache: run with --update-state-cache"
    assert json.loads(CACHE.read_text(encoding="utf-8")) == got
