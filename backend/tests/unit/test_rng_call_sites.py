"""TST ADR-0013: one stream name per call site, every name registered (simcore_testing)."""

from __future__ import annotations

from pathlib import Path

from simcore_testing.call_sites import check_call_sites

from plaza.sim.streams import TABLE

PLAZA = Path(__file__).resolve().parents[2] / "plaza"


def test_every_stream_call_site_is_unique_and_registered() -> None:
    files = sorted(PLAZA.rglob("*.py"))
    assert check_call_sites(files, PLAZA, TABLE, allow_passed_in=False) == []


def test_the_check_catches_a_repeated_or_unknown_name(tmp_path: Path) -> None:
    bad = tmp_path / "bad.py"
    bad.write_text(
        "def a(rng):\n    return rng.stream(0, 'plaza', 1)\n"
        "def b(rng):\n    return rng.stream(0, 'plaza', 2)\n"
        "def c(rng):\n    return rng.stream(0, 'nope')\n"
    )
    problems = check_call_sites([bad], tmp_path, TABLE, allow_passed_in=False)
    assert len(problems) == 2
