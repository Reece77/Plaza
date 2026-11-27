"""The content-rules linter (ADR PL-0008 section 6).

What it reads (`targets`): every YAML file under backend/plaza/data/ and backend/plaza/llm/
(seed data and prompt templates), every Markdown file under docs/ and at the repository
root, and the comments and docstrings of every Python, TypeScript and JavaScript source file
(backend/, tools/, frontend/src, frontend/e2e, frontend/scripts). Its own term list and the
guard's fixtures are excluded: the fixtures are linted by their own tests.
"""

from __future__ import annotations

import io
import re
import sys
import tokenize
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TERMS = HERE / "terms.yaml"
ALLOW = "content-rules-allow:"
FIXTURES = REPO / "backend" / "tests" / "fixtures" / "content_rules"
SKIP_DIRS = frozenset({"node_modules", ".venv", "dist", "__pycache__", ".git", "api"})
CODE_SUFFIXES = (".ts", ".tsx", ".js", ".mjs")


@dataclass(frozen=True, slots=True)
class Rule:
    id: str
    clause: str
    pattern: re.Pattern[str]
    reason: str


@dataclass(frozen=True, slots=True)
class Finding:
    path: str
    line: int
    rule: str
    text: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: [{self.rule}] {self.text}"


def load_rules(path: Path = TERMS) -> tuple[Rule, ...]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    rules = tuple(
        Rule(r["id"], str(r["clause"]), re.compile(r["pattern"], re.IGNORECASE), r["reason"])
        for r in raw["rules"]
    )
    ids = [r.id for r in rules]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate rule ids in terms.yaml")
    return rules


def lint_lines(
    lines: Iterable[tuple[int, str]], where: str, rules: tuple[Rule, ...]
) -> list[Finding]:
    """Every rule match in `(line number, text)` pairs, unless the line carries an allow
    marker naming that rule."""
    found: list[Finding] = []
    for number, text in lines:
        allowed = text.split(ALLOW, 1)[1].split()[:1] if ALLOW in text else []
        for rule in rules:
            if rule.id in allowed:
                continue
            match = rule.pattern.search(text)
            if match:
                found.append(Finding(where, number, rule.id, match.group(0)))
    return found


def lint_text(text: str, where: str, rules: tuple[Rule, ...]) -> list[Finding]:
    return lint_lines(enumerate(text.splitlines(), start=1), where, rules)


def python_comments(source: str) -> Iterator[tuple[int, str]]:
    """Comments and docstrings (every string statement) of a Python module, by line."""
    tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    previous = tokenize.NEWLINE
    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            yield tok.start[0], tok.string
        elif tok.type == tokenize.STRING and previous in (
            tokenize.NEWLINE,
            tokenize.NL,
            tokenize.INDENT,
            tokenize.DEDENT,
        ):
            for offset, line in enumerate(tok.string.splitlines()):
                yield tok.start[0] + offset, line
        if tok.type not in (tokenize.COMMENT, tokenize.NL):
            previous = tok.type


_JS_COMMENT = re.compile(r"//[^\n]*|/\*.*?\*/", re.DOTALL)


def js_comments(source: str) -> Iterator[tuple[int, str]]:
    """`//` and `/* */` comments of a TypeScript or JavaScript file, by line (a URL's `//`
    inside a string is read as a comment too: harmless, it only widens the scan)."""
    for match in _JS_COMMENT.finditer(source):
        first = source.count("\n", 0, match.start()) + 1
        for offset, line in enumerate(match.group(0).splitlines()):
            yield first + offset, line


def _walk(root: Path, suffixes: tuple[str, ...]) -> Iterator[Path]:
    if not root.exists():
        return
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.relative_to(REPO).parts):
            continue
        wanted = path.is_file() and path.suffix in suffixes and path != TERMS
        if wanted and FIXTURES not in path.parents:
            yield path


def targets(repo: Path = REPO) -> Iterator[tuple[Path, str]]:
    """(path, kind) for every file the guard lints: kind is "text", "python" or "js"."""
    for folder in (repo / "backend" / "plaza" / "data", repo / "backend" / "plaza" / "llm"):
        for path in _walk(folder, (".yaml", ".yml")):
            yield path, "text"
    for path in _walk(repo / "docs", (".md",)):
        yield path, "text"
    for path in sorted(repo.glob("*.md")):
        yield path, "text"
    for folder in (repo / "backend", repo / "tools"):
        for path in _walk(folder, (".py",)):
            yield path, "python"
    for name in ("src", "e2e", "scripts"):
        for path in _walk(repo / "frontend" / name, CODE_SUFFIXES):
            yield path, "js"


def lint_file(path: Path, kind: str, rules: tuple[Rule, ...], repo: Path = REPO) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    where = path.relative_to(repo).as_posix()
    if kind == "python":
        return lint_lines(python_comments(text), where, rules)
    if kind == "js":
        return lint_lines(js_comments(text), where, rules)
    return lint_text(text, where, rules)


def lint_repo(repo: Path = REPO) -> list[Finding]:
    rules = load_rules()
    return [f for path, kind in targets(repo) for f in lint_file(path, kind, rules, repo)]


def main() -> int:
    found = lint_repo()
    for finding in found:
        print(finding)
    print(f"{len(found)} finding(s)")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
