"""FastAPI app. OpenAPI is the contract; the front end's client is generated from it
(`pnpm gen:api`, checked by `make check-api`). Adapted from Partner Track's `ptk/api/app.py`
at PT-M0. Responses carry only public values (SC-0008): at PL-M0 there are no hidden ones.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from simcore.kernel.calendar import format_turn
from simcore.kernel.errors import SimError
from simcore_db.turns import SaveBusyError
from simcore_llm.settings import month_spend, reset_date, save_settings

from plaza import loader
from plaza.config import get_settings
from plaza.db import saves
from plaza.llm.kinds import llm_settings
from plaza.sim.books import CLEAN_CASH, DIRTY_CASH, cash
from plaza.sim.errors import (
    GameOverError,
    InvalidSaveNameError,
    SaveExistsError,
    SaveNotFoundError,
    UnknownBackgroundError,
    UnknownDifficultyError,
    UnknownKpiError,
    UnknownScenarioError,
)
from plaza.sim.interfaces import CLEAN_CASH_KPI, DIRTY_CASH_KPI
from plaza.sim.state import Organisation, SaveInfo, last_turn

_STATUS: dict[type[SimError], int] = {
    SaveNotFoundError: 404,
    UnknownKpiError: 404,
    SaveExistsError: 409,
    GameOverError: 409,
    SaveBusyError: 409,
    InvalidSaveNameError: 400,
    UnknownScenarioError: 400,
    UnknownDifficultyError: 400,
    UnknownBackgroundError: 400,
}
_KPI_ACCOUNTS = {DIRTY_CASH_KPI: DIRTY_CASH, CLEAN_CASH_KPI: CLEAN_CASH}


class ErrorBody(BaseModel):
    code: str
    message: str


class OptionOut(BaseModel):
    id: str
    name: str
    description: str


class MetaOut(BaseModel):
    scenarios: list[OptionOut]
    difficulties: list[OptionOut]
    backgrounds: list[OptionOut]
    default_scenario: str
    default_difficulty: str


class SaveOut(BaseModel):
    slug: str
    name: str
    org_name: str
    leader_name: str
    turn: int
    date_label: str
    status: str


class NewGameIn(BaseModel):
    slug: str = Field(min_length=1, max_length=63)
    org_name: str = Field(min_length=1, max_length=120)
    leader_name: str = Field(min_length=1, max_length=120)
    background: str
    difficulty: str | None = None
    scenario_id: str | None = None
    ironman: bool = False
    seed: int | None = Field(default=None, ge=0, le=2**64 - 1)


class StateOut(BaseModel):
    slug: str
    org_name: str
    leader_name: str
    background: str
    difficulty: str
    ironman: bool
    turn: int
    date_label: str
    last_turn: int
    last_date_label: str
    dirty_cash_cents: int
    clean_cash_cents: int
    status: Literal["active", "campaign_complete"]


class ExplainLineOut(BaseModel):
    turn: int
    date_label: str
    book: str
    memo: str
    amount_cents: int


class ExplainOut(BaseModel):
    kpi: str
    account: str
    total_cents: int
    lines: list[ExplainLineOut]


class LlmSettingsOut(BaseModel):
    adapter: Literal["claude", "templates", "mock"]
    has_key: bool
    monthly_budget_cents: int
    spent_cents: float
    calls: int
    resets_on: str


class LlmSettingsIn(BaseModel):
    adapter: Literal["claude", "templates"]
    monthly_budget_cents: int = Field(ge=0, le=1_000_000)


def _state(slug: str) -> StateOut:
    path = saves.open_save(get_settings().resolved_save_dir(), slug)
    state, balances = saves.read_state(path)
    org, info = state.sub(Organisation), state.sub(SaveInfo)
    start = state.meta.start_ym
    dirty, clean = cash(balances, org.id)
    status = state.meta.status
    return StateOut(
        slug=slug,
        org_name=org.name,
        leader_name=org.leader_name,
        background=org.background,
        difficulty=info.difficulty,
        ironman=info.ironman,
        turn=state.turn,
        date_label=format_turn(state.turn, start),
        last_turn=last_turn(state),
        last_date_label=format_turn(last_turn(state), start),
        dirty_cash_cents=dirty,
        clean_cash_cents=clean,
        status="campaign_complete" if status == "campaign_complete" else "active",
    )


def _llm() -> LlmSettingsOut:
    settings = get_settings()
    folder = settings.resolved_save_dir()
    chosen = llm_settings(folder)
    spend = month_spend(folder)
    return LlmSettingsOut(
        adapter=chosen.adapter,
        has_key=bool(settings.anthropic_api_key),
        monthly_budget_cents=chosen.monthly_budget_cents,
        spent_cents=spend.cents,
        calls=spend.calls,
        resets_on=reset_date(),
    )


def create_app() -> FastAPI:
    app = FastAPI(title="Plaza", version="0.1.0")

    @app.exception_handler(SimError)
    async def _sim_error(_request: Request, exc: SimError) -> JSONResponse:
        status = next((s for cls, s in _STATUS.items() if isinstance(exc, cls)), 400)
        return JSONResponse(status_code=status, content={"code": exc.code, "message": exc.message})

    errors: dict[int | str, dict[str, Any]] = {
        400: {"model": ErrorBody},
        404: {"model": ErrorBody},
        409: {"model": ErrorBody},
    }

    @app.get("/api/meta", response_model=MetaOut, operation_id="getMeta")
    def get_meta() -> MetaOut:
        s = loader.game_data().scenarios
        return MetaOut(
            scenarios=[
                OptionOut(id=x.id, name=x.name, description=x.description) for x in s.scenarios
            ],
            difficulties=[
                OptionOut(id=x.id, name=x.name, description=x.description) for x in s.difficulties
            ],
            backgrounds=[
                OptionOut(id=x.id, name=x.name, description=x.lean) for x in s.backgrounds
            ],
            default_scenario=s.default_scenario,
            default_difficulty=s.default_difficulty,
        )

    @app.get("/api/saves", response_model=list[SaveOut], operation_id="listSaves")
    def list_saves() -> list[SaveOut]:
        return [
            SaveOut(
                slug=s.slug,
                name=s.name,
                org_name=s.org_name,
                leader_name=s.leader_name,
                turn=s.turn,
                date_label=s.date_label,
                status=s.status,
            )
            for s in saves.list_saves(get_settings().resolved_save_dir())
        ]

    @app.post("/api/saves", response_model=StateOut, responses=errors, operation_id="newGame")
    def new_game(body: NewGameIn) -> StateOut:
        saves.create_save(
            get_settings().resolved_save_dir(),
            body.slug,
            org_name=body.org_name,
            leader_name=body.leader_name,
            background=body.background,
            scenario_id=body.scenario_id,
            difficulty=body.difficulty,
            ironman=body.ironman,
            data=loader.game_data(),
            seed=body.seed,
        )
        return _state(body.slug)

    @app.get(
        "/api/saves/{slug}/state",
        response_model=StateOut,
        responses=errors,
        operation_id="getState",
    )
    def get_state(slug: str) -> StateOut:
        return _state(slug)

    @app.post(
        "/api/saves/{slug}/advance",
        response_model=StateOut,
        responses=errors,
        operation_id="advance",
    )
    def advance(slug: str) -> StateOut:
        path = saves.open_save(get_settings().resolved_save_dir(), slug)
        saves.run_turn(path, loader.game_data())
        return _state(slug)

    @app.get(
        "/api/saves/{slug}/explain/{kpi}",
        response_model=ExplainOut,
        responses=errors,
        operation_id="explainKpi",
    )
    def explain(slug: str, kpi: str) -> ExplainOut:
        """The breakdown of a cash KPI: every posted line on its account."""
        account = _KPI_ACCOUNTS.get(kpi)
        if account is None:
            raise UnknownKpiError(f"no breakdown for {kpi!r}")
        path = saves.open_save(get_settings().resolved_save_dir(), slug)
        state, _ = saves.read_state(path)
        lines = saves.account_lines(path, account)
        return ExplainOut(
            kpi=kpi,
            account=account,
            total_cents=sum(ln.amount_cents for ln in lines),
            lines=[
                ExplainLineOut(
                    turn=ln.turn,
                    date_label=format_turn(ln.turn, state.meta.start_ym),
                    book=ln.book,
                    memo=ln.memo,
                    amount_cents=ln.amount_cents,
                )
                for ln in lines
            ],
        )

    @app.get("/api/settings/llm", response_model=LlmSettingsOut, operation_id="getLlmSettings")
    def get_llm() -> LlmSettingsOut:
        return _llm()

    @app.put("/api/settings/llm", response_model=LlmSettingsOut, operation_id="putLlmSettings")
    def put_llm(body: LlmSettingsIn) -> LlmSettingsOut:
        folder = get_settings().resolved_save_dir()
        current = llm_settings(folder)
        save_settings(
            folder,
            current.model_copy(
                update={"adapter": body.adapter, "monthly_budget_cents": body.monthly_budget_cents}
            ),
        )
        return _llm()

    frontend = get_settings().frontend_dir
    if frontend is not None and (frontend / "index.html").is_file():
        _serve_frontend(app, frontend)
    return app


def _serve_frontend(app: FastAPI, folder: Path) -> None:
    """The built front end on the API's own port (the launcher's single server)."""
    app.mount("/assets", StaticFiles(directory=folder / "assets"), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    def spa(path: str) -> FileResponse:
        target = (folder / path).resolve()
        if path and target.is_file() and folder.resolve() in target.parents:
            return FileResponse(target)
        return FileResponse(folder / "index.html")


app = create_app()
