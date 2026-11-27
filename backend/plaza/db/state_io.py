"""The save mapper: Plaza's tables <-> sim-core's `CoreState`, and a turn's writes
(TST ADR-0004). `tests/integration/test_saves.py` checks that a state read back from the
tables encodes exactly as the state that was written (SC-0003's mapper contract)."""

from __future__ import annotations

import json
from collections.abc import Iterable

from simcore.interfaces import Snapshot
from simcore.kernel.ledger import DEFAULT_CURRENCY, LedgerEntry
from simcore.kernel.log import LogItem
from simcore.kernel.money import Cents
from simcore.state import CoreState, SaveMeta
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from plaza.db.models import (
    LedgerEntryRow,
    LedgerLineRow,
    OrganisationRow,
    SaveMetaRow,
    TurnLogRow,
    TurnSnapshotRow,
)
from plaza.sim.books import CLEAN
from plaza.sim.state import PLAYER_ORG_ID, Organisation, SaveInfo, new_state

META_ID = 1
_SIGN = 2**63  # SQLite integers are signed 64-bit; seeds are 0..2**64-1 (PT-M0)

type Balances = dict[tuple[int, str, str], Cents]


def seed_to_db(seed: int) -> int:
    return seed - _SIGN


def seed_from_db(value: int) -> int:
    return value + _SIGN


def insert_new(session: Session, state: CoreState, entries: Iterable[LedgerEntry]) -> None:
    meta, info, org = state.meta, state.sub(SaveInfo), state.sub(Organisation)
    session.add(
        SaveMetaRow(
            id=META_ID,
            name=meta.name,
            game=meta.game,
            master_seed=seed_to_db(meta.master_seed),
            start_year=meta.start_ym[0],
            start_month=meta.start_ym[1],
            start_turn=meta.start_turn,
            current_turn=state.turn,
            status=meta.status,
            scenario_id=info.scenario_id,
            difficulty=info.difficulty,
            ironman=info.ironman,
            campaign_turns=info.campaign_turns,
            ended_turn=info.ended_turn,
        )
    )
    session.add(
        OrganisationRow(
            id=org.id,
            name=org.name,
            leader_name=org.leader_name,
            background=org.background,
            is_player=org.id == PLAYER_ORG_ID,
        )
    )
    session.flush()
    write_entries(session, entries)


def load_state(session: Session) -> CoreState:
    row = session.get(SaveMetaRow, META_ID)
    if row is None:
        raise LookupError("save has no save_meta row")
    org = session.get(OrganisationRow, PLAYER_ORG_ID)
    if org is None:
        raise LookupError("save has no player organisation")
    meta = SaveMeta(
        name=row.name,
        master_seed=seed_from_db(row.master_seed),
        game=row.game,
        start_ym=(row.start_year, row.start_month),
        start_turn=row.start_turn,
        status=row.status,
    )
    return (
        new_state(meta)
        .with_turn(row.current_turn)
        .with_sub(
            SaveInfo(
                scenario_id=row.scenario_id,
                difficulty=row.difficulty,
                ironman=row.ironman,
                campaign_turns=row.campaign_turns,
                ended_turn=row.ended_turn,
            )
        )
        .with_sub(
            Organisation(
                id=org.id, name=org.name, leader_name=org.leader_name, background=org.background
            )
        )
    )


def ledger_balances(session: Session) -> Balances:
    stmt = (
        select(
            LedgerEntryRow.entity_id,
            LedgerLineRow.account,
            LedgerLineRow.currency,
            func.sum(LedgerLineRow.amount_cents),
        )
        .join(LedgerEntryRow, LedgerLineRow.entry_id == LedgerEntryRow.id)
        .group_by(LedgerEntryRow.entity_id, LedgerLineRow.account, LedgerLineRow.currency)
    )
    return {
        (int(e), str(a), str(c)): int(total)
        for e, a, c, total in session.execute(stmt)
        if int(total)
    }


def write_entries(session: Session, entries: Iterable[LedgerEntry]) -> None:
    for entry in entries:
        row = LedgerEntryRow(
            turn=entry.turn,
            entity_id=entry.entity_id,
            book=entry.book or CLEAN,
            memo=entry.memo,
            link=entry.link,
        )
        session.add(row)
        session.flush()
        session.add_all(
            LedgerLineRow(
                entry_id=row.id,
                account=line.account,
                amount_cents=line.amount,
                currency=line.currency or DEFAULT_CURRENCY,
                dims_json=json.dumps(list(line.dims)),
            )
            for line in entry.lines
        )


def write_turn(
    session: Session,
    new_state: CoreState,
    entries: Iterable[LedgerEntry],
    log_items: Iterable[LogItem],
    snapshot: Snapshot | None,
) -> None:
    write_entries(session, entries)
    session.add_all(
        TurnLogRow(
            turn=i.turn,
            entity_id=i.entity_id,
            kind=i.kind,
            message=i.message,
            template=i.template,
            params_json=json.dumps(list(i.params)),
            link_kind=i.link_kind,
            link_id=i.link_id,
        )
        for i in log_items
    )
    if snapshot is not None:
        session.add_all(
            TurnSnapshotRow(
                turn=snapshot.turn, entity_id=e.entity_id, kpis_json=json.dumps(dict(e.kpis))
            )
            for e in snapshot.entities
        )
    meta = session.get(SaveMetaRow, META_ID)
    assert meta is not None
    info = new_state.sub(SaveInfo)
    meta.current_turn = new_state.turn
    meta.status = new_state.meta.status
    meta.ended_turn = info.ended_turn
