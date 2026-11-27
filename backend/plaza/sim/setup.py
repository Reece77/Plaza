"""New game: the January 2006 state and the starting entry (spec 2.1; questions 16).

The organisation starts with a small dirty-cash stake (debit dirty cash, credit the leader's
equity, both in the dirty book) and an empty clean book.
"""

from __future__ import annotations

from dataclasses import dataclass

from simcore.kernel.ledger import LedgerEntry
from simcore.kernel.rng import check_seed
from simcore.state import CoreState, SaveMeta

from plaza.sim.books import DIRTY, DIRTY_CASH, DIRTY_EQUITY, check_declared
from plaza.sim.data_models import GameData
from plaza.sim.errors import (
    UnknownBackgroundError,
    UnknownDifficultyError,
    UnknownScenarioError,
)
from plaza.sim.state import GAME, PLAYER_ORG_ID, Organisation, SaveInfo, new_state


@dataclass(frozen=True, slots=True)
class NewGame:
    state: CoreState
    ledger_entries: tuple[LedgerEntry, ...]


def new_game(
    *,
    name: str,
    master_seed: int,
    org_name: str,
    leader_name: str,
    background: str,
    scenario_id: str,
    difficulty: str,
    ironman: bool,
    data: GameData,
) -> NewGame:
    scenarios = data.scenarios
    scenario = scenarios.scenario(scenario_id)
    if scenario is None:
        raise UnknownScenarioError(f"unknown scenario {scenario_id!r}")
    if scenarios.difficulty(difficulty) is None:
        raise UnknownDifficultyError(f"unknown difficulty {difficulty!r}")
    if scenarios.background(background) is None:
        raise UnknownBackgroundError(f"unknown background {background!r}")
    start = scenario.start_ym
    meta = SaveMeta(
        name=name,
        master_seed=check_seed(master_seed),
        game=GAME,
        start_ym=start,
        start_turn=0,  # turn 0 is the scenario's first month (ADR PL-0002 section 1)
    )
    state = (
        new_state(meta)
        .with_sub(
            Organisation(
                id=PLAYER_ORG_ID, name=org_name, leader_name=leader_name, background=background
            )
        )
        .with_sub(
            SaveInfo(
                scenario_id=scenario.id,
                difficulty=difficulty,
                ironman=ironman,
                campaign_turns=scenario.campaign_turns,
            )
        )
    )
    stake = LedgerEntry.transfer(
        turn=meta.start_turn,
        entity_id=PLAYER_ORG_ID,
        memo="Starting stake",
        debit=DIRTY_CASH,
        credit=DIRTY_EQUITY,
        amount=data.balance.start.dirty_stake_cents,
        book=DIRTY,
    )
    check_declared((stake,), data.accounts)
    return NewGame(state=state, ledger_entries=(stake,))
