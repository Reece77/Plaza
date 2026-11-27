"""The LLM seam (TST ADR-0005; spec 16): Plaza's four text kinds are declared, the template
adapter is the default, tests use the mock, and no text is generated at PL-M0."""

from __future__ import annotations

from pathlib import Path

import pytest
from simcore_llm.base import TextPrompt
from simcore_llm.settings import LLMSettings, save_settings

from plaza.config import get_settings
from plaza.llm import kinds


def test_the_four_text_kinds_are_declared() -> None:
    declared = kinds.text_kinds()
    assert (
        tuple(sorted(declared))
        == kinds.TEXT_KINDS
        == (
            "council_minutes",
            "field_report",
            "informant_tip",
            "year_end_report",
        )
    )
    assert set(declared) >= kinds.STORY_TEXT_KINDS
    for kind in declared.values():
        assert "real person" in kind.system and "operational" in kind.system


def test_template_adapter_is_the_default(save_dir: Path) -> None:
    assert kinds.llm_settings(save_dir).adapter == "templates"
    save_settings(save_dir, LLMSettings(adapter="claude"))
    assert kinds.llm_settings(save_dir).adapter == "claude"


def test_tests_get_the_mock_and_templates_need_no_key(
    save_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert kinds.adapter().name == "mock"
    monkeypatch.delenv("PLAZA_LLM_ADAPTER")
    get_settings.cache_clear()
    adapter = kinds.adapter()
    assert adapter.name == "template"
    done = adapter.generate_text(TextPrompt("field_report", "s", "u", "A quiet month."))
    assert done.content == "A quiet month."
