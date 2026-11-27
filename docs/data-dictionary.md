# Data dictionary

Every table and column in a Plaza save (`saves/<slug>.plaza.sqlite`), schema v1 (migration `0001_initial`, PL-M0). Money is integer cents (US dollars); turn 0 is the save's `start_year`/`start_month` (January 2006 for the standard campaign). Kept current with every migration.

## save_meta (one row, id 1; updated in place)

| Column | Type | Meaning |
| --- | --- | --- |
| id | integer | Always 1 |
| name | string(80) | The save's name (its slug at creation) |
| game | string(20) | `plaza` (sim-core's `SaveMeta.game`) |
| master_seed | bigint | The master seed minus 2^63 (SQLite integers are signed 64-bit; seeds are 0..2^64-1) |
| start_year, start_month | integer | The month of turn 0 |
| start_turn | integer | The first turn played (0) |
| current_turn | integer | The next turn to play; after the campaign's last month, one past it |
| status | string(20) | `active` or `campaign_complete` |
| scenario_id | string(40) | The scenario in `scenarios.yaml` (`standard`) |
| difficulty | string(20) | `lieutenant`, `boss` or `kingpin` |
| ironman | boolean | Ironman mode (off by default; ADR PL-0011) |
| campaign_turns | integer | Months in the campaign (360) |
| ended_turn | integer, null | The last turn played once the campaign is complete |

## organisation (current state; the player's is id 1)

| Column | Type | Meaning |
| --- | --- | --- |
| id | integer | The organisation's id; the ledger's `entity_id` |
| name | string(120) | The organisation's name |
| leader_name | string(120) | The leader's name |
| background | string(40) | The leader's background id in `scenarios.yaml` |
| is_player | boolean | True for the player's organisation |

## ledger_entry (append-only)

| Column | Type | Meaning |
| --- | --- | --- |
| id | integer | Row id (posting order) |
| turn | integer, indexed | The turn the entry belongs to (turn 0 for the starting stake) |
| entity_id | integer, FK organisation.id | The organisation whose books it is in |
| book | string(20), indexed | `dirty` or `clean` (ADR PL-0003); every line's account is in this book |
| memo | text | What the entry records |
| link | string(80), null | Shared by the two entries of one laundering bridge transfer; null otherwise |

## ledger_line (append-only)

| Column | Type | Meaning |
| --- | --- | --- |
| id | integer | Row id |
| entry_id | integer, FK ledger_entry.id | Its entry |
| account | string(40), indexed | An account code from `accounts.yaml` (D... dirty, C... clean) |
| amount_cents | bigint | Debit positive, credit negative; an entry's lines sum to zero |
| currency | string(3) | `USD` |
| dims_json | text | Reporting dimensions as a JSON list of [name, value] pairs (empty at PL-M0) |

## turn_snapshot (append-only; one row per organisation per turn)

| Column | Type | Meaning |
| --- | --- | --- |
| id | integer | Row id |
| turn | integer, indexed | The turn played |
| entity_id | integer, FK organisation.id | The organisation |
| kpis_json | text | KPI name to value at the month's close: `dirty_cash_cents`, `clean_cash_cents` |

## turn_log (append-only)

| Column | Type | Meaning |
| --- | --- | --- |
| id | integer | Row id |
| turn | integer, indexed | The turn |
| entity_id | integer, null | The organisation it concerns, if any |
| kind | string(60) | The item's kind |
| message | text | Plain text |
| template | string(60), null | Inbox template key; null for turn-log only |
| params_json | text | Template parameters as a JSON list of [name, value] pairs |
| link_kind, link_id | string(40) null, integer null | The screen and record the item links to |

No turn writes a log item at PL-M0.

## alembic_version

Alembic's own table: the save's schema revision.
