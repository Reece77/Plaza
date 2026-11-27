"""TST ADR-0003: no money arithmetic in binary floats in plaza.sim (simcore_testing)."""

from __future__ import annotations

from pathlib import Path

from simcore_testing.money_guard import scan

SIM = Path(__file__).resolve().parents[2] / "plaza" / "sim"


def test_no_float_money_in_the_sim() -> None:
    assert scan(SIM) == []


def test_the_guard_catches_float_money(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text(
        "def f(price_cents: int) -> int:\n    return price_cents * 0.5\n"
    )
    assert len(scan(tmp_path)) == 1
