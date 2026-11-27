"""Alembic environment for Plaza's own chain (TST ADR-0004; SC-0009). Migrations always
target a single save file; `simcore_db.migrate.Migrator` passes the connection in."""

from __future__ import annotations

from pathlib import Path

from alembic import context
from simcore_db.session import make_engine

from plaza.config import SQLITE_SYNC_ENV
from plaza.db.models import Base

config = context.config
target_metadata = Base.metadata


def _run(connection: object) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,  # SQLite cannot ALTER most things in place
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connection = config.attributes.get("connection")
    if connection is not None:
        _run(connection)
        return
    save = context.get_x_argument(as_dictionary=True).get("save")
    if not save:
        raise SystemExit("pass the save file: alembic -x save=PATH upgrade head")
    engine = make_engine(Path(save), SQLITE_SYNC_ENV)
    with engine.connect() as conn:
        _run(conn)
    engine.dispose()


if context.is_offline_mode():
    raise SystemExit("offline migrations are not supported")
run_migrations_online()
