"""TST ADR-0002, PL-0001 section 5: plaza.sim is pure (simcore_testing's purity scanner)."""

from __future__ import annotations

from pathlib import Path

from simcore_testing.purity import find_violations, scan_package

SIM = Path(__file__).resolve().parents[2] / "plaza" / "sim"
BANNED = (
    "plaza.db",
    "plaza.api",
    "plaza.llm",
    "plaza.loader",
    "plaza.config",
    "simcore_db",
    "simcore_llm",
    "simcore_testing",
)


def test_plaza_sim_is_pure() -> None:
    assert scan_package(SIM, BANNED) == []


def test_the_scanner_catches_each_kind_of_impurity(tmp_path: Path) -> None:
    pkg = tmp_path / "sim"
    pkg.mkdir()
    bad = pkg / "bad.py"
    bad.write_text(
        "import random\nimport time\nfrom pathlib import Path\nfrom plaza.db import saves\n"
        "import numpy as np\nfrom datetime import datetime\n"
        "x = np.random.rand()\ny = datetime.now()\nz = open('f')\n"
    )
    problems = find_violations(bad, pkg, BANNED)
    joined = "\n".join(problems)
    for needle in ("random", "time", "pathlib", "plaza.db", "np.random", "clock", "open"):
        assert needle in joined, needle
