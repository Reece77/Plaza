"""Reads Plaza's YAML data and validates it through sim-core's DataRegistry (TST ADR-0008).
Outside the sim: invalid data fails at start-up."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from simcore.kernel.errors import InvalidDataError

from plaza.config import get_settings
from plaza.sim.data_models import SECTIONS, GameData, registry


def _read(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        loaded = yaml.safe_load(fh)
    if not isinstance(loaded, dict):
        raise InvalidDataError(f"{path.name} must hold a mapping")
    return loaded


def load_game_data(data_dir: Path) -> GameData:
    """One section per file: `<section>.yaml` in `data_dir`."""
    raw = {name: _read(data_dir / f"{name}.yaml") for name, _model in SECTIONS}
    return GameData(registry().load(raw))


@lru_cache(maxsize=1)
def game_data() -> GameData:
    return load_game_data(get_settings().data_dir)
