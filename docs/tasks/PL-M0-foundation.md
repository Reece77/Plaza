# PL-M0: Foundation (brief)

Nov 27, 2026 · @Reece DeHaan

Destined for `docs/tasks/PL-M0-foundation.md` in `Reece77/Plaza`. Format follows Partner Track's PT-M0 brief.

**Goal:** a new repository on `sim-core` v0.1.0 that already obeys the engine's rules: a pure, seeded simulation with a dirty book and a clean book on the shared ledger, one transaction per turn, the LLM seam, the UI shell and the content-rules guard. It starts in January 2006 with an empty organisation that can press Continue for 360 months, to December 2035.

**ADRs:** PL-0001 (amended 2026-11-27), PL-0002, PL-0003 (chart and books only), PL-0008, PL-0009, PL-0011; `sim-core` SC-0001 to SC-0011 · **Spec:** §1, §4.1, §10.1, §17 (shell) · **Reuse map:** §1.1, §2, §4 (shell), §5 · **Core:** `sim-core` v0.1.0 (`b2fc2db`) · **Depends on:** PL-D0 (complete) · **Lane:** A

## Reece's decisions

- **Repository:** `Reece77/Plaza` (public, empty, created by Reece). Package names stay lower case: `backend/plaza/`.
- **`sim-core` is public** and stays public, so no access token or Actions secret is needed; depend on `simcore[db,llm] @ git+https://github.com/Reece77/sim-core@v0.1.0` (note the GitHub name is `Sim-core`; either spelling resolves).
- **Read-only:** `Reece77/Tech_Executive_Tycoon`, `Reece77/LawGame` and `Reece77/Sim-core`. Plaza never edits them; core bugs go to Reece for a `sim-core` session.
- **The design pack is the source of truth:** roadmap, reuse map, ADRs PL-0001 to PL-0011, spec v0.1, questions and the v1 dossier (Claude docs, linked from `docs/README.md`). Copy each into `docs/` in sub-task 1, unchanged.

## Out of scope

People, hiring, org (PL-M1a onward, on `sim-core` 0.2), territory, products, supply, logistics, heat, the agency, the council and rivals. No stub modules for them. No seed data beyond what this milestone needs.

## Sub-tasks (commit after each)

1. **Repository and tooling.** `backend/plaza/` (`sim/`, `db/`, `api/`, `llm/`), `frontend/`, `docs/` (the design pack as above, plus `docs/tasks/`), the engine's `Makefile` targets, `ruff.toml`, `uv`, `pnpm`, pre-commit, CI workflows (`check`, `e2e`, `determinism`, `nightly`, `tag-milestone`) adapted from Partner Track's, tag pattern `pl-m*-done`. `CLAUDE.md` and `AGENTS.md` adapted from PT's: same rules and definition of done, the repository map, the read-only rule for the three upstream repositories, and the content rules of PL-0008 in full. A pin test fails on any `sim-core` dependency that is not a tag.
2. **Content-rules guard (PL-0008 §6).** `tools/content_rules/` with a maintained list of out-of-bounds terms and patterns, and a test (`tests/test_content_rules.py`) that lints `backend/plaza/data/`, `docs/`, LLM prompt templates and code comments. It ships with its own fixture tests (a forbidden-term fixture fails, a news-level fixture passes). The list itself is reviewed by Reece at merge.
3. **Streams (PL-0009).** Plaza's rows 20–36 registered with `StreamTable.build(own_rows, aliases={"council": "governance"})`, avoiding 200–299; `RngFactory(seed, TABLE)`. Stream call-site check from `simcore_testing`.
4. **Calendar and scenario.** `scenarios.yaml` with the standard campaign: `start_ym` 2006-01, 360 turns. The save stores the start; `turn_to_ym` is always called with it (a test fails on a call without `start`).
5. **Books and chart (PL-0003).** A `Chart` with two books, **`dirty`** and **`clean`**, declared as `sim-core` books with `accounts.yaml` per PL-0003 §6, and a laundering `BookBridge` from dirty to clean (fee and leakage as data, unused until PL-M4). Starting entry: a small dirty-cash stake (debit dirty cash, credit leader's equity); the clean book starts empty (questions 16). Property tests: every entry balances within one book; only the bridge crosses books; assets = liabilities + equity in each book every month.
6. **State and turn.** A `CoreState` with Plaza's sub-states for save meta and the organisation (name, leader name, background), empty otherwise; the twelve slots registered with Plaza's phase names from PL-0002 §5 as no-ops in fixed order; `advance_turn`, `TurnResult`, and a `KpiProvider` for dirty cash and clean cash.
7. **Persistence and API.** `simcore_db` with suffix `.plaza.sqlite`, Alembic schema v1 in Plaza's own chain, one transaction per turn, backups every 12 turns; FastAPI with `new-game`, `advance`, `state`, `saves`; OpenAPI and the generated TypeScript client; CLI `plaza new-game`, `advance`, `inspect`. `simcore_llm` wired with Plaza's text kinds declared (field report, council minutes, informant tip, year-end report) and the template adapter as default; no text is generated yet.
8. **Front-end shell.** The `sim-core` `ui/` shell (hash-checked against `MANIFEST.json`) plus TST's tables, Explain plumbing, command palette, hotkeys, tokens and fonts, ported as PT did. Screens: Main menu, New game (organisation name, leader name, background, difficulty: Lieutenant, Boss, Kingpin; Ironman off by default), Overview (date, dirty cash, clean cash, Continue), Saves, Settings (LLM budget meter). A launcher shortcut as in TST and PT.
9. **Guards.** From `simcore_testing`: purity (`plaza.sim` may not import `plaza.db`, `plaza.api`, `plaza.llm`, `random`, `time` or the filesystem), stream call sites, the float-money guard, golden framework with the pytest plugin. Plaza's own: turn order, migration chain, state-cache test. Golden seeds 1–3 for 360 empty turns.

## Acceptance criteria

- [ ] `make check` and CI green, including the content-rules test and the tag-pin test.
- [ ] A new game in January 2006 advances 360 turns headless (`plaza advance --turns 360`) and ends in December 2035; the save reloads cold at any turn.
- [ ] Killing the process mid-turn leaves the save at the previous turn (test).
- [ ] Both books balance every month, and nothing crosses between them except through the bridge (property test).
- [ ] Same seed, same results on two processes (the determinism job).
- [ ] The content-rules guard fails on its forbidden fixture and passes on the design pack as copied.
- [ ] Merged through a pull request with `Milestone-Tag: pl-m0-done`.

## Manual check (Reece)

Start the game with the launcher, create an organisation with each background, press Continue a few times, see dirty cash on the Overview, close and reopen the save.

## Notes for the session

- `tests/consumers/plaza_like.py` in `sim-core` (532 lines) is a worked example of heat, territory, the two books with a leaky bridge, investigations and the council. Read it before sub-tasks 5 and 6; do not copy its domain code, which belongs to later milestones.
- Follow `sim-core`'s `docs/adoption.md` ("Both games" steps 1–12 apply to a new game too) and record any departure in this brief's **Decisions made** section, as PT-M0 did.
- When `sim-core` 0.2 is tagged, upgrading is the first sub-task of PL-M1a, not part of this milestone.

## Decisions made

1. **Upstream commits.** sim-core `v0.1.0` (`b2fc2db`), locked in `backend/uv.lock`. Ported files name their source: TST `3da2f5b1` (launcher, palette, hotkeys, recent items, Explain, tokens and fonts) and Partner Track `0e13dca7` and its `pt-m0-done` tree (scaffolding, DataTable, table features, workflows, Alembic environment).
2. **The design pack copy.** Each Claude doc was exported as Markdown on 2026-11-27 and written byte for byte (byte counts checked against the export). The ADR document is split one section per file, as its status line asks; `docs/adr/README.md` keeps its preamble and closing section verbatim, and `tests/unit/test_design_pack.py` checks that the files rejoin to the exported document's sha256 and that the other copied documents are unchanged. This brief is the one copied file that changes (this section). The concept document is not copied: the pack supersedes it.
3. **Phases and slots.** sim-core's twelve slots are positions; Plaza's twelve phases fill them one each in PL-0002 section 5's order (`world_and_policy_shocks` in `decisions` through `snapshot` in `requests`), so the slot order is the phase order. Only `snapshot` has a body. When the player's orders need their own phase, it registers in the `decisions` slot with `before=("world_and_policy_shocks",)`.
4. **The snapshot and its KPI provider.** A `KpiProvider` reads `(state, entity)` and the ledger is not part of the state, so `CashKpis` is built each month over the closing balances inside the `snapshot` phase.
5. **The default book.** sim-core's `Chart` needs exactly one book with the empty prefix; `clean` is that book (as in sim-core's Plaza-shaped consumer) and `dirty` has prefix `D`. So a mistyped account cannot fall silently into the clean book, every clean code must start with `C` (data model) and `check_declared` refuses any account `accounts.yaml` does not declare in the entry's book, on every turn.
6. **Accounts.** PL-0003 section 6's list, by book: dirty assets, liabilities, the leader's equity, sales and plaza tax, the six costs, and `D5900_laundered_out` (the bridge's sending side); clean cash, fronts, legitimate assets, the leader's lawful equity, front revenue, front costs, losses and `C4900_laundered_in` (the receiving side). Types are asset, liability, equity, income and cost.
7. **Fee and leakage.** sim-core's bridge carries leakage only, so `balance.yaml` holds both rates (fee 1,500 bp, leakage 500 bp, placeholders) and the bridge takes its leakage from it; PL-M4 posts the fee as a dirty-book cost.
8. **The accounting equation test.** With debits positive and nothing closed to equity yet, "assets = liabilities + equity" is checked in each book every month as assets + costs + liabilities + equity + income = 0 (assets = liabilities + equity + current earnings).
9. **The starting stake.** $100,000 of dirty cash (`start.dirty_stake_cents`, a tunable), debit `D1000_cash`, credit `D3000_leader_equity`, on turn 0; the clean book starts empty (questions 16). Backgrounds and difficulties are recorded only; their effects arrive with the systems they touch.
10. **Save state.** Sub-states `organisation` (name, leader name, background) and `save` (scenario, difficulty, Ironman, campaign length, ended turn). Campaign end uses sim-core's `SaveMeta.status`: after turn 359 (December 2035) the save is `campaign_complete`; a further turn raises `GameOverError` (HTTP 409). Saves keep tables, not a state blob; a test checks that a state read back encodes exactly as the one written (SC-0003's mapper contract). The seed is stored minus 2^63, as in PT.
11. **The killed-process test.** A child process writes the month's rows inside the open transaction, signals through a marker file, and is killed with SIGKILL before the commit; the save reopens at the previous turn and plays on.
12. **The LLM default.** sim-core's `LLMSettings` defaults to Claude; Plaza uses the template adapter until the player saves a choice in Settings. The four text kinds and their system prompts live in `backend/plaza/llm/prompts.yaml`, linted by the guard; council minutes and the year-end report use the story model.
13. **The content-rules guard.** Its test is `backend/tests/test_content_rules.py` (the brief's `tests/`, inside the backend suite so `make check` runs it). The list targets vocabulary that only appears in procedural or graphic text (laboratory operations and equipment, laboratory-scale quantities, temperatures, yields and ratios, two laundering patterns and one concealment pattern, and section 4's three prohibitions), with negative look-behinds so the prohibitions as PL-0008 itself words them pass. It names no real reagent, process or person: a name list would itself break sections 2 and 3, so the real-name check stays with the PL-M8 validator. It reads seed data, prompt templates, every Markdown file in `docs/` and at the root, and the comments and docstrings of every Python, TypeScript and JavaScript file. A line-level `content-rules-allow: <rule>` marker exists for review; none is used. The forbidden fixture trips every rule with harmless kitchen and office sentences.
14. **`httpx` for the test client.** TST and PT list `httpx2`; this session's safety check refused to install it, so Plaza's dev group uses `httpx`, which FastAPI's `TestClient` needs. Recorded as a departure from ADR-0001's list as the games apply it.
15. **Front end.** TST's tokens are used unchanged (their `tst-` names kept, since the ported components use them). Saved column views, the glossary and unlock gating are not ported (each needs an API Plaza does not have yet); the palette lists screens only. Explain is real for the two cash KPIs: every posted line on the account (`GET /api/saves/{slug}/explain/{kpi}`). `src/core` is excluded from Prettier so the copy stays byte-identical.
16. **CI.** One `check` job (no shards yet), `e2e`, `determinism` (the golden seeds and state cache in two processes, on pull requests and `main`), `nightly` (seeds 1-10, 360 turns) and `tag-milestone` (`pl-m*-done`).
17. **Launcher.** TST's, with port 8790 so it runs beside TST's (8770).

**Reported to Reece (sim-core, none blocking):** `docs/adoption.md` step 1 still asks for a read token, which a public sim-core does not need (none is used); `ui/lib/slug.ts` names its parameter `companyName`, a game noun in the shared shell; `KpiProvider` cannot see the ledger, so every game will build balance KPIs as decision 4 does; and `Chart`'s required empty-prefix default book (decision 5) means a game with no natural default book needs its own guard.

## Prompt to start the session

```markdown
You are the engineer for Plaza (repository Reece77/Plaza), a single-player management game on the shared sim-core engine. Address me as Reece; be direct and formal.

Implement PL-M0 exactly as briefed in the Claude doc "PL-M0: Foundation (brief)". Read the Plaza design pack it links (roadmap, reuse map, ADRs PL-0001 to PL-0011, spec v0.1, questions, dossier) and sim-core's CLAUDE.md, docs/adr and docs/adoption.md first.

Read-only: Reece77/Tech_Executive_Tycoon, Reece77/LawGame, Reece77/Sim-core. Depend on sim-core by tag v0.1.0. The content rules in ADR PL-0008 are non-negotiable in every file, comment and prompt.

Work sub-task by sub-task, committing after each, on a branch; open one pull request with the trailer Milestone-Tag: pl-m0-done when every acceptance criterion passes. Report anything in sim-core that blocks you instead of working around it.
```

## Ideas to expand

- Add the territory map component as a spike branch alongside PL-M0, since no map exists in either game and PL-M3a is on the critical path.
- Seed `plazas.yaml` for the 24-plaza map during PL-M0's review, under the content-rules guard, so PL-M3a starts with data in hand.
