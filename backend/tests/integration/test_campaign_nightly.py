"""Nightly: seeds 1-10, a full headless campaign each with a cold reload every month, both
books balanced every month, ending in December 2035 (`make nightly`)."""

from __future__ import annotations

from pathlib import Path

import pytest

from plaza.db import saves
from plaza.sim.books import totals_by_type
from plaza.sim.data_models import GameData
from tests.support import BACKGROUNDS, make_save


@pytest.mark.nightly
@pytest.mark.parametrize("seed", range(1, 11))
def test_campaign(seed: int, save_dir: Path, data: GameData) -> None:
    path = make_save(
        save_dir, data, slug=f"n{seed}", seed=seed, background=BACKGROUNDS[seed % len(BACKGROUNDS)]
    )
    for turn in range(360):
        state, balances = saves.read_state(saves.open_save(save_dir, f"n{seed}"))
        assert state.turn == turn
        for book in ("dirty", "clean"):
            assert sum(totals_by_type(balances, 1, data.accounts, book).values()) == 0
        saves.run_turn(path, data)
    assert saves.read_state(path)[0].meta.status == "campaign_complete"
