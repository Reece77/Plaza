"""Saves (TST ADR-0004): a full campaign with a cold reload every month, one transaction per
turn (an exception or a killed process mid-turn leaves the previous month), backups, and the
mapper contract (SC-0003)."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import pytest
from simcore.kernel.calendar import format_turn
from simcore.state import encode_state
from simcore_db import backup

from plaza.db import saves, state_io
from plaza.sim.books import DIRTY_CASH, totals_by_type
from plaza.sim.data_models import GameData
from plaza.sim.errors import GameOverError, SaveExistsError
from plaza.sim.setup import new_game
from plaza.sim.state import SaveInfo
from tests.support import BACKGROUNDS, make_save

BACKEND = Path(__file__).resolve().parents[2]


def test_full_campaign_ends_in_december_2035_and_reloads_cold(
    save_dir: Path, data: GameData
) -> None:
    path = make_save(save_dir, data)
    stake = data.balance.start.dirty_stake_cents
    for turn in range(360):
        state, balances = saves.read_state(saves.open_save(save_dir, "t"))  # cold, every month
        assert state.turn == turn and state.meta.status == "active"
        for book in ("dirty", "clean"):
            t = totals_by_type(balances, 1, data.accounts, book)
            assert sum(t.values()) == 0  # each book balances every month
        result = saves.run_turn(path, data)
        assert result.snapshot is not None and result.snapshot.turn == turn
    assert format_turn(result.snapshot.turn, state.meta.start_ym) == "Dec 2035"
    state, balances = saves.read_state(path)
    assert state.meta.status == "campaign_complete"
    assert state.sub(SaveInfo).ended_turn == 359
    assert balances[(1, DIRTY_CASH, "USD")] == stake
    with pytest.raises(GameOverError):
        saves.run_turn(path, data)
    backup.wait(path)
    backups = backup.periodic_backups(path, suffix=saves.SAVE_SUFFIX)
    assert len(backups) == data.balance.backups.keep_periodic
    assert backups[-1].name == "t.turn-360.sqlite"


def test_a_raise_mid_turn_leaves_the_save_unchanged(
    save_dir: Path, data: GameData, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = make_save(save_dir, data)
    saves.run_turn(path, data)
    before = saves.read_state(path)
    real = state_io.write_turn

    def crash(session, *args, **kwargs):  # type: ignore[no-untyped-def]
        real(session, *args, **kwargs)  # every row written, then the turn fails
        raise RuntimeError("power cut")

    monkeypatch.setattr(saves, "write_turn", crash)
    with pytest.raises(RuntimeError):
        saves.run_turn(path, data)
    assert saves.read_state(path) == before
    monkeypatch.undo()
    saves.run_turn(path, data)
    assert saves.read_state(path)[0].turn == 2


KILLED_CHILD = textwrap.dedent(
    """
    import sys, time
    from pathlib import Path
    from plaza.db import saves, state_io
    from plaza.loader import game_data

    marker = Path(sys.argv[2])
    real = state_io.write_turn

    def write_then_hang(session, *args, **kwargs):
        real(session, *args, **kwargs)
        session.flush()  # the month's rows are in the open transaction
        marker.write_text("written")
        time.sleep(60)  # killed here, before the commit

    saves.write_turn = write_then_hang
    saves.run_turn(Path(sys.argv[1]), game_data())
    """
)


def test_killing_the_process_mid_turn_leaves_the_previous_turn(
    save_dir: Path, data: GameData, tmp_path: Path
) -> None:
    path = make_save(save_dir, data)
    for _ in range(3):
        saves.run_turn(path, data)
    before = saves.read_state(path)
    marker = tmp_path / "written"
    env = {**os.environ, "PLAZA_SQLITE_SYNC": "NORMAL"}
    child = subprocess.Popen(
        [sys.executable, "-c", KILLED_CHILD, str(path), str(marker)], cwd=BACKEND, env=env
    )
    try:
        deadline = time.monotonic() + 60
        while not marker.exists():  # wait on state: the child has written the month's rows
            assert child.poll() is None, "the child exited before writing"
            assert time.monotonic() < deadline, "the child never wrote"
            time.sleep(0.05)
        child.send_signal(signal.SIGKILL)
    finally:
        child.wait(timeout=30)
    assert child.returncode == -signal.SIGKILL
    reopened = saves.open_save(save_dir, "t")
    assert saves.read_state(reopened) == before
    assert before[0].turn == 3
    saves.run_turn(reopened, data)
    assert saves.read_state(reopened)[0].turn == 4


def test_the_mapper_round_trips_the_state(save_dir: Path, data: GameData) -> None:
    game = new_game(
        name="m",
        master_seed=2**64 - 1,
        org_name="The Organisation",
        leader_name="The Leader",
        background="accountant",
        scenario_id="standard",
        difficulty="kingpin",
        ironman=True,
        data=data,
    )
    path = make_save(
        save_dir,
        data,
        slug="m",
        seed=2**64 - 1,
        background="accountant",
        difficulty="kingpin",
        ironman=True,
    )
    assert encode_state(saves.read_state(path)[0]) == encode_state(game.state)


@pytest.mark.parametrize("background", BACKGROUNDS)
def test_each_background_starts(save_dir: Path, data: GameData, background: str) -> None:
    path = make_save(save_dir, data, slug=background, background=background)
    saves.run_turn(path, data)
    summary = {s.slug: s for s in saves.list_saves(save_dir)}[background]
    assert summary.date_label == "Feb 2006" and summary.status == "active"


def test_duplicate_save_name_refused(save_dir: Path, data: GameData) -> None:
    make_save(save_dir, data)
    with pytest.raises(SaveExistsError):
        make_save(save_dir, data)


def test_seed_round_trips_at_the_extremes(save_dir: Path, data: GameData) -> None:
    for i, seed in enumerate((0, 2**63, 2**64 - 1)):
        path = make_save(save_dir, data, slug=f"s{i}", seed=seed)
        assert saves.read_state(path)[0].meta.master_seed == seed


def test_save_files_use_plazas_suffix(save_dir: Path, data: GameData) -> None:
    path = make_save(save_dir, data)
    assert path.name == "t.plaza.sqlite"
