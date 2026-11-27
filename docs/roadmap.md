# Plaza Roadmap v0.1

Nov 26, 2026 · @Reece DeHaan

**Status: ACCEPTED by Reece (2026-11-26).** Same process as Tech Startup Tycoon (TST) and Partner Track (PT): one brief per milestone in `docs/tasks/`, up to three lanes at once, one named session merges each milestone by pull request with a `Milestone-Tag:` trailer (`pl-m3a-done`), a Codex review every five to six milestones, and a playtest on a played save every second milestone. Ids are prefixed `PL-`.

## Sequencing decision: sim-core first

Plaza is the third consumer of the engine. PT's `sim-core` checkpoint is now due (TST v5 closed 2026-11-21; PT-M7 merged), and the extraction plan is written during PT-M19.

**Recommendation:** run Plaza's design pack (PL-D0) now, in parallel with PT-M19, and start code (PL-M0) on the extracted `sim-core`. Plaza's territory, heat and adversary systems should be raised as requirements in that extraction plan so the shared interfaces (`WorkSource`, `KpiProvider`, `AreaRule`, `EffectType`) are tested against a third game before they freeze. If extraction would cost more than two milestones, fall back to a selective transplant with provenance (ADR PT-0001), as PT did.

Effect on size: v1 is about 11 code milestones on `sim-core`, or about 14 transplanted.

## PL-D0: design pack (documents only, before any code) — COMPLETE 2026-11-26

| Deliverable | Contents |
| --- | --- |
| `docs/reuse-map.md` | TST and PT modules marked AS IS / CHANGED / PATTERN / NOT USED for Plaza |
| `docs/adr/` | PL-0001 code sharing and `sim-core`; PL-0002 time model; PL-0003 two-book ledger; PL-0004 territory; PL-0005 heat; PL-0006 law enforcement as adversary; PL-0007 council and succession; PL-0008 content rules (with the guard test that enforces them) |
| `docs/game-design-spec.md` v0.1 | structured like PT's spec |
| `docs/research/` v1 dossier | public macro sources only (seizure statistics, market-size estimates, policy timelines, enforcement eras), each fact tagged S / D / A |
| `docs/questions.md` | open decisions with proposed defaults |

## v1: the playable core (2006–2016, one corridor)

Goal: a breakaway lieutenant starts in January 2006 with a small crew, one plaza and one product line; grows production, moves product along one corridor into one consumer market, launders through fronts, survives the 2006 escalation and the council's December confidence vote, and plays ten years against rival organisations and an adapting state.

| Milestone | Lane | What | Depends on |
| --- | --- | --- | --- |
| **PL-M0, foundation** | A | new repository on `sim-core` (or vendored kernel); content-rules guard test; calendar from 2006; schema v1; phase runner; API and UI shell; CI | PL-D0 |
| **PL-M1a, members** | A | roles (lieutenant, producer, courier, accountant, fixer, enforcer, lookout), skills, loyalty, ambition, hidden informant risk, growth, reveal | PL-M0 |
| **PL-M1b, recruitment and morale** | A | recruitment pools, cuts and pay, morale, desertion, members lost to arrest or conflict | PL-M1a |
| **PL-M2, cells and structure** | B | cells, crews, regions, span of control, compartmentalisation against coordination, delegated recruitment | PL-M1a |
| **PL-M3a, territory** | A | the corridor's plaza map: control, tax yield, local loyalty, contested status | PL-M1b, PL-M2 |
| **PL-M3b, products and supply** | B | three products with demand by market; precursors as supply nodes; reagent categories; equipment tiers; sites, capacity and quality tier | PL-M3a's site model |
| **PL-M3c, logistics** | C | route categories on the corridor, capacity, transit time, seizure risk; shipments as the season's fixtures | PL-M3b |
| **PL-M4, two books** | A | dirty and clean ledgers on the double-entry kernel, fronts, laundering capacity and leakage, audit risk, asset seizure | PL-M3b |
| **PL-M5, heat and the state** | A | heat per person, site, route and organisation; one fictional agency with budget and priorities; investigations, raids, informants, indictments, trials and pleas | PL-M3c, PL-M4 |
| **PL-M6, the council** | B | plaza holders, confidence, tribute and splits, the December council, deposition, defections and crew splits | PL-M4 |
| **PL-M7, rival organisations** | B | generated organisations, utility AI, poaching, turf contests, abstract conflict resolution in reports | PL-M3a, PL-M5 |
| **PL-M8, events and the LLM** | C | templates, context builder, validator carrying the content rules, critical events, storylines, the year-end report | PL-M5 |
| **PL-M9, screens** | C | Organisation, Member, Territory map, Supply chain, Shipments, Books, Heat, Council | runs beside PL-M3 to PL-M7 |
| **PL-M10, balance and v1 close** | A | strategy scripts, news-level history 2006–2016, Holiday, History, onboarding, the 10-year run | all of v1 |

**Lanes.** A carries the spine (people → territory → books → heat → balance). B joins at PL-M2 on systems touching few shared files. C does logistics, events and screens. PL-M3b and PL-M5 are the riskiest and start as early as their dependencies allow.

**Playtests.** First full playtest after PL-M6 (the council makes the loop complete); then every second milestone.

## v2: depth (to 2035)

| Milestone | What | Ports |
| --- | --- | --- |
| PL-M11, research tree | all six branches (production, logistics, concealment, finance, security and influence, organisation) as named modifiers | TST `research/` |
| PL-M12, precursor eras and substitution | dated control shocks, substitution races, the shift to synthetics |  |
| PL-M13, history to 2025, then seeded | enforcement eras (kingpin strategy, extradition, crypto, encrypted-phone takedowns, sanctions) pinned to 2025, then seeded cycles to 2035 | PT-M10 pattern |
| PL-M14, corridors and markets | additional producing regions, transit corridors and consumer markets |  |
| PL-M15, wars and alliances | declared conflicts, truces, alliances, splinter groups after a leader's fall |  |
| PL-M16, influence and corruption | protection, corruption reach and its informant risk, political cycles |  |
| PL-M17, delegation everywhere | areas, money limits, one-offs, the monthly digest, Automation screen | TST M27a |
| PL-M18, the leader's life and succession | persona, family, heirs, succession by council | TST M24, M26, M36 |
| PL-M19, legitimacy exit | moving clean wealth into lawful businesses before the law catches up; scored as a win |  |
| PL-M20, v2 balance | seeds 1–40, 30-year targets, turn time, nightly run | runs alone |

## v3: the world

Global routes and markets, more adversary agencies, scenario starts, dynasty mode; a shared-world link with TST and PT if `sim-core` allows it.

## Decisions (all five defaults accepted by Reece, 2026-11-26)

1. **Sequencing.** Design pack now in parallel with PT-M19; code on extracted `sim-core`. *Default: yes.*
2. **First corridor.** One producing region, one transit corridor (northern Mexico border crossings), one consumer market (US Southwest). *Default: yes.*
3. **Starting products.** One plant-based, one synthetic, one emerging synthetic that rises in the late 2010s. *Default: yes.*
4. **Lanes.** Plaza takes one lane while PT v3 runs, rising to three when PT reaches a balance pass. *Default: yes.*
5. **Design pack order.** Reuse map, then ADRs, then spec, then questions, each shown to you before the next. *Default: yes.*

## Ideas to expand

- A press and public-opinion layer feeding political cycles, so violence in reports moves enforcement budgets.
- A street-price index per market as the game's "league table" alongside market share.
- Informant play in reverse: the player planting moles in rivals and the agency.
- A post-v1 "what killed us" retrospective screen built from the event log after game over.
