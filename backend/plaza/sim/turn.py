"""The monthly turn (ADR PL-0002 section 5; sim-core's phase registry, SC-0005).

Plaza's twelve phases fill sim-core's twelve slots one each, in PL-0002's order, so the slot
order is the phase order and `describe()` prints it (guarded by tests/unit/test_turn_order.py).
Every phase is a pure `TurnContext -> TurnContext`. At PL-M0 all but `snapshot` are no-ops;
each later milestone gives its phase a body and never moves it.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Final

from simcore.interfaces import build_snapshot
from simcore.kernel.ledger import LedgerBalances
from simcore.kernel.rng import RngFactory
from simcore.state import CoreState
from simcore.turn import Phase, PhaseRegistry, TurnContext, TurnResult
from simcore.turn import advance_turn as run_phases

from plaza.sim.books import chart, check_declared
from plaza.sim.data_models import GameData
from plaza.sim.decisions import Decisions
from plaza.sim.errors import GameOverError
from plaza.sim.interfaces import CashKpis
from plaza.sim.state import CAMPAIGN_COMPLETE, PLAYER_ORG_ID, SaveInfo, is_active, last_turn


def world_and_policy_shocks(ctx: TurnContext) -> TurnContext:
    """1. Dated policy and enforcement shocks to 2025, seeded after (PL-M13)."""
    return ctx


def agency(ctx: TurnContext) -> TurnContext:
    """2. The agency's month; its budget and targets each December (PL-M5)."""
    return ctx


def rivals(ctx: TurnContext) -> TurnContext:
    """3. Rival organisations decide (PL-M7)."""
    return ctx


def production(ctx: TurnContext) -> TurnContext:
    """4. Sites produce at their capacity and quality tier (PL-M3b)."""
    return ctx


def logistics(ctx: TurnContext) -> TurnContext:
    """5. Flows move and named shipments resolve (PL-M3c)."""
    return ctx


def markets_and_sales(ctx: TurnContext) -> TurnContext:
    """6. Sales by market and plaza tax into the dirty book (PL-M3a, PL-M3b)."""
    return ctx


def laundering(ctx: TurnContext) -> TurnContext:
    """7. Value crosses from the dirty book to the clean one through fronts (PL-M4)."""
    return ctx


def heat(ctx: TurnContext) -> TurnContext:
    """8. Heat rises from activity and decays slowly (PL-M5)."""
    return ctx


def people(ctx: TurnContext) -> TurnContext:
    """9. Morale, growth and informants (PL-M1a, PL-M1b, PL-M5)."""
    return ctx


def council(ctx: TurnContext) -> TurnContext:
    """10. The council's confidence; its meeting each December (PL-M6)."""
    return ctx


def events(ctx: TurnContext) -> TurnContext:
    """11. The event director (PL-M8)."""
    return ctx


def snapshot(ctx: TurnContext) -> TurnContext:
    """12. The month-end snapshot from the KPI providers, on the closing balances."""
    snap = build_snapshot(ctx.state, (CashKpis(ctx.balances),), (PLAYER_ORG_ID,))
    return replace(ctx, snapshot=snap)


# (slot, phase): sim-core's slots in their order, one Plaza phase each (PL-0002 section 5).
PHASES: Final[tuple[tuple[str, str, Phase], ...]] = (
    ("decisions", "world_and_policy_shocks", world_and_policy_shocks),
    ("actors", "agency", agency),
    ("progress", "rivals", rivals),
    ("operations", "production", production),
    ("revenue", "logistics", logistics),
    ("costs", "markets_and_sales", markets_and_sales),
    ("financing", "laundering", laundering),
    ("people", "heat", heat),
    ("world", "people", people),
    ("checks", "council", council),
    ("report", "events", events),
    ("requests", "snapshot", snapshot),
)


def phase_registry() -> PhaseRegistry:
    reg = PhaseRegistry()
    for slot, name, fn in PHASES:
        reg.register(slot, name, fn)
    reg.freeze()
    return reg


REGISTRY: Final = phase_registry()


def advance_turn(
    state: CoreState,
    decisions: Decisions,
    rng: RngFactory,
    data: GameData,
    balances: LedgerBalances,
) -> TurnResult:
    """Play one month. Pure: the same state, decisions, seed, data and balances always give
    the same result. After the campaign's last month the save is complete; a further turn
    raises GameOverError."""
    if not is_active(state):
        raise GameOverError(f"the campaign ended on turn {state.sub(SaveInfo).ended_turn}")
    played = state.turn
    result = run_phases(
        REGISTRY,
        state,
        decisions,
        rng,
        balance=data.balance,
        data=data,
        chart=chart(data.balance),
        balances=balances,
    )
    check_declared(result.ledger_entries, data.accounts)
    if played < last_turn(state):
        return result
    info = result.new_state.sub(SaveInfo)
    done = result.new_state.with_meta(status=CAMPAIGN_COMPLETE)
    return replace(result, new_state=done.with_sub(replace(info, ended_turn=played)))
