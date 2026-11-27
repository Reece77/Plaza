"""Plaza's pure simulation (ADR PL-0001 section 5).

`plaza.sim` imports `simcore` and its own modules only: never `plaza.db`, `plaza.api`,
`plaza.llm`, the clock, the filesystem or the global random module (guarded by
tests/unit/test_sim_purity.py through `simcore_testing.purity`).
"""
