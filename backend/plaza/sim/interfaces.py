"""Where Plaza's domain packages meet, as implementations of `simcore.interfaces`
(ADR PL-0001 section 5; SC-0006).

PL-M0 has one: the cash KPIs. A KPI provider reads `(state, entity)`, so this one is built
for a month from that month's closing balances (the ledger is not part of the state).
"""

from __future__ import annotations

from collections.abc import Mapping

from simcore.interfaces import KpiValue
from simcore.kernel.ledger import LedgerBalances
from simcore.state import CoreState

from plaza.sim.books import cash

DIRTY_CASH_KPI = "dirty_cash_cents"
CLEAN_CASH_KPI = "clean_cash_cents"
CASH_KPIS = (CLEAN_CASH_KPI, DIRTY_CASH_KPI)


class CashKpis:
    """Dirty cash and clean cash, in cents, at the month's close."""

    key = "cash"

    def __init__(self, balances: LedgerBalances) -> None:
        self._balances = balances

    def kpis(self, state: CoreState, entity_id: int) -> Mapping[str, KpiValue]:
        del state
        dirty, clean = cash(self._balances, entity_id)
        return {DIRTY_CASH_KPI: dirty, CLEAN_CASH_KPI: clean}
