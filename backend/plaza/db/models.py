"""SQLAlchemy tables for one save file (TST ADR-0004). Column reference:
docs/data-dictionary.md. Schema v1 (migration 0001).

History tables (ledger, snapshots, turn log) are append-only; current-state tables
(save_meta, organisation) are updated in place.
"""

from __future__ import annotations

from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SaveMetaRow(Base):
    __tablename__ = "save_meta"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # always 1
    name: Mapped[str] = mapped_column(String(80))
    game: Mapped[str] = mapped_column(String(20))
    master_seed: Mapped[int] = mapped_column(BigInteger)  # stored minus 2**63; see state_io
    start_year: Mapped[int] = mapped_column(Integer)
    start_month: Mapped[int] = mapped_column(Integer)
    start_turn: Mapped[int] = mapped_column(Integer)
    current_turn: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20))
    scenario_id: Mapped[str] = mapped_column(String(40))
    difficulty: Mapped[str] = mapped_column(String(20))
    ironman: Mapped[bool] = mapped_column(Boolean)
    campaign_turns: Mapped[int] = mapped_column(Integer)
    ended_turn: Mapped[int | None] = mapped_column(Integer, nullable=True)


class OrganisationRow(Base):
    __tablename__ = "organisation"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    leader_name: Mapped[str] = mapped_column(String(120))
    background: Mapped[str] = mapped_column(String(40))
    is_player: Mapped[bool] = mapped_column(Boolean)


class LedgerEntryRow(Base):
    __tablename__ = "ledger_entry"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    turn: Mapped[int] = mapped_column(Integer, index=True)
    entity_id: Mapped[int] = mapped_column(ForeignKey("organisation.id"), index=True)
    book: Mapped[str] = mapped_column(String(20), index=True)
    memo: Mapped[str] = mapped_column(Text)
    link: Mapped[str | None] = mapped_column(String(80), nullable=True)


class LedgerLineRow(Base):
    __tablename__ = "ledger_line"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("ledger_entry.id"), index=True)
    account: Mapped[str] = mapped_column(String(40), index=True)
    amount_cents: Mapped[int] = mapped_column(BigInteger)
    currency: Mapped[str] = mapped_column(String(3))
    dims_json: Mapped[str] = mapped_column(Text)


class TurnSnapshotRow(Base):
    __tablename__ = "turn_snapshot"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    turn: Mapped[int] = mapped_column(Integer, index=True)
    entity_id: Mapped[int] = mapped_column(ForeignKey("organisation.id"), index=True)
    kpis_json: Mapped[str] = mapped_column(Text)


class TurnLogRow(Base):
    __tablename__ = "turn_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    turn: Mapped[int] = mapped_column(Integer, index=True)
    entity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    kind: Mapped[str] = mapped_column(String(60))
    message: Mapped[str] = mapped_column(Text)
    template: Mapped[str | None] = mapped_column(String(60), nullable=True)
    params_json: Mapped[str] = mapped_column(Text)
    link_kind: Mapped[str | None] = mapped_column(String(40), nullable=True)
    link_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
