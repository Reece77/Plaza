"""Seed and balance data load through sim-core's DataRegistry; invalid data fails."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from simcore.kernel.errors import InvalidDataError

from plaza.loader import load_game_data
from plaza.sim.data_models import GameData

DATA = Path(__file__).resolve().parents[2] / "plaza" / "data"


def test_data_loads(data: GameData) -> None:
    s = data.scenarios
    assert [d.id for d in s.difficulties] == ["lieutenant", "boss", "kingpin"]
    assert [b.id for b in s.backgrounds] == [
        "smuggler",
        "producer",
        "enforcer",
        "accountant",
        "fixer",
    ]
    assert data.balance.start.dirty_stake_cents > 0
    books = {a.book for a in data.accounts.accounts}
    assert books == {"dirty", "clean"}


@pytest.mark.parametrize(
    ("file", "old", "new"),
    [
        ("balance.yaml", "dirty_stake_cents: 10000000", "dirty_stake_cents: -1"),
        ("accounts.yaml", "C1000_cash, name", "D1999_cash, name"),  # a dirty code in the clean book
        ("scenarios.yaml", "default_difficulty: boss", "default_difficulty: tycoon"),
        ("scenarios.yaml", "start_ym: [2006, 1]", "start_ym: [2006, 13]"),
    ],
)
def test_invalid_data_fails_at_load(tmp_path: Path, file: str, old: str, new: str) -> None:
    folder = tmp_path / "data"
    shutil.copytree(DATA, folder)
    text = (folder / file).read_text(encoding="utf-8")
    assert old in text
    (folder / file).write_text(text.replace(old, new), encoding="utf-8")
    with pytest.raises(InvalidDataError):
        load_game_data(folder)
