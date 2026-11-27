"""Plaza's game state: a sim-core `CoreState` with Plaza's registered sub-states (SC-0003).

At PL-M0 the state holds the save's own settings and the player's organisation, and nothing
else: people, territory, products and the rest arrive with their milestones, each as its own
sub-state. The core `SaveMeta` carries the save name, master seed, game id, the month of
turn 0 (`start_ym`), the first turn and the status ("active" or "campaign_complete").
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from simcore.state import CoreState, SaveMeta, SubStateRegistry, SubStateSpec

GAME: Final = "plaza"
PLAYER_ORG_ID: Final = 1
ACTIVE: Final = "active"
CAMPAIGN_COMPLETE: Final = "campaign_complete"


@dataclass(frozen=True, slots=True)
class SaveInfo:
    """The choices made at New game that are not the core's (spec 17; ADR PL-0011)."""

    scenario_id: str = ""
    difficulty: str = ""
    ironman: bool = False
    campaign_turns: int = 0
    ended_turn: int | None = None


@dataclass(frozen=True, slots=True)
class Organisation:
    """The player's organisation (spec 2.1): its name, the leader's name and background."""

    id: int = PLAYER_ORG_ID
    name: str = ""
    leader_name: str = ""
    background: str = ""


SPECS: Final = (
    SubStateSpec("organisation", Organisation, Organisation()),
    SubStateSpec("save", SaveInfo, SaveInfo()),
)

REGISTRY: Final = SubStateRegistry(SPECS).freeze()


def new_state(meta: SaveMeta) -> CoreState:
    return REGISTRY.new_state(meta)


def is_active(state: CoreState) -> bool:
    return state.meta.status == ACTIVE


def last_turn(state: CoreState) -> int:
    """The campaign's final turn (December 2035 for the standard campaign)."""
    return state.meta.start_turn + state.sub(SaveInfo).campaign_turns - 1
