## PL-0009: Plaza's stream table, with kernel ids reserved

- Status: **Accepted** (Reece, 2026-11-26)
- Inherits: TST ADR-0002 and ADR-0013; PT-0012

**Decision.** `STREAM_IDS` is an append-only table. Ids **1–19** keep TST's names and meanings for ported systems (people\_gen 1, hiring 2, morale 3, events 6, founder 7 → the leader's build, growth 8, reveal 9, tags 10, resign 11 → desertion, actions 13, delegate 14, board 17 → `council`, poach 19). If `sim-core` publishes a unified table, Plaza adopts its numbering for 1–19 unchanged. Ids **20–99** are Plaza's; 99 stays `misc` for tests.

| Name | Id | Key | Used for | Milestone |
| --- | --- | --- | --- | --- |
| `market` | 20 | `(market, product)` | Monthly demand noise | PL-M3b |
| `production` | 21 | `(site_id,)` | A site's monthly output and quality noise | PL-M3b |
| `shipment` | 22 | `(shipment_id,)` | A named shipment's transit, delay and outcome | PL-M3c |
| `plaza` | 23 | `(plaza_id,)` | Control and loyalty noise | PL-M3a |
| `heat` | 24 | `(level, id)` | Heat events at person, site, route level | PL-M5 |
| `agency` | 25 | `(agency_id, year)` | Budget, priorities and target choice | PL-M5 |
| `case` | 26 | `(case_id,)` | A case's stage progress and outcome | PL-M5 |
| `informant` | 27 | `(person_id,)` | Recruitment by the agency and reveal | PL-M5 |
| `laundering` | 28 | `(front_id,)` | Leakage and audit draws | PL-M4 |
| `rival_org` | 29 | `(*rival_key,)` | A rival organisation's month | PL-M7 |
| `war` | 30 | `(war_id,)` | Conflict resolution draws (PL-0010) | PL-M7 |
| `supplier` | 31 | `(supplier_id,)` | Delivery and betrayal draws | PL-M3b |
| `council_vote` | 32 | `(vote_id, person_id)` | Each plaza holder's vote noise | PL-M6 |
| `recruit_pool` | 33 | `(region, search_id)` | Regional recruitment pools | PL-M1b |
| `org_gen` | 34 | `(org_index,)` | Generated rival organisations at creation | PL-M7 |
| `price` | 35 | `(market, product)` | Price walk after 2025 | PL-M3b |
| `policy` | 36 | `(year,)` | Seeded policy and enforcement shocks after 2025 | v2 |

**Consequences.** Every random draw is keyed and replayable; adding a system never shifts another system's draws.

