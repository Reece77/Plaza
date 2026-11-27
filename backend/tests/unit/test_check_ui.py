"""The UI shell under frontend/src/core is sim-core v0.1.0's ui/, unchanged (SC-0010)."""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"
spec = importlib.util.spec_from_file_location("plaza_check_ui", TOOLS / "check_ui.py")
assert spec is not None and spec.loader is not None
check_ui = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_ui)


def test_the_copy_matches_the_pinned_manifest() -> None:
    assert check_ui.problems() == []


def test_an_edited_file_or_manifest_is_caught(tmp_path: Path) -> None:
    copy = tmp_path / "core"
    shutil.copytree(check_ui.CORE, copy)
    (copy / "lib" / "format.ts").write_text("// edited\n", encoding="utf-8")
    assert check_ui.problems(copy) == ["ui drift: lib/format.ts"]
    (copy / "MANIFEST.json").write_text("{}\n", encoding="utf-8")
    assert any("MANIFEST.json" in p for p in check_ui.problems(copy))
