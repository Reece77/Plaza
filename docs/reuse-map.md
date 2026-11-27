# Plaza Reuse Map v0.1

Nov 26, 2026 · @Reece DeHaan

**Status: ACCEPTED by Reece (2026-11-26).** First deliverable of PL-D0; destined for `docs/reuse-map.md`. Read against `Reece77/Tech_Executive_Tycoon` at `main` `3da2f5b` (M54 merged, 2026-11-26) and `Reece77/LawGame` (Partner Track) at `main` `0329497` (PT-M12 fix merged, 2026-11-26).

## How to read this

| Mark | Meaning |
| --- | --- |
| **AS IS** | Used unchanged: from `sim-core` once extracted, otherwise vendored with a hash check (PT's `tools/check_vendored.py`). |
| **CHANGED** | Copied, then adapted. Formulas and code shape stay; domain nouns and some terms change. |
| **PATTERN** | Not copied; its structure, rules and tests are the template for a new Plaza module. |
| **NOT USED** | Nothing carried over. |

**Source** names where to take it from. Where both games have a module, Plaza takes **Partner Track's** version: PT already removed the tech-industry imports and routes its seams through `ptk/sim/interfaces.py`. **Core?** marks a candidate for the shared `sim-core` (input to PT-M19's extraction plan).

## The three findings that drive everything below

1. **Partner Track already paid the de-tech cost.** TST's general modules (org, automation, events, founder, family, rivals) import products and markets; PT's ports of them do not. Porting from PT roughly halves Plaza's adaptation work on the people and governance spine.
2. **State and turn wiring are still per game.** Both games build their own `GameState` and their own 12-phase `turn.py`. This is the problem `sim-core` has to solve (a phase registry and composable sub-states); Plaza should ask for it in the extraction plan rather than write a third copy.
3. **Plaza's five new systems each have a partial analogue.** PT's partnership governance is the council; TST's regulation cases plus PT's risk module are the law-enforcement case machinery; PT's trust accounts (client money kept apart, ADR PT-0003) are the precedent for two books; TST's negotiation and meetings are sit-downs and the December council; TST's geopolitics and world are policy shocks and rival organisations. Only territory, heat and abstract conflict are wholly new.

## 1. Simulation core

### 1.1 Kernel

| Module | Source | Mark | Core? | Notes |
| --- | --- | --- | --- | --- |
| `rng.py`, `money.py`, `ledger.py`, `dmath.py`, `scale.py`, `log.py`, `decisions.py` | TST | **AS IS** | yes | Plaza gets its own append-only `STREAM_IDS` range, keeping ids 1–19 as PT did (ADR PT-0012). |
| `calendar.py` | PT | **AS IS** | yes | PT already made turn 0 a data value; Plaza sets January 2006. |
| `errors.py` | PT | **CHANGED** | base classes | Keep base and generic errors; add territory, shipment, laundering and council errors. |
| `snapshot.py`, `score.py`, `whatnext.py` | PT | **CHANGED** | mechanism | KPIs become revenue, dirty and clean cash, territory held, organisation heat, members by role. Score per the concept: revenue, territory, survival, clean wealth. |
| `setup.py` | PT | **CHANGED** | — | The breakaway start: crew, one plaza, one product line, background lean. |
| `state.py`, `turn.py` | both | **PATTERN** | ask | New `GameState` and phase bodies; see finding 2. |
| `data_models.py` | PT | **CHANGED** | loaders | Keep people, personality, tags, interests, regions, macro, events; add products, precursors, reagent categories, equipment tiers, routes, plazas, agencies, policy shocks. |
| `unlocks.py` | TST | **CHANGED** | mechanism | Unlocks: cells at a crew size, second product, fronts, a council seat, a second corridor (v2). |
| `coo.py` | TST | **CHANGED** | — | The briefing comes from the player's second-in-command. |
| `interfaces.py` | PT | **CHANGED** | yes | `WorkSource`, `KpiProvider`, `AreaRule`, `EffectType`; Plaza adds heat and territory providers. |

### 1.2 People, recruitment and organisation

| Module | Source | Mark | Core? | Notes |
| --- | --- | --- | --- | --- |
| `people/` | PT | **CHANGED** (light) | yes | Data-driven skills and roles. Adds a hidden **informant risk** beside poachability; PT's per-person strain carries over. Reveal as is. |
| `hiring/` | PT | **CHANGED** | yes | Offers and acceptance become recruitment from regional pools with a sponsor who vouches; resignation becomes desertion; arrests and conflict remove members. |
| `org/` | PT | **CHANGED** | yes | Units become cells and crews; span of control and manager quality port; **compartmentalisation against coordination** is new. |
| `actions/` | TST/PT | **CHANGED** | framework | Immediate-action framework (ADR-0014) as is; action bodies new. |
| `automation/` | PT | **CHANGED** | framework | Areas become production, logistics, laundering, security, recruitment; money limits, one-offs and the digest port. |

### 1.3 Money, governance and the leader

| Module | Source | Mark | Core? | Notes |
| --- | --- | --- | --- | --- |
| `finance/` | TST | **CHANGED** | statements | Statements, loans and the macro layer port; cap table and fundraising do not. The **two books** split is new (ADR PL-0003), modelled on PT's trust accounts. |
| `partnership/` | PT | **CHANGED** | ask | Becomes **the council**: confidence, comp systems become tribute and splits by earner, elections become deposition, partner flight becomes defections and crew splits. |
| `founder/` | PT | **CHANGED** (light) | yes | Stress, persona, the personal account; the leader's wealth sits in the clean book. |
| `family/` | TST/PT | **CHANGED** (v2) | yes | Heirs and succession by council. |
| `dynasty/`, `modes/` | TST | **CHANGED** | yes | Modes in v1 (Campaign, Sandbox, continue until); dynasty in v3. |
| `regulation/` (TST) + `risk/` (PT) | both | **CHANGED** | ask | Case machinery (visible stages, odds as ranges, warnings ahead) becomes investigations, raids, indictments, trials and pleas. Settle and contest become plea and trial. |
| `rivals/` | PT | **CHANGED** | AI only | Utility AI, personalities, poaching both ways and history port; PT's boutique spin-offs become **splinter groups**. |
| `events/` | PT | **CHANGED** | framework | Director, slots, severity caps, storylines port; triggers, effects and templates are new; the validator carries the content rules. |
| `negotiation/` | TST | **CHANGED** | yes | Sit-downs: supplier terms, transit-partner deals, truces and tribute, with the counterpart's hidden zone. |
| `meetings/` | TST | **CHANGED** | yes | The December council as a meeting with agenda items and hidden priorities. |
| `contracts/` | TST | **CHANGED** | yes | Supplier and transit agreements; counterparties' memory becomes memory of betrayal. |
| `press/` | TST | **CHANGED** | — | Press attention feeds organisation heat; rival leaders' public profile. |
| `geo/` | PT | **CHANGED** | yes | Regions and cities port; plazas sit on top (new). |
| `world/`, `geopolitics/` | TST | **PATTERN** | — | World news and organisation pages; tension and tariffs become dated policy shocks, border measures and sanctions. |
| `commodities/` | TST | **PATTERN** | — | Wholesale and street price indexes by market. |
| `matters/` | PT | **PATTERN** | — | Its two fidelity tiers (named matters and flow work) become named shipments and routine flow. |
| `mergers/` (PT), `mna/`, `group/` (TST) | both | **PATTERN** (v2) | — | Alliances and absorbing a rival; fronts held as subsidiaries for the legitimacy exit. |
| `tech/` (PT) | PT | **PATTERN** (v2) | — | Adoption eras become enforcement technology eras. |
| `fx/`, `finserv/` | TST | **PATTERN** (v2) | — | Currency of cross-border cash; banks as a laundering channel with compliance risk, at abstract stats only. |
| `reputation/` | PT | **PATTERN** | — | Reputation becomes fear and respect by plaza. |
| `talks/` | TST | **NOT USED** (v1) | — | Reconsider for v2 parleys. |

### 1.4 Industry modules

| Module | Mark | Notes |
| --- | --- | --- |
| `products/` | **PATTERN** | Demand by market and price score. |
| `research/` | **PATTERN** | Tree, named modifiers and eras (v2). |
| `facilities/`, `refining/` | **PATTERN** | Sites with capacity, footprint and outages; outages become raids. |
| `equipment/` | **PATTERN** | Tiers and traceable imports. |
| `billing/`, `rankings/` (PT); `hardware/`, `chips/`, `fabs/`, `exploration/`, `mining/`, `power/`, `platforms/`, `vehicles/`, `robotics/`, `space/`, `telecom/`, `medical/`, `pharma/`, `government/`, `markets_public/`, `markets/` (TST) | **NOT USED** |  |

## 2. Backend outside the core

| Module | Mark | Notes |
| --- | --- | --- |
| `llm/` | **AS IS** | New text kinds: field report, council minutes, informant tip, year-end report. |
| `events/` service and validator | **CHANGED** | The validator gains the content-rule checks (procedural detail, graphic violence, real names); every event keeps an offline template. |
| `conversations/` (TST) | **CHANGED** | Prompt builders for sit-downs and the council; hidden values never reach a prompt (ADR-0023). |
| `db/` session, migrate, backup, saves, history, inbox | **AS IS** | One SQLite file per save, transactional turns, backups. |
| `db/` models, mappers, state I/O | **PATTERN** | New tables for the new state. |
| `api/` app, deps, errors, interruptions, Explain plumbing | **AS IS / CHANGED** | Routers and schemas follow their modules. |
| `advisor/` | **CHANGED** | Explain breakdowns for heat, seizure odds, laundering loss and council confidence. |
| `balance/` | **PATTERN** | Runner, seeds, strategy scripts, known misses, nightly and weekly split. |
| `mods/`, `profile/`, `holiday.py`, `ui_settings.py` | **AS IS** | Achievement list new. |

## 3. Seed data

| Mark | Files |
| --- | --- |
| **AS IS** | `personality.yaml`, `interests.yaml` |
| **CHANGED** | `names.yaml` (regional pools), `skills.yaml` (production, logistics, discretion, security, finance, influence, leadership), `roles.yaml`, `tags.yaml`, `balance.yaml`, `glossary.yaml`, `achievements.yaml` |
| **New** | `products.yaml`, `precursors.yaml`, `reagent_categories.yaml`, `equipment_tiers.yaml`, `routes.yaml`, `plazas.yaml`, `agencies.yaml`, `policy_shocks.yaml`, `fronts.yaml` — every one under the content rules and the guard test |
| **NOT USED** | Every industry, firm and client file from both games |

## 4. Front end

| Area | Mark | Notes |
| --- | --- | --- |
| Shell, tables, Explain, help, inbox, Holiday, game flow, saves, settings | **AS IS** | Football Manager feel: dark, dense, keyboard-first. Nav list changes. |
| People, Person, recruitment | **CHANGED** | Role, loyalty, informant-risk range, morale. |
| Org | **CHANGED** | Cell diagram, crews, span badges. |
| Finance | **CHANGED** | Two books side by side, fronts, laundering capacity. |
| Rivals and world | **CHANGED** | Rival organisations, world news, policy timeline. |
| Automation | **CHANGED** | Plaza's areas. |
| Regulation screen | **PATTERN** | Investigations and cases. |
| **New screens** | — | Territory map (no map component exists in either game), Supply chain, Shipments, Heat, Council. |

## 5. Tooling, tests and CI

| Item | Mark | Notes |
| --- | --- | --- |
| Makefile, uv, pnpm, ruff, pre-commit, Alembic, CI workflows, milestone tagging | **AS IS** | Paths change. |
| Purity, turn-order, RNG uniqueness, ledger and clamp property tests, golden framework | **AS IS** |  |
| `tools/check_vendored.py` (PT) | **AS IS** | Only if Plaza transplants rather than depends on `sim-core`. |
| **Content-rules guard test** | **New** | Lints data, prompts, comments and LLM drafts against the Out column of the content rules (ADR PL-0008). |
| `CLAUDE.md`, `AGENTS.md` | **CHANGED** | Same rules and process; adds the content rules. |

## 6. Size estimate

|  | On `sim-core` | Transplanted |
| --- | --- | --- |
| Lines Plaza writes or adapts | about 45,000 | about 60,000 |
| Lines taken without edits | about 15,000 (from the core) | about 8,000 |

These are planning figures from module line counts, not measurements.

## 7. What is new for Plaza

| System | Nearest analogue |
| --- | --- |
| **Territory**: plazas with control, tax yield, local loyalty, contested status | none; `geo/` gives the regions underneath |
| **Heat** per person, site, route and organisation, with slow decay | press credibility (TST), PT strain, generalised |
| **Law enforcement as an adversary** with budget, priorities, research and political cycle | rivals' utility AI plus the case machinery |
| **Abstract conflict** from strength, morale, money and intelligence | none |
| **Two books** and fronts with laundering capacity, leakage and seizure | PT trust accounts |
| **Supply graph**: products, precursor nodes, reagent categories, equipment tiers, linked by "requires" | TST commodity and chain links |
| **Informant risk** as a hidden per-person value | poachability |
| **Compartmentalisation** as an org trade-off | span of control |

## 8. Asks for PT-M19's `sim-core` plan

1. A **phase registry** and composable sub-states, so no game hand-wires `turn.py` or a 150-field `GameState`.
2. A **multi-book ledger**: PT's trust accounts and Plaza's two books are the same shape.
3. A **generic case machinery** (stages, odds ranges, outcomes) serving TST regulation, PT discipline and Plaza investigations.
4. A **governing body** abstraction (TST board, PT partnership, Plaza council): confidence, votes, removal, succession.
5. Interfaces tested against Plaza's heat and territory providers before they freeze.

## Ideas to expand

- Measure finding 1 precisely: count PT modules with zero product or market imports, to confirm which can go to `sim-core` unchanged.
- Prototype the territory map component early (PL-M3a is on the critical path and nothing exists).
- Reuse TST's hidden-value discipline (ADR-0023) for informant risk, so an informant is never visible through the API or a prompt.
