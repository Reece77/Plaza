"""Golden seeds 1-3 (TST ADR-0002): a new game advanced 360 empty months through the save
layer gives exactly the recorded results. Regenerate with `uv run pytest tests/golden
--update-golden` (sim-core's plugin) and record the reason in CHANGELOG.md.

Each file holds one record per December (turn 11, 23, ... 359) and a final record whose
sha256 covers every month's snapshot, entries and log in order."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest
from simcore.state import state_digest, sub_digests
from simcore_testing.golden import Golden

from plaza.db import saves
from plaza.sim.data_models import GameData
from tests.support import make_save

GOLDEN_DIR = Path(__file__).parent / "snapshots"
SEEDS = (1, 2, 3)


def records(path: Path, data: GameData) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    rolling = hashlib.sha256()
    for _ in range(360):
        result = saves.run_turn(path, data)
        assert result.snapshot is not None
        month = {
            "turn": result.snapshot.turn,
            "kpis": [[e.entity_id, [list(k) for k in e.kpis]] for e in result.snapshot.entities],
            "entries": [
                [e.book, e.memo, [[ln.account, ln.amount] for ln in e.lines]]
                for e in result.ledger_entries
            ],
            "log": [[i.kind, i.message] for i in result.log_items],
        }
        rolling.update(json.dumps(month, sort_keys=True).encode())
        if result.snapshot.turn % 12 == 11:
            state, balances = saves.read_state(path)
            out.append(
                {
                    "turn": result.snapshot.turn,
                    "digest": state_digest(state),
                    "subs": sub_digests(state),
                    "kpis": month["kpis"],
                    "balances": sorted([e, a, c, v] for (e, a, c), v in balances.items()),
                }
            )
    state, _ = saves.read_state(path)
    out.append(
        {"final_turn": state.turn, "status": state.meta.status, "sha256": rolling.hexdigest()}
    )
    return out


@pytest.mark.parametrize("seed", SEEDS)
def test_golden_seed(seed: int, save_dir: Path, data: GameData, golden: Golden) -> None:
    path = make_save(save_dir, data, slug=f"g{seed}", seed=seed)
    golden.check(f"seed_{seed}", records(path, data))
