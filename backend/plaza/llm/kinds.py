"""Plaza's text kinds and the adapter in use (spec 16; ADR PL-0008).

The four kinds are declared with their system prompts (`prompts.yaml`, linted by the
content-rules guard). The default adapter is the offline template adapter: Plaza is fully
playable without a key, and Claude is used only when the player chooses it in Settings and a
key is present.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Final

import yaml
from pydantic import BaseModel, ConfigDict
from simcore_llm.base import LLMAdapter
from simcore_llm.settings import SETTINGS_FILE, LLMSettings, active_adapter, load_settings

from plaza.config import get_settings

FIELD_REPORT: Final = "field_report"
COUNCIL_MINUTES: Final = "council_minutes"
INFORMANT_TIP: Final = "informant_tip"
YEAR_END_REPORT: Final = "year_end_report"
TEXT_KINDS: Final = (COUNCIL_MINUTES, FIELD_REPORT, INFORMANT_TIP, YEAR_END_REPORT)
# The longer, rarer texts use the story model (simcore_llm's Claude adapter routes by kind).
STORY_TEXT_KINDS: Final = frozenset({COUNCIL_MINUTES, YEAR_END_REPORT})
PROMPTS_FILE: Final = Path(__file__).resolve().parent / "prompts.yaml"


class TextKind(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: str
    title: str
    system: str


@lru_cache(maxsize=1)
def text_kinds() -> dict[str, TextKind]:
    raw = yaml.safe_load(PROMPTS_FILE.read_text(encoding="utf-8"))
    kinds = {k["kind"]: TextKind.model_validate(k) for k in raw["kinds"]}
    if tuple(sorted(kinds)) != TEXT_KINDS:
        raise ValueError(f"prompts.yaml must declare exactly {TEXT_KINDS}, got {sorted(kinds)}")
    return kinds


def llm_settings(save_dir: Path) -> LLMSettings:
    """The player's LLM settings; before any are saved, the template adapter."""
    if not (save_dir / SETTINGS_FILE).is_file():
        return LLMSettings(adapter="templates")
    return load_settings(save_dir)


def adapter() -> LLMAdapter:
    settings = get_settings()
    return active_adapter(
        llm_settings(settings.resolved_save_dir()),
        settings.anthropic_api_key,
        settings.llm_adapter,
        story_text_kinds=STORY_TEXT_KINDS,
    )
