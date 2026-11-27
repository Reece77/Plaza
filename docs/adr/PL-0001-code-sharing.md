## PL-0001: Code sharing — depend on `sim-core`, transplant only as a fallback

- Inherits: PT-0001 (selective transplant, clean kernel boundary, extraction checkpoint)
- Inputs: the accepted reuse map; roadmap decision 1

**Context.** PT-0001's extraction checkpoint is met (TST v5 closed 2026-11-21; PT-M7 merged). PT-M19 writes the extraction plan. A third game copying the kernel again would make three drifting copies.

**Decision.**

1. Plaza depends on `sim-core` by tag. **Amended 2026-11-27 (Reece):** PL-M0 starts on `sim-core` **v0.1.0** (kernel, stream registry, multi-book ledger, composable state, phase registry, interfaces, cases, governing bodies, persistence, LLM, guard suites, UI shell). **PL-M1a** waits for **v0.2**, which brings people, hiring and org from Partner Track (SC-2). Each later Plaza milestone names the core version it needs; an upgrade is its own sub-task with snapshots re-recorded.
2. Plaza's five asks (reuse map §8) go into PT-M19's plan: phase registry and composable sub-states; multi-book ledger; generic case machinery; governing-body abstraction; interfaces tested against heat and territory.
3. **Fallback:** if the plan costs more than two milestones, Plaza transplants from **Partner Track first, TST second**, with provenance and PT's `check_vendored.py`. *Not triggered: the accepted `sim-core` plan (2026-11-26) costs two milestones on Plaza's route. It applies again only if SC-2 slips past one milestone after its cut line (plan risk 10).*
4. Plaza never edits TST or PT. Core bugs are reported to Reece for a session in the owning repository.
5. Plaza has no kernel of its own (amended 2026-11-27): `plaza/sim` imports `simcore` and its own packages only, never `plaza.db`, `plaza.api`, `plaza.llm` or I/O, checked by `simcore_testing`'s purity suite. Plaza's domain packages meet only through `plaza/sim/interfaces.py`, which implements `simcore.interfaces`. `sim-core` is a public repository (Reece, 2026-11-27), so no access token is needed.

**Consequences.** PL-D0 and early design run in parallel with PT-M19; code waits on the core. One fix in the core reaches three games.

