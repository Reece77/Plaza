# CLAUDE.md — Plaza

Read this file fully before every task. It is the contract between the owner (Reece) and any coding agent working in this repository. It follows Partner Track's CLAUDE.md (`Reece77/LawGame`), with Plaza's changes.

## 1. What this project is

A single-player, turn-based management game for personal use: Football Manager for a fictional criminal organisation. The player is a lieutenant who breaks away in **January 2006** and grows the organisation over a **360-turn (30-year)** standard campaign to December 2035. It is told through reports, ledgers and briefings, and says nothing operational (section 3).

- Design source of truth: the design pack in `docs/` (`docs/README.md` lists it and links each Claude doc).
- Technical decisions: `docs/adr/` (start with `docs/adr/README.md`); sim-core's ADRs SC-0001 to SC-0011 are inherited.
- Reece's setting decisions: ADR PL-0011 (`docs/questions.md`).
- Current task: the brief in `docs/tasks/` named in your instructions.

Precedence: on technical matters sim-core's ADRs and Plaza's ADRs override the spec. Any other conflict: stop and ask. Never resolve a conflict by guessing.

## 2. The rules that matter most

1. **The simulation is pure.** Code in `backend/plaza/sim/` imports `simcore` and its own modules only: never `plaza.db`, `plaza.api`, `plaza.llm`, `plaza.loader` or `plaza.config`; never reads the clock; never touches the network or filesystem; never uses the global `random` module or `numpy.random` functions. (TST ADR-0002, PL-0001 section 5; `tests/unit/test_sim_purity.py`)
2. **Randomness is seeded and derived.** Get a generator only from the `RngFactory` built by `plaza.sim.streams.rng_factory`, with `stream(turn, name, *key)`; one stream name per call site; new names go into `OWN_ROWS` and ADR PL-0009's table, append-only, from 20 and never in 200-299. (SC-0002, PL-0009)
3. **Money is integer cents.** Never floats. Every movement is a balanced `LedgerEntry` in one book; only the `launder` bridge crosses from the dirty book to the clean one. (SC-0004, PL-0003)
4. **One turn = one database transaction.** A crash or a killed process mid-turn leaves the save exactly as it was. (TST ADR-0004, `simcore_db.turns`)
5. **The LLM proposes, the engine disposes.** LLM output is untrusted, validated and clamped; the LLM never receives hidden true values and never writes state. (TST ADR-0005, SC-0008)
6. **The content rules (section 3) bind every file, comment, prompt and draft.** They are a test, not only a promise.

## 3. Content rules (ADR PL-0008, in full)

Applies to every document, data file, code comment, LLM prompt and LLM draft.

1. **In, at news level:** real product names and market tiers; scheduled precursors named as in public control lists, linked to products by "requires"; process families as named eras; route and laundering method categories with abstract stats; real geography; dated policy and enforcement shocks.
2. **Out:** synthesis routes, reaction steps or conditions, intermediates in sequence; real reagent or equipment lists tied to real processes; real ratios, yields or quantities (all numbers are balance-tuned fictions); concealment or laundering techniques detailed enough to work.
3. **No real people:** every organisation, member, official and agent is generated; real governments appear only as sources of dated policy events, never as named corrupt actors.
4. **Violence** is an outcome in reports and events, never a depicted scene; no torture; no harm to children.
5. **Research** uses public macro sources only (seizure statistics, market-size estimates, policy timelines), each fact tagged S, D or A.
6. **Enforcement:** a guard test lints data, prompts and comments against a maintained list of out-of-bounds terms and patterns; the LLM validator rejects drafts with procedural detail, graphic violence or real names; every event keeps an offline template; a reviewer checks each data file at its milestone.

The guard is `tools/content_rules/` (its term list `terms.yaml` is reviewed by Reece at each merge), run by `backend/tests/test_content_rules.py` in `make check`. Never weaken a rule or add an allow marker to get a test green: rewrite the text. If a rule is wrong, say so and ask.

## 4. Upstream repositories are read-only

Plaza depends on `sim-core` (`Reece77/Sim-core`) **by tag only** (ADR PL-0001; `backend/pyproject.toml`; `tests/unit/test_core_pin.py` fails on any other pin). Tech Startup Tycoon (`Reece77/Tech_Executive_Tycoon`), Partner Track (`Reece77/LawGame`) and sim-core are **read-only**: clone them into a separate folder to read; never commit, push, open pull requests or run workflows there. A bug in sim-core is reported to Reece for a sim-core session; do not work around it here. Upgrading sim-core is its own sub-task in the milestone that needs the new version.

Files ported from TST or PT (front-end components, tooling) carry a header naming their upstream path and commit and what changed. The UI shell under `frontend/src/core/` is sim-core's `ui/` unchanged, checked against its pinned `MANIFEST.json` (`tools/check_ui.py`).

## 5. Scope discipline

- Build only what the current brief lists; put better ideas under "Follow-ups".
- No systems from a later milestone, not even as stubs (the turn's no-op phases are the exception, by design).
- Dependencies: TST ADR-0001's list plus `simcore`. Ask before adding any package.
- Do not reformat or refactor files unrelated to the task. Never edit a copied design-pack file (`tests/unit/test_design_pack.py`).

## 6. Repository map

```text
CLAUDE.md  AGENTS.md  README.md  CHANGELOG.md  Makefile  ruff.toml  .pre-commit-config.yaml
Plaza.cmd  "Make desktop shortcut.cmd"   the launcher (tools/launcher.py)
docs/        README (the design pack), roadmap, reuse map, spec, questions, research/, adr/, tasks/, data dictionary
backend/
  plaza/     sim/ (PURE: streams, books, state, turn, setup, interfaces), db/, api/, llm/,
             data/ (seed YAML), loader.py, cli.py, config.py
  migrations/ Plaza's own Alembic chain
  scripts/   export_openapi.py
  tests/     unit/ property/ integration/ golden/ fixtures/, test_content_rules.py
frontend/    src/core/ (sim-core's UI shell, hash-checked), src/api/ (GENERATED: never hand-edit), e2e/
tools/       content_rules/, check_ui.py, launcher.py, dev.py
```

## 7. Commands

```bash
cd backend && uv sync && uv run pytest -q -n auto        # tests
uv run plaza new-game --name dev --seed 42               # a save in saves/
uv run plaza advance --save dev --turns 360
uv run plaza inspect --save dev
uv run pytest tests/golden --update-golden               # regenerate golden files (reason in CHANGELOG.md)
uv run pytest tests/unit/test_state_cache.py --update-state-cache   # re-record the state cache (same rule)
cd frontend && pnpm install && pnpm gen:api && pnpm dev
make check     # backend lint, types, tests, content rules, API sync, UI shell, frontend. Must pass.
make e2e       # Playwright smoke tests (set PLAYWRIGHT_CHROMIUM_PATH in cloud sessions)
make dev       # API and front end together
```

Each session works in its **own clone or worktree**; never share a folder with another session.

## 8. Definition of done (every task)

- [ ] Every acceptance criterion in the brief is met, and you state how each was verified.
- [ ] `make check` and `make e2e` pass, and CI's `check`, `e2e` and `determinism` are green on the pushed branch.
- [ ] New engine logic has unit tests; randomness has a seeded test; invariants have Hypothesis property tests.
- [ ] Golden snapshots and the state cache unchanged, or regenerated with the reason in `CHANGELOG.md`.
- [ ] Schema changes have an Alembic migration and `docs/data-dictionary.md` is updated.
- [ ] Tunable numbers live in `backend/plaza/data/balance.yaml` with a comment (unit and intent).
- [ ] The content-rules guard passes; any new term or pattern is listed for Reece's review.
- [ ] Decisions the spec and ADRs did not cover are written down (an ADR or the brief's "Decisions made").
- [ ] Final message: summary, files touched, how each criterion was verified, follow-ups.

### Merging

`main` changes arrive through pull requests whose `check`, `e2e` and `determinism` runs are green on a branch up to date with `main`. Merge with a **merge commit** whose message ends with `Milestone-Tag: pl-mX-done`; the `tag-milestone` workflow tags it (cloud sessions cannot push tags). Never force-push or rewrite `main`. Commit as `Claude <noreply@anthropic.com>`. Only the session a brief names merges that milestone.

## 9. Conventions

- Python 3.12, full type hints, `mypy --strict` for `plaza/sim`. Sim models are `@dataclass(frozen=True, slots=True)`; return new objects; tuples sorted by id.
- IDs are `int`. Turn 0 is the scenario's start month (January 2006); convert only with `simcore.kernel.calendar`, always passing the save's `start_ym` (`tests/unit/test_calendar.py` fails on a call without it).
- State is a sim-core `CoreState` with registered sub-states (`plaza/sim/state.py`); phases register into sim-core's twelve slots (`plaza/sim/turn.py`).
- Attributes are floats in [1.0, 20.0], shown as integers; clamp on every write.
- Hidden values (informant risk, true odds) are `hidden_field()`s; the API and prompts see views only. (SC-0008)
- No `print` in library code. Domain errors live in `plaza.sim.errors` and subclass sim-core's.
- Front end: strict TypeScript, TanStack Query and Table, Mantine, dark theme; no game logic; money arrives as integer cents and is shown with `formatMoney()`.
- Seed and balance data are YAML validated by Pydantic through sim-core's `DataRegistry`; invalid data fails at startup.

## 10. Never

- Never write anything the content rules put out of bounds, in any file, comment, prompt or test.
- Never expose hidden true values through the API or a prompt.
- Never call the Anthropic API in tests; use `MockLLMAdapter`.
- Never commit secrets (`ANTHROPIC_API_KEY` comes from `.env`).
- Never edit an applied migration or delete golden snapshots to make tests pass; never weaken a test.
- Never write to Tech Startup Tycoon's, Partner Track's or sim-core's repository; never pin sim-core to anything but a tag.

## 11. When unsure

Ask one short, specific question with your proposed default. Engineering details you may decide and note in your summary. Partner Track's balance, seed and lane rules (its CLAUDE.md section 12) apply here by analogy once Plaza has balance targets (PL-M10).
