"""The content-rules guard (ADR PL-0008 section 6; PL-M0 sub-task 2).

It lints backend/plaza/data/, docs/, the LLM prompt templates and every code comment and
docstring against tools/content_rules/terms.yaml. The guard's own fixtures prove it bites:
the forbidden fixture trips every rule, the news-level fixture trips none.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))

from content_rules.lint import (  # noqa: E402
    FIXTURES,
    js_comments,
    lint_file,
    lint_lines,
    lint_repo,
    lint_text,
    load_rules,
    python_comments,
    targets,
)

RULES = load_rules()


def test_the_repository_passes() -> None:
    found = lint_repo()
    assert found == [], "\n".join(str(f) for f in found)


def test_the_design_pack_as_copied_is_linted_and_passes() -> None:
    linted = {p.relative_to(REPO).as_posix() for p, _ in targets()}
    for doc in (
        "docs/roadmap.md",
        "docs/reuse-map.md",
        "docs/game-design-spec.md",
        "docs/questions.md",
        "docs/research/dossier-v1.md",
        "docs/adr/PL-0008-content-rules.md",
        "docs/tasks/PL-M0-foundation.md",
    ):
        assert doc in linted
        assert lint_file(REPO / doc, "text", RULES) == []


def test_data_prompts_and_code_are_in_scope() -> None:
    kinds = {(p.relative_to(REPO).as_posix(), k) for p, k in targets()}
    assert ("backend/plaza/data/accounts.yaml", "text") in kinds
    assert ("backend/plaza/llm/prompts.yaml", "text") in kinds
    assert ("backend/plaza/sim/turn.py", "python") in kinds
    assert not any(FIXTURES.as_posix() in (REPO / p).as_posix() for p, _ in kinds)


@pytest.mark.parametrize("rule", [r.id for r in RULES])
def test_the_forbidden_fixture_trips_every_rule(rule: str) -> None:
    found = lint_file(FIXTURES / "forbidden.md", "text", RULES)
    assert rule in {f.rule for f in found}, f"no line of the fixture trips {rule}"


def test_every_forbidden_line_is_flagged() -> None:
    lines = (FIXTURES / "forbidden.md").read_text(encoding="utf-8").splitlines()
    flagged = {f.line for f in lint_file(FIXTURES / "forbidden.md", "text", RULES)}
    for number, line in enumerate(lines, start=1):
        if line.startswith("- "):
            assert number in flagged, line


def test_the_news_level_fixture_passes() -> None:
    assert lint_file(FIXTURES / "news_level.md", "text", RULES) == []


def test_comments_and_docstrings_are_read_but_code_is_not() -> None:
    source = (
        '"""Module docstring: the film was gory."""\n'
        "GORY = 1  # a comment: the film was gory\n"
        "def f() -> str:\n"
        '    """Docstring: gory."""\n'
        '    return "gory"\n'
    )
    lines = [n for n, _ in python_comments(source)]
    assert lines == [1, 2, 4]
    assert len(lint_lines(python_comments(source), "x.py", RULES)) == 3
    js = "const a = 'gory'; // gory\n/* also\n gory */\n"
    assert [n for n, _ in js_comments(js)] == [1, 2, 3]


def test_an_allow_marker_names_one_rule() -> None:
    text = "the film was gory  content-rules-allow: graphic-violence quoting a review"
    assert lint_text(text, "x", RULES) == []
    assert lint_text("the film was gory  content-rules-allow: torture", "x", RULES) != []
