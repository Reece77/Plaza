"""ADR PL-0003 on sim-core's ledger: every entry balances within one book, only the
laundering bridge crosses books, and in each book assets = liabilities + equity (with the
period's income less costs) after every month."""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from simcore.kernel.errors import BookError, UnbalancedEntryError
from simcore.kernel.ledger import LedgerEntry, LedgerLine, apply_entries, bridge_transfer

from plaza.loader import load_game_data
from plaza.sim.books import CLEAN, DIRTY, LAUNDER, chart, check_declared, totals_by_type
from plaza.sim.data_models import GameData
from tests.conftest import DATA_DIR

DATA: GameData = load_game_data(DATA_DIR)
CHART = chart(DATA.balance)
ORG = 1
CODES = {
    book: [a.code for a in DATA.accounts.accounts if a.book == book] for book in (DIRTY, CLEAN)
}
amounts = st.integers(min_value=1, max_value=10**11)


@st.composite
def entry_in(draw: st.DrawFn, book: str, turn: int = 0) -> LedgerEntry:
    """A balanced entry of 2-5 lines, all on accounts of one book."""
    n = draw(st.integers(min_value=1, max_value=4))
    accounts = draw(st.lists(st.sampled_from(CODES[book]), min_size=n + 1, max_size=n + 1))
    parts = draw(st.lists(amounts, min_size=n, max_size=n))
    lines = [LedgerLine(a, v) for a, v in zip(accounts, parts, strict=False)]
    lines.append(LedgerLine(accounts[-1], -sum(parts)))
    return LedgerEntry(turn, ORG, "test", tuple(lines), book=book if book == DIRTY else "")


def check_equation(balances: dict[tuple[int, str, str], int]) -> None:
    for book in (DIRTY, CLEAN):
        t = totals_by_type(balances, ORG, DATA.accounts, book)
        # debits positive: assets + costs == -(liabilities + equity + income)
        assert t["asset"] == -(t["liability"] + t["equity"] + (t["income"] + t["cost"]))


@given(book=st.sampled_from([DIRTY, CLEAN]), data=st.data())
def test_an_entry_balances_within_its_book(book: str, data: st.DataObject) -> None:
    entry = data.draw(entry_in(book))
    CHART.check(entry)
    check_declared((entry,), DATA.accounts)
    assert sum(line.amount for line in entry.lines) == 0
    check_equation(apply_entries({}, (entry,), CHART))


@given(dirty=st.sampled_from(CODES[DIRTY]), clean=st.sampled_from(CODES[CLEAN]), amount=amounts)
def test_an_entry_across_books_is_refused(dirty: str, clean: str, amount: int) -> None:
    for book in (DIRTY, ""):
        entry = LedgerEntry.transfer(
            turn=0, entity_id=ORG, memo="x", debit=dirty, credit=clean, amount=amount, book=book
        )
        with pytest.raises(BookError):
            CHART.check(entry)
        with pytest.raises(BookError):
            apply_entries({}, (entry,), CHART)


@given(amount=amounts)
def test_an_unbalanced_entry_is_refused(amount: int) -> None:
    with pytest.raises(UnbalancedEntryError):
        LedgerEntry(
            0,
            ORG,
            "x",
            (LedgerLine("D1000_cash", amount), LedgerLine("D3000_leader_equity", -amount + 1)),
            book=DIRTY,
        )


@given(amount=amounts)
def test_the_bridge_is_two_linked_single_book_entries(amount: int) -> None:
    t = bridge_transfer(
        CHART, LAUNDER, turn=0, entity_id=ORG, memo="launder", amount=amount, link="l-1"
    )
    assert t.sent.book == DIRTY and (t.received.book or CLEAN) == CLEAN
    assert t.sent.link == t.received.link == "l-1"
    for entry in (t.sent, t.received):
        CHART.check(entry)
        assert sum(ln.amount for ln in entry.lines) == 0
    check_declared((t.sent, t.received), DATA.accounts)
    arrived = sum(ln.amount for ln in t.received.lines if ln.amount > 0)
    assert arrived + t.leaked == amount and t.leaked >= 0


@settings(max_examples=60)
@given(data=st.data(), months=st.integers(min_value=1, max_value=24))
def test_both_books_balance_every_month(data: st.DataObject, months: int) -> None:
    """A random history of single-book entries and bridges: after every month each book still
    satisfies the accounting equation, and the only entries that move value between books
    are the linked pairs of the declared bridge."""
    balances: dict[tuple[int, str, str], int] = {}
    for turn in range(months):
        entries: list[LedgerEntry] = []
        for _ in range(data.draw(st.integers(min_value=0, max_value=3))):
            entries.append(data.draw(entry_in(data.draw(st.sampled_from([DIRTY, CLEAN])), turn)))
        if data.draw(st.booleans()):
            t = bridge_transfer(
                CHART,
                LAUNDER,
                turn=turn,
                entity_id=ORG,
                memo="launder",
                amount=data.draw(amounts),
                link=f"l-{turn}",
            )
            entries += [t.sent, t.received]
        check_declared(entries, DATA.accounts)
        balances = apply_entries(balances, entries, CHART)
        check_equation(balances)
        linked = [e for e in entries if e.link is not None]
        assert len(linked) in (0, 2)
        if linked:
            assert {e.book or CLEAN for e in linked} == {DIRTY, CLEAN}
