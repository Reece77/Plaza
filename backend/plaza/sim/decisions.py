"""The player's orders for a month (TST ADR-0012's `decisions` input). Empty at PL-M0: each
milestone that gives the player a choice adds its field."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Decisions:
    pass
