"""ADR PL-0001 and SC-0011: Plaza depends on sim-core by tag only. A branch, a commit or a
bare requirement fails here, in pyproject.toml and in the lock."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parents[2]
TAG_PIN = re.compile(
    r"^simcore(\[[a-z,]+\])? @ git\+https://github\.com/Reece77/(sim-core|Sim-core)@v\d+\.\d+\.\d+$"
)


def is_tag_pin(requirement: str) -> bool:
    return bool(TAG_PIN.match(requirement.strip()))


def simcore_requirements() -> list[str]:
    project = tomllib.loads((BACKEND / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    return [r for r in project["dependencies"] if re.match(r"^simcore\b", r)]


def test_pyproject_pins_simcore_by_tag() -> None:
    reqs = simcore_requirements()
    assert len(reqs) == 1, reqs
    assert is_tag_pin(reqs[0]), f"sim-core must be pinned to a tag: {reqs[0]}"


def test_lock_resolves_the_same_tag_to_a_commit() -> None:
    lock = tomllib.loads((BACKEND / "uv.lock").read_text(encoding="utf-8"))
    (pkg,) = [p for p in lock["package"] if p["name"] == "simcore"]
    tag = simcore_requirements()[0].rsplit("@", 1)[1]
    source = pkg["source"]["git"]
    assert f"?rev={tag}#" in source or f"?tag={tag}#" in source, source
    assert re.search(r"#[0-9a-f]{40}$", source), "the lock must record the tag's commit"


@pytest.mark.parametrize(
    "requirement",
    [
        "simcore",
        "simcore>=0.1",
        "simcore[db,llm] @ git+https://github.com/Reece77/sim-core",
        "simcore[db,llm] @ git+https://github.com/Reece77/sim-core@main",
        "simcore[db,llm] @ git+https://github.com/Reece77/sim-core@b2fc2db",
        "simcore[db,llm] @ git+https://github.com/Reece77/sim-core@v0.1",
        "simcore[db,llm] @ file:///home/user/Sim-core",
    ],
)
def test_non_tag_pins_are_refused(requirement: str) -> None:
    assert not is_tag_pin(requirement)


def test_the_tag_pin_is_accepted() -> None:
    assert is_tag_pin("simcore[db,llm] @ git+https://github.com/Reece77/sim-core@v0.1.0")
