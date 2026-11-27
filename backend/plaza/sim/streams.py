"""Plaza's stream table (ADR PL-0009; SC-0002).

Ids 1-19 are sim-core's core streams with TST's names and meanings; Plaza registers its own
rows 20-36 exactly as PL-0009's table lists them, and names the core `governance` stream
(17) `council`, as TST names it `board` and PT `partnership`. Ids 200-299 are reserved for
sim-core. The table is append-only: never renumber or reuse an id, it is part of every draw.

Nothing draws on Plaza's rows at PL-M0; each row's milestone adds its one call site
(TST ADR-0013, checked by tests/unit/test_rng_call_sites.py).
"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from simcore.kernel.rng import RngFactory, StreamTable

# name -> id, with the key each draw passes and the milestone that first draws on it.
OWN_ROWS: Final[Mapping[str, int]] = MappingProxyType(
    {
        "market": 20,  # (market, product): monthly demand noise (PL-M3b)
        "production": 21,  # (site_id,): a site's monthly output and quality noise (PL-M3b)
        "shipment": 22,  # (shipment_id,): a named shipment's transit, delay, outcome (PL-M3c)
        "plaza": 23,  # (plaza_id,): control and loyalty noise (PL-M3a)
        "heat": 24,  # (level, id): heat events at person, site, route level (PL-M5)
        "agency": 25,  # (agency_id, year): budget, priorities and target choice (PL-M5)
        "case": 26,  # (case_id,): a case's stage progress and outcome (PL-M5)
        "informant": 27,  # (person_id,): recruitment by the agency and reveal (PL-M5)
        "laundering": 28,  # (front_id,): leakage and audit draws (PL-M4)
        "rival_org": 29,  # (*rival_key,): a rival organisation's month (PL-M7)
        "war": 30,  # (war_id,): conflict resolution draws, PL-0010 (PL-M7)
        "supplier": 31,  # (supplier_id,): delivery and betrayal draws (PL-M3b)
        "council_vote": 32,  # (vote_id, person_id): each plaza holder's vote noise (PL-M6)
        "recruit_pool": 33,  # (region, search_id): regional recruitment pools (PL-M1b)
        "org_gen": 34,  # (org_index,): generated rival organisations at creation (PL-M7)
        "price": 35,  # (market, product): price walk after 2025 (PL-M3b)
        "policy": 36,  # (year,): seeded policy and enforcement shocks after 2025 (v2)
    }
)

ALIASES: Final[Mapping[str, str]] = MappingProxyType({"council": "governance"})

TABLE: Final = StreamTable.build(OWN_ROWS, aliases=ALIASES)


def rng_factory(master_seed: int) -> RngFactory:
    """The only way Plaza builds an RNG factory: the save's seed over Plaza's table."""
    return RngFactory(master_seed, TABLE)
