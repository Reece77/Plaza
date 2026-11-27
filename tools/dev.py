"""`make dev`: the API on :8000 and Vite on :5173 together; Ctrl+C stops both (from PT-M0)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SHELL = sys.platform == "win32"


def main() -> int:
    api = subprocess.Popen(
        ["uv", "run", "uvicorn", "plaza.api.app:app", "--reload", "--port", "8000"],
        cwd=REPO / "backend",
        shell=SHELL,
    )
    web = subprocess.Popen(["pnpm", "dev"], cwd=REPO / "frontend", shell=SHELL)
    try:
        return web.wait()
    except KeyboardInterrupt:
        return 0
    finally:
        for proc in (api, web):
            proc.terminate()


if __name__ == "__main__":
    sys.exit(main())
