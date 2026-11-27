"""Plaza's two books on sim-core's multi-book ledger (ADR PL-0003; SC-0004).

`dirty` holds every trafficking income and cost; `clean` holds fronts, legitimate assets and
the leader's lawful wealth. Every entry belongs to one book and only the `launder` bridge
crosses them: the dirty book sends the whole amount, the clean book receives it less
leakage (sim-core's `bridge_transfer`). The fee is a separate dirty-book cost that PL-M4
posts when fronts arrive; both rates are data in balance.yaml, unused until then.

sim-core needs exactly one book with the empty prefix (the default). `clean` is that book,
as in sim-core's Plaza-shaped consumer; `plaza.sim.data_models.Account` still requires every
clean code to start with "C", and `check_declared` refuses any account accounts.yaml does
not list, so a mistyped code cannot fall silently into the clean book.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Final

from simcore.kernel.errors import BookError
from simcore.kernel.ledger import (
    Book,
    BookBridge,
    Chart,
    LedgerBalances,
    LedgerEntry,
    account_balance,
)
from simcore.kernel.money import Cents

from plaza.sim.data_models import Accounts, AccountType, Balance

# Account codes the engine posts to (accounts.yaml names them all; never renumber).
DIRTY_CASH: Final = "D1000_cash"
DIRTY_EQUITY: Final = "D3000_leader_equity"
DIRTY_LAUNDERED_OUT: Final = "D5900_laundered_out"
CLEAN_CASH: Final = "C1000_cash"
CLEAN_LAUNDERED_IN: Final = "C4900_laundered_in"

DIRTY: Final = "dirty"
CLEAN: Final = "clean"
LAUNDER: Final = "launder"


def chart(balance: Balance) -> Chart:
    """The chart of books, with the laundering bridge's leakage from balance.yaml."""
    return Chart(
        books=(Book(CLEAN, "", owner="entity"), Book(DIRTY, "D", owner="entity")),
        bridges=(
            BookBridge(
                LAUNDER,
                from_book=DIRTY,
                to_book=CLEAN,
                from_account=DIRTY_CASH,
                from_contra=DIRTY_LAUNDERED_OUT,
                to_account=CLEAN_CASH,
                to_contra=CLEAN_LAUNDERED_IN,
                leakage_bp=balance.laundering.leakage_bp,
            ),
        ),
    )


def check_declared(entries: Iterable[LedgerEntry], accounts: Accounts) -> None:
    """Refuse an entry whose account accounts.yaml does not declare, or declares in the
    other book."""
    declared = accounts.by_code()
    for entry in entries:
        for line in entry.lines:
            account = declared.get(line.account)
            if account is None:
                raise BookError(f"entry {entry.memo!r}: account {line.account} is not declared")
            book = entry.book or CLEAN
            if account.book != book:
                raise BookError(
                    f"entry {entry.memo!r} is in book {book} but {line.account} is "
                    f"declared in book {account.book}"
                )


def cash(balances: LedgerBalances, entity_id: int) -> tuple[Cents, Cents]:
    """(dirty cash, clean cash) for one entity."""
    return (
        account_balance(balances, entity_id, DIRTY_CASH),
        account_balance(balances, entity_id, CLEAN_CASH),
    )


def totals_by_type(
    balances: LedgerBalances, entity_id: int, accounts: Accounts, book: str
) -> Mapping[AccountType, Cents]:
    """One book's balances summed by account type, debit positive (the accounting equation:
    asset + cost + liability + equity + income == 0, i.e. assets = liabilities + equity +
    current earnings, with credits negative)."""
    declared = accounts.by_code()
    out: dict[AccountType, Cents] = {
        "asset": 0,
        "liability": 0,
        "equity": 0,
        "income": 0,
        "cost": 0,
    }
    for (eid, code, _currency), amount in sorted(balances.items()):
        account = declared.get(code)
        if eid == entity_id and account is not None and account.book == book:
            out[account.type] += amount
    return out
