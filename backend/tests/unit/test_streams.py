"""ADR PL-0009: Plaza's rows 20-36 on sim-core's table, `council` naming `governance`."""

from __future__ import annotations

import numpy as np
import pytest
from simcore.kernel.errors import StreamRegistrationError
from simcore.kernel.rng import CORE_RESERVED, CORE_STREAMS, RngFactory, StreamTable, derive

from plaza.sim.streams import ALIASES, OWN_ROWS, TABLE, rng_factory

PL_0009 = {
    "market": 20,
    "production": 21,
    "shipment": 22,
    "plaza": 23,
    "heat": 24,
    "agency": 25,
    "case": 26,
    "informant": 27,
    "laundering": 28,
    "rival_org": 29,
    "war": 30,
    "supplier": 31,
    "council_vote": 32,
    "recruit_pool": 33,
    "org_gen": 34,
    "price": 35,
    "policy": 36,
}


def test_own_rows_are_pl_0009s_table() -> None:
    assert dict(OWN_ROWS) == PL_0009
    assert sorted(OWN_ROWS.values()) == list(range(20, 37))
    assert not set(OWN_ROWS.values()) & set(CORE_RESERVED)


def test_table_holds_the_core_rows_unchanged_and_the_alias() -> None:
    for name, sid in CORE_STREAMS.items():
        assert TABLE.id_of(name) == sid
    assert dict(ALIASES) == {"council": "governance"}
    assert TABLE.id_of("council") == CORE_STREAMS["governance"] == 17
    assert len(TABLE.ids) == len(CORE_STREAMS) + len(PL_0009) + 1


def test_registration_refuses_the_reserved_and_core_ranges() -> None:
    with pytest.raises(StreamRegistrationError):
        StreamTable.build({"later": 200})
    with pytest.raises(StreamRegistrationError):
        StreamTable.build({"hiring_again": 2})


def test_draws_are_seeded_derived_and_independent() -> None:
    a, b = rng_factory(42), rng_factory(42)
    assert isinstance(a, RngFactory) and a.table is TABLE
    first = a.stream(5, "plaza", 3).integers(0, 1_000_000, 8)
    assert np.array_equal(first, b.stream(5, "plaza", 3).integers(0, 1_000_000, 8))
    assert np.array_equal(first, derive(42, 5, 23, 3).integers(0, 1_000_000, 8))
    assert not np.array_equal(first, a.stream(5, "plaza", 4).integers(0, 1_000_000, 8))
    assert not np.array_equal(
        first, rng_factory(43).stream(5, "plaza", 3).integers(0, 1_000_000, 8)
    )
