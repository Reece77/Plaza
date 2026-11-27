"""The calendar (ADR PL-0002; PT-0002): turn 0 is the scenario's start, January 2006, and
every call into sim-core's calendar passes the save's start (a call without it would mean
January 2010, TST's turn 0)."""

from __future__ import annotations

import ast
from pathlib import Path

from simcore.kernel.calendar import format_turn, turn_to_ym, ym_to_turn

from plaza.sim.data_models import GameData

REPO = Path(__file__).resolve().parents[3]
CALENDAR_FUNCS = {"turn_to_ym": 1, "format_turn": 1, "ym_to_turn": 2, "start_turn_of": 2}
SCANNED = (REPO / "backend" / "plaza", REPO / "backend" / "tests", REPO / "tools")


def test_standard_campaign_runs_january_2006_to_december_2035(data: GameData) -> None:
    scenario = data.scenarios.scenario(data.scenarios.default_scenario)
    assert scenario is not None
    start = scenario.start_ym
    assert start == (2006, 1) and scenario.campaign_turns == 360
    assert turn_to_ym(0, start) == (2006, 1)
    assert format_turn(scenario.campaign_turns - 1, start) == "Dec 2035"
    assert ym_to_turn(2035, 12, start) == 359


def missing_start(path: Path, root: Path = REPO) -> list[str]:
    """Calls to a calendar function without `start` (as a keyword or the last positional)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", None)
        if name not in CALENDAR_FUNCS:
            continue
        has_start = any(k.arg == "start" for k in node.keywords) or (
            len(node.args) > CALENDAR_FUNCS[name]
        )
        if not has_start:
            found.append(f"{path.relative_to(root)}:{node.lineno}: {name} without start")
    return found


def test_every_calendar_call_passes_the_start() -> None:
    problems = [p for root in SCANNED for f in sorted(root.rglob("*.py")) for p in missing_start(f)]
    assert problems == []


def test_the_check_catches_a_call_without_start(tmp_path: Path) -> None:
    bad = tmp_path / "bad.py"
    bad.write_text("from simcore.kernel.calendar import format_turn\nformat_turn(3)\n")
    assert len(missing_start(bad, tmp_path)) == 1
