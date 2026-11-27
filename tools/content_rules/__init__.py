"""The content-rules guard (ADR PL-0008 section 6): lints data, documents, LLM prompt
templates and code comments against `terms.yaml`. Run by backend/tests/test_content_rules.py
in `make check`; `python tools/content_rules/lint.py` prints every finding."""
