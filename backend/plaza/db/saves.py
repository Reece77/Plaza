"""Save files on `simcore_db`: create, list, open, and play a turn in one transaction
(TST ADR-0004; SC-0009). Adapted from Partner Track's `ptk/db/saves.py` at PT-M0.

One SQLite file per save (`<slug>.plaza.sqlite`), Plaza's own Alembic chain, one write lock
per save, and a periodic backup every `backups.every_turns` months after the turn commits.
"""

from __future__ import annotations

import json
import re
import secrets
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from simcore.kernel.calendar import format_turn
from simcore.kernel.rng import MAX_SEED
from simcore.state import CoreState
from simcore.turn import TurnResult
from simcore_db import backup
from simcore_db.migrate import Migrator
from simcore_db.session import make_sessionmaker, shared_engine
from simcore_db.turns import SaveLocks, run_in_transaction
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from plaza.config import BACKEND_DIR, SQLITE_SYNC_ENV
from plaza.db.models import (
    LedgerEntryRow,
    LedgerLineRow,
    OrganisationRow,
    SaveMetaRow,
    TurnSnapshotRow,
)
from plaza.db.state_io import (
    META_ID,
    Balances,
    insert_new,
    ledger_balances,
    load_state,
    write_turn,
)
from plaza.sim.data_models import GameData
from plaza.sim.decisions import Decisions
from plaza.sim.errors import InvalidSaveNameError, SaveExistsError, SaveNotFoundError
from plaza.sim.setup import new_game
from plaza.sim.state import PLAYER_ORG_ID
from plaza.sim.streams import rng_factory
from plaza.sim.turn import advance_turn

SAVE_SUFFIX: Final = ".plaza.sqlite"
MIGRATIONS_DIR: Final = BACKEND_DIR / "migrations"
MIGRATOR: Final = Migrator(
    MIGRATIONS_DIR,
    suffix=SAVE_SUFFIX,
    turn_sql="SELECT current_turn FROM save_meta",
    sync_env=SQLITE_SYNC_ENV,
)
LOCKS: Final = SaveLocks()
_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")


@dataclass(frozen=True, slots=True)
class SaveSummary:
    slug: str
    name: str
    org_name: str
    leader_name: str
    turn: int
    date_label: str
    status: str


@dataclass(frozen=True, slots=True)
class LineOut:
    turn: int
    book: str
    memo: str
    account: str
    amount_cents: int


def save_path(save_dir: Path, slug: str) -> Path:
    if not _SLUG_RE.match(slug):
        raise InvalidSaveNameError(
            f"save names use lower-case letters, digits and hyphens, got {slug!r}"
        )
    return save_dir / f"{slug}{SAVE_SUFFIX}"


def _sessions(path: Path) -> sessionmaker[Session]:
    return make_sessionmaker(shared_engine(path, SQLITE_SYNC_ENV))


def create_save(
    save_dir: Path,
    slug: str,
    *,
    org_name: str,
    leader_name: str,
    background: str,
    data: GameData,
    scenario_id: str | None = None,
    difficulty: str | None = None,
    ironman: bool = False,
    seed: int | None = None,
) -> CoreState:
    path = save_path(save_dir, slug)
    if path.exists():
        raise SaveExistsError(f"a save named {slug!r} already exists")
    master_seed = secrets.randbelow(MAX_SEED + 1) if seed is None else seed
    game = new_game(
        name=slug,
        master_seed=master_seed,
        org_name=org_name,
        leader_name=leader_name,
        background=background,
        scenario_id=scenario_id or data.scenarios.default_scenario,
        difficulty=difficulty or data.scenarios.default_difficulty,
        ironman=ironman,
        data=data,
    )
    save_dir.mkdir(parents=True, exist_ok=True)
    MIGRATOR.upgrade_new(path)

    def persist(session: Session) -> None:
        insert_new(session, game.state, game.ledger_entries)

    run_in_transaction(_sessions(path), persist)
    return game.state


def open_save(save_dir: Path, slug: str) -> Path:
    path = save_path(save_dir, slug)
    if not path.is_file():
        raise SaveNotFoundError(f"no save named {slug!r}")
    backup.wait(path)
    MIGRATOR.ensure_current(path)
    return path


def read_state(path: Path) -> tuple[CoreState, Balances]:
    with _sessions(path)() as session:
        return load_state(session), ledger_balances(session)


def run_turn(path: Path, data: GameData, decisions: Decisions | None = None) -> TurnResult:
    """Play one month: load, advance, write everything in one transaction (TST ADR-0004
    section 4). If anything raises, nothing of the month is written."""

    def persist(session: Session) -> TurnResult:
        state = load_state(session)
        result = advance_turn(
            state,
            decisions or Decisions(),
            rng_factory(state.meta.master_seed),
            data,
            ledger_balances(session),
        )
        write_turn(
            session, result.new_state, result.ledger_entries, result.log_items, result.snapshot
        )
        return result

    with LOCKS.exclusive(path):
        result = run_in_transaction(_sessions(path), persist)
    backups = data.balance.backups
    if result.new_state.turn % backups.every_turns == 0:
        backup.periodic_backup_in_background(
            path, result.new_state.turn, backups.keep_periodic, suffix=SAVE_SUFFIX
        )
    return result


def list_saves(save_dir: Path) -> list[SaveSummary]:
    out: list[SaveSummary] = []
    if not save_dir.is_dir():
        return out
    for path in sorted(save_dir.glob(f"*{SAVE_SUFFIX}")):
        with _sessions(path)() as session:
            meta = session.get(SaveMetaRow, META_ID)
            org = session.get(OrganisationRow, PLAYER_ORG_ID)
            if meta is None or org is None:
                continue
            start = (meta.start_year, meta.start_month)
            out.append(
                SaveSummary(
                    slug=backup.slug_of(path, SAVE_SUFFIX),
                    name=meta.name,
                    org_name=org.name,
                    leader_name=org.leader_name,
                    turn=meta.current_turn,
                    date_label=format_turn(meta.current_turn, start),
                    status=meta.status,
                )
            )
    return out


def snapshots(path: Path, entity_id: int = PLAYER_ORG_ID) -> list[tuple[int, dict[str, object]]]:
    with _sessions(path)() as session:
        rows = session.scalars(
            select(TurnSnapshotRow)
            .where(TurnSnapshotRow.entity_id == entity_id)
            .order_by(TurnSnapshotRow.turn)
        )
        return [(r.turn, json.loads(r.kpis_json)) for r in rows]


def account_lines(path: Path, account: str, entity_id: int = PLAYER_ORG_ID) -> list[LineOut]:
    """Every posted line on one account, oldest first (the Explain breakdown of a balance)."""
    with _sessions(path)() as session:
        rows = session.execute(
            select(LedgerEntryRow, LedgerLineRow)
            .join(LedgerLineRow, LedgerLineRow.entry_id == LedgerEntryRow.id)
            .where(LedgerEntryRow.entity_id == entity_id, LedgerLineRow.account == account)
            .order_by(LedgerEntryRow.turn, LedgerEntryRow.id, LedgerLineRow.id)
        )
        return [LineOut(e.turn, e.book, e.memo, ln.account, ln.amount_cents) for e, ln in rows]
