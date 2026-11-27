"""Plaza's own Alembic chain (SC-0009): one linear chain from schema v1, its head matches
the models exactly, and it upgrades and downgrades cleanly."""

from __future__ import annotations

from pathlib import Path

from alembic.autogenerate import compare_metadata
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from simcore_db.migrate import Migrator
from simcore_db.session import make_engine

from plaza.config import SQLITE_SYNC_ENV
from plaza.db.models import Base
from plaza.db.saves import MIGRATIONS_DIR, MIGRATOR, SAVE_SUFFIX


def _script() -> ScriptDirectory:
    return ScriptDirectory.from_config(MIGRATOR._config())


def test_the_chain_is_linear_from_0001() -> None:
    script = _script()
    assert script.get_heads() == [MIGRATOR.head_revision()]
    revisions = list(script.walk_revisions())  # head first
    assert revisions[-1].revision == "0001_initial" and revisions[-1].down_revision is None
    for rev in revisions:
        assert not isinstance(rev.down_revision, tuple), "no merge revisions"
    files = sorted(p.name for p in (MIGRATIONS_DIR / "versions").glob("*.py"))
    assert len(files) == len(revisions)
    assert [r.revision for r in reversed(revisions)] == [f.removesuffix(".py") for f in files]


def test_head_matches_the_models(tmp_path: Path) -> None:
    path = tmp_path / f"m{SAVE_SUFFIX}"
    migrator = Migrator(MIGRATIONS_DIR, suffix=SAVE_SUFFIX, sync_env=SQLITE_SYNC_ENV)
    migrator.upgrade_new(path)
    engine = make_engine(path, SQLITE_SYNC_ENV)
    try:
        with engine.connect() as conn:
            diff = compare_metadata(MigrationContext.configure(conn), Base.metadata)
    finally:
        engine.dispose()
    assert diff == []


def test_downgrade_to_base_and_up_again(tmp_path: Path) -> None:
    path = tmp_path / f"d{SAVE_SUFFIX}"
    migrator = Migrator(MIGRATIONS_DIR, suffix=SAVE_SUFFIX, sync_env=SQLITE_SYNC_ENV)
    migrator.upgrade_new(path)
    migrator.downgrade(path, "base")
    assert migrator.current_revision(path) is None
    migrator.ensure_current(path)
    assert migrator.current_revision(path) == migrator.head_revision()
