"""The API: new game, advance, state, saves, Explain and the LLM settings (TestClient)."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from plaza.api.app import create_app
from plaza.sim.data_models import GameData

NEW = {"slug": "api", "org_name": "Org", "leader_name": "Leader", "background": "fixer", "seed": 5}


def test_new_game_advance_state_and_saves(save_dir: Path, data: GameData) -> None:
    client = TestClient(create_app())
    meta = client.get("/api/meta").json()
    assert [d["id"] for d in meta["difficulties"]] == ["lieutenant", "boss", "kingpin"]
    assert len(meta["backgrounds"]) == 5 and meta["default_difficulty"] == "boss"
    created = client.post("/api/saves", json=NEW)
    assert created.status_code == 200, created.text
    body = created.json()
    assert body["date_label"] == "Jan 2006" and body["last_date_label"] == "Dec 2035"
    assert body["dirty_cash_cents"] == data.balance.start.dirty_stake_cents
    assert body["clean_cash_cents"] == 0 and body["ironman"] is False
    assert body["difficulty"] == "boss"
    after = client.post("/api/saves/api/advance").json()
    assert after["turn"] == 1 and after["date_label"] == "Feb 2006"
    assert client.get("/api/saves/api/state").json() == after
    (summary,) = client.get("/api/saves").json()
    assert summary["slug"] == "api" and summary["org_name"] == "Org"


def test_explain_breaks_a_cash_kpi_into_lines(save_dir: Path, data: GameData) -> None:
    client = TestClient(create_app())
    client.post("/api/saves", json=NEW)
    explain = client.get("/api/saves/api/explain/dirty_cash_cents").json()
    assert explain["total_cents"] == data.balance.start.dirty_stake_cents
    assert [ln["memo"] for ln in explain["lines"]] == ["Starting stake"]
    assert client.get("/api/saves/api/explain/clean_cash_cents").json()["lines"] == []
    assert client.get("/api/saves/api/explain/heat").status_code == 404


def test_errors_map_to_statuses(save_dir: Path) -> None:
    client = TestClient(create_app())
    assert client.get("/api/saves/nope/state").status_code == 404
    assert client.post("/api/saves", json={**NEW, "slug": "Bad Name"}).status_code == 400
    assert client.post("/api/saves", json={**NEW, "background": "astronaut"}).status_code == 400
    client.post("/api/saves", json=NEW)
    clash = client.post("/api/saves", json=NEW)
    assert clash.status_code == 409 and clash.json()["code"] == "save_exists"


def test_llm_settings_default_to_templates_and_save(save_dir: Path) -> None:
    client = TestClient(create_app())
    first = client.get("/api/settings/llm").json()
    assert first["adapter"] == "templates" and first["has_key"] is False
    assert first["spent_cents"] == 0 and first["monthly_budget_cents"] == 1000
    saved = client.put(
        "/api/settings/llm", json={"adapter": "claude", "monthly_budget_cents": 500}
    ).json()
    assert saved["adapter"] == "claude" and saved["monthly_budget_cents"] == 500
