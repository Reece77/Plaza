# Changelog

Golden snapshots and the state cache are regenerated only with a line here saying why.

## PL-M0 follow-up (2026-11-28)

- Content rules: the `lab-quantity` rule is removed at Reece's review of `terms.yaml`. Quantities are game numbers (balance-tuned fictions); the milestone reviewer still checks data files for real figures. The news-level fixture now carries quantities to keep them passing.

## PL-M0 (foundation)

- New repository on sim-core v0.1.0: the design pack copied into `docs/`, the content-rules guard, Plaza's stream table (20-36), the January 2006 calendar, the dirty and clean books with the laundering bridge, the twelve-phase turn, persistence (schema v1), the API and CLI, the LLM seam, the front-end shell and the launcher.
- Golden snapshots for seeds 1-3 (360 empty turns) and the state cache recorded for the first time.
