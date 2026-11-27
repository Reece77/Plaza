# Architecture Decision Records

Each ADR records one decision agents must not re-decide. To change one, write a new ADR that supersedes it; never edit an accepted ADR's decision.

The PL ADRs are the design pack's "Plaza ADRs PL-0001 to PL-0008 v0.1" document (Claude doc, linked from `docs/README.md`), split one section per file as its status line says, each section's text unchanged. The pack's preamble and its closing "Ideas to expand" are kept verbatim below; joined in the order of the table (preamble, PL-0001 to PL-0008, PL-0011, PL-0009, PL-0010, ideas) the files reproduce the exported document byte for byte (sha256 `9529bdcc2f4c8b27e7e5837a482d14abb8f676fe05528eaa68455aba69535c69`, 16,896 bytes, exported 2026-11-27).

| ADR | Subject | Status |
| --- | --- | --- |
| [PL-0001](PL-0001-code-sharing.md) | Code sharing: depend on `sim-core` by tag (v0.1.0 for PL-M0) | Accepted, amended 2026-11-27 |
| [PL-0002](PL-0002-time-model.md) | January 2006 start, monthly turns, the December cycle, phase order | Accepted |
| [PL-0003](PL-0003-two-book-ledger.md) | The two-book ledger: dirty and clean, laundering the only crossing | Accepted |
| [PL-0004](PL-0004-territory.md) | Territory: plazas on a map | Accepted |
| [PL-0005](PL-0005-heat.md) | Heat at four levels, slow decay | Accepted |
| [PL-0006](PL-0006-law-enforcement-adversary.md) | Law enforcement as an adversary | Accepted |
| [PL-0007](PL-0007-council-and-succession.md) | The council and succession | Accepted |
| [PL-0008](PL-0008-content-rules.md) | Content rules, enforced by a guard test | Accepted |
| [PL-0011](PL-0011-setting-decisions.md) | Setting decisions (questions 1-20) | Accepted |
| [PL-0009](PL-0009-rng-streams.md) | Plaza's stream table, 20-36 | Accepted |
| [PL-0010](PL-0010-conflict-resolution.md) | Conflict resolved abstractly, month by month | Accepted |

## Inherited

sim-core's ADRs SC-0001 to SC-0011 and the TST and PT ADRs they inherit (listed in sim-core's `docs/adr/README.md` at tag `v0.1.0`) apply to Plaza as written. On technical matters they and Plaza's ADRs override the spec.

## The pack's preamble (verbatim)

# Plaza ADRs PL-0001 to PL-0008 v0.1

Nov 26, 2026 · @Reece DeHaan

**Status: all eight ACCEPTED by Reece (2026-11-26).** Second deliverable of PL-D0; each section becomes one file in `docs/adr/`. Format follows Partner Track's ADRs. "TST" is Tech Startup Tycoon; "PT" is Partner Track.

## The pack's closing section (verbatim)

## Ideas to expand

- PL-0009 RNG streams: reserve Plaza's id range now, before any code, as PT-0012 did.
- PL-0010 conflict resolution: the formula for wars and alliances deserves its own ADR before PL-M7.
- A threat-model note for PL-0008: list the ways an LLM draft could drift and the validator test for each.
