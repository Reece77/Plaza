"""Plaza's LLM seam on `simcore_llm` (TST ADR-0005; SC-0009). The LLM proposes, the engine
disposes: an adapter turns a prompt built from public facts into words, never sees state and
never writes it. No text is generated at PL-M0; PL-M8 adds the first caller."""
