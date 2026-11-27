"""Check frontend/src/core against sim-core's UI shell at the pinned tag (SC-0010).

frontend/src/core is a copy of sim-core's `ui/` at `v0.1.0` with its MANIFEST.json. This
check needs no sim-core checkout: the manifest's own sha256 is pinned here (taken from the
tag), and every file's sha256 must match the manifest, the same digests sim-core's
`tools/ui_manifest.py --check` computes. Upgrading sim-core re-copies `ui/` and updates both.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

CORE = Path(__file__).resolve().parents[1] / "frontend" / "src" / "core"
SIMCORE_TAG = "v0.1.0"
MANIFEST_SHA256 = "1ecdf03bf74d22308fb825d45106c4fe11d08ee057b5a15f0b910606a207a835"
SKIP = ("MANIFEST.json", "README.md")


def digests(root: Path) -> dict[str, str]:
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file() and p.name not in SKIP
    }


def problems(root: Path = CORE) -> list[str]:
    manifest = root / "MANIFEST.json"
    if not manifest.is_file():
        return ["frontend/src/core/MANIFEST.json is missing"]
    out = []
    if hashlib.sha256(manifest.read_bytes()).hexdigest() != MANIFEST_SHA256:
        out.append(f"MANIFEST.json is not sim-core {SIMCORE_TAG}'s")
    recorded = json.loads(manifest.read_text(encoding="utf-8"))
    found = digests(root)
    out += [
        f"ui drift: {name}"
        for name in sorted(set(recorded) | set(found))
        if recorded.get(name) != found.get(name)
    ]
    return out


def main() -> int:
    found = problems()
    for line in found:
        print(line)
    print("UI shell matches sim-core " + SIMCORE_TAG if not found else f"{len(found)} problem(s)")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
