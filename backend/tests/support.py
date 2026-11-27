"""Shared helpers for Plaza's tests: a new save, and playing the pure sim in memory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from simcore.kernel.ledger import apply_entries
from simcore.state import CoreState
from simcore.turn import TurnResult

from plaza.db import saves
from plaza.sim.books import chart
from plaza.sim.data_models import GameData
from plaza.sim.decisions import Decisions
from plaza.sim.setup import new_game
from plaza.sim.streams import rng_factory
from plaza.sim.turn import advance_turn

BACKGROUNDS = ("smuggler", "producer", "enforcer", "accountant", "fixer")


def make_save(save_dir: Path, data: GameData, slug: str = "t", seed: int = 7, **kw: object) -> Path:
    args: dict[str, object] = {
        "org_name": "The Organisation",
        "leader_name": "The Leader",
        "background": "smuggler",
    }
    args.update(kw)
    saves.create_save(save_dir, slug, data=data, seed=seed, **args)  # type: ignore[arg-type]
    return saves.open_save(save_dir, slug)


@dataclass
class Played:
    results: list[TurnResult]
    state: CoreState


def play(data: GameData, seed: int, turns: int, background: str = "smuggler") -> Played:
    """The pure sim alone, in memory: new game then `turns` months."""
    game = new_game(
        name=f"s{seed}",
        master_seed=seed,
        org_name="The Organisation",
        leader_name="The Leader",
        background=background,
        scenario_id=data.scenarios.default_scenario,
        difficulty=data.scenarios.default_difficulty,
        ironman=False,
        data=data,
    )
    balances = apply_entries({}, game.ledger_entries, chart(data.balance))
    state, rng, results = game.state, rng_factory(seed), []
    for _ in range(turns):
        result = advance_turn(state, Decisions(), rng, data, balances)
        results.append(result)
        state, balances = result.new_state, dict(result.balances)
    return Played(results, state)
