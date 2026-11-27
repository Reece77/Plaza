"""ADR PL-0002 section 5: the twelve phases, one per sim-core slot, in Plaza's order. The
printed order is the guard; registration order cannot change it (SC-0005)."""

from __future__ import annotations

import itertools
import random

from simcore.turn import SLOTS, PhaseRegistry

from plaza.sim.turn import PHASES, REGISTRY

EXPECTED = (
    "decisions.world_and_policy_shocks",
    "actors.agency",
    "progress.rivals",
    "operations.production",
    "revenue.logistics",
    "costs.markets_and_sales",
    "financing.laundering",
    "people.heat",
    "world.people",
    "checks.council",
    "report.events",
    "requests.snapshot",
)


def test_the_order_is_pl_0002s() -> None:
    assert REGISTRY.describe() == EXPECTED
    assert tuple(slot for slot, _, _ in PHASES) == SLOTS


def test_registration_order_does_not_matter() -> None:
    orders = list(itertools.islice(itertools.permutations(PHASES), 50))
    shuffled = list(PHASES)
    random.Random(7).shuffle(shuffled)  # a test-only ordering, not a sim draw
    for order in [*orders, shuffled]:
        reg = PhaseRegistry()
        for slot, name, fn in order:
            reg.register(slot, name, fn)
        assert reg.describe() == EXPECTED
