# Root tasks (adapted from Partner Track's Makefile). Recipes avoid shell-specific syntax so
# they run under sh and cmd.exe.

.PHONY: check check-fast check-backend check-lint check-api check-ui check-frontend golden golden-twice nightly e2e dev gen-api

check: check-backend check-api check-ui check-frontend

# Lint, format, types and every test except the nightly ones. The content-rules guard
# (backend/tests/test_content_rules.py) and the tag-pin test (tests/unit/test_core_pin.py) run here.
check-backend: check-lint
	cd backend && uv run pytest -q -n auto -m "not nightly"

check-lint:
	cd backend && uv run ruff check .. && uv run ruff format --check .. && uv run mypy

# For local iteration only: the same without the golden seeds.
check-fast: check-lint
	cd backend && uv run pytest -q -n auto -m "not nightly" --ignore=tests/golden

# The generated client must match the API (TST ADR-0009).
check-api:
	cd frontend && pnpm gen:api && git diff --exit-code -- src/api

# The UI shell under frontend/src/core is sim-core's ui/ at the pinned tag, unchanged.
check-ui:
	uv run --project backend python tools/check_ui.py

check-frontend:
	cd frontend && pnpm lint && pnpm typecheck && pnpm test

golden:
	cd backend && uv run pytest tests/golden -q --update-golden

# Same seed, same results on two processes (the determinism job): each run is its own
# Python process compared with the recorded snapshots and state cache.
golden-twice:
	cd backend && uv run pytest tests/golden tests/unit/test_state_cache.py -q
	cd backend && uv run pytest tests/golden tests/unit/test_state_cache.py -q

# The long runs (CI: nightly.yml; dispatch it on a branch for long runs).
nightly:
	cd backend && uv run pytest -q -n auto -m nightly

gen-api:
	cd frontend && pnpm gen:api

e2e:
	cd frontend && pnpm exec playwright test

dev:
	cd backend && uv run python ../tools/dev.py
