"""Plaza's sub-states and new game (SC-0003; spec 2.1; questions 16)."""

from __future__ import annotations

import pytest
from simcore.state import decode_state, encode_state, state_digest

from plaza.sim.books import DIRTY, DIRTY_CASH, DIRTY_EQUITY
from plaza.sim.data_models import GameData
from plaza.sim.errors import UnknownBackgroundError, UnknownDifficultyError
from plaza.sim.setup import new_game
from plaza.sim.state import REGISTRY, Organisation, SaveInfo
from tests.support import BACKGROUNDS


def _new(data: GameData, **kw: object) -> object:
    args: dict[str, object] = {
        "name": "t",
        "master_seed": 9,
        "org_name": "The Organisation",
        "leader_name": "The Leader",
        "background": "fixer",
        "scenario_id": "standard",
        "difficulty": "boss",
        "ironman": False,
        "data": data,
    }
    args.update(kw)
    return new_game(**args)  # type: ignore[arg-type]


@pytest.mark.parametrize("background", BACKGROUNDS)
def test_new_game_in_january_2006_with_a_dirty_stake(data: GameData, background: str) -> None:
    game = _new(data, background=background)
    state = game.state  # type: ignore[attr-defined]
    assert state.turn == 0 and state.meta.start_ym == (2006, 1) and state.meta.game == "plaza"
    assert state.sub(Organisation).background == background
    assert state.sub(SaveInfo).campaign_turns == 360 and not state.sub(SaveInfo).ironman
    (stake,) = game.ledger_entries  # type: ignore[attr-defined]
    assert stake.book == DIRTY
    assert {(ln.account, ln.amount) for ln in stake.lines} == {
        (DIRTY_CASH, data.balance.start.dirty_stake_cents),
        (DIRTY_EQUITY, -data.balance.start.dirty_stake_cents),
    }


def test_unknown_choices_are_refused(data: GameData) -> None:
    with pytest.raises(UnknownBackgroundError):
        _new(data, background="astronaut")
    with pytest.raises(UnknownDifficultyError):
        _new(data, difficulty="tycoon")


def test_state_round_trips_through_the_codec(data: GameData) -> None:
    state = _new(data, ironman=True).state  # type: ignore[attr-defined]
    again = decode_state(REGISTRY, encode_state(state))
    assert again == state and state_digest(again) == state_digest(state)
    assert [s.key for s in REGISTRY.specs] == ["organisation", "save"]
