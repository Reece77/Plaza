"""Headless commands: new-game, advance, inspect, saves (adapted from Partner Track's CLI)."""

from __future__ import annotations

import typer
from simcore.kernel.calendar import format_turn
from simcore.kernel.money import format_money

from plaza import loader
from plaza.config import get_settings
from plaza.db import saves
from plaza.sim.books import cash
from plaza.sim.state import Organisation, SaveInfo, is_active

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command("new-game")
def new_game_cmd(
    name: str = typer.Option(..., help="Save name (lower-case letters, digits, hyphens)"),
    org: str = typer.Option("The Organisation", help="The organisation's name"),
    leader: str = typer.Option("The Leader", help="The leader's name"),
    background: str = typer.Option("smuggler", help="smuggler, producer, enforcer, ..."),
    difficulty: str | None = typer.Option(None, help="lieutenant, boss or kingpin"),
    ironman: bool = typer.Option(False, help="One save; capture or death is final"),
    seed: int | None = typer.Option(None, help="Master seed; random if omitted"),
) -> None:
    state = saves.create_save(
        get_settings().resolved_save_dir(),
        name,
        org_name=org,
        leader_name=leader,
        background=background,
        difficulty=difficulty,
        ironman=ironman,
        data=loader.game_data(),
        seed=seed,
    )
    typer.echo(f"Created {name}: {org}, {format_turn(state.turn, state.meta.start_ym)}")


@app.command()
def advance(save: str = typer.Option(...), turns: int = typer.Option(1, min=1)) -> None:
    path = saves.open_save(get_settings().resolved_save_dir(), save)
    played = 0
    for _ in range(turns):
        state, _ = saves.read_state(path)
        if not is_active(state):
            break
        saves.run_turn(path, loader.game_data())
        played += 1
    state, _ = saves.read_state(path)
    shown = state.turn - 1 if not is_active(state) else state.turn
    typer.echo(
        f"{save}: {played} turn(s) played; {format_turn(shown, state.meta.start_ym)}"
        f" ({state.meta.status})"
    )


@app.command()
def inspect(save: str = typer.Option(...)) -> None:
    path = saves.open_save(get_settings().resolved_save_dir(), save)
    state, balances = saves.read_state(path)
    org, info = state.sub(Organisation), state.sub(SaveInfo)
    dirty, clean = cash(balances, org.id)
    typer.echo(f"{org.name}, led by {org.leader_name} ({org.background}, {info.difficulty})")
    shown = state.turn if is_active(state) else (info.ended_turn or state.turn)
    typer.echo(f"Date: {format_turn(shown, state.meta.start_ym)} (turn {shown})")
    typer.echo(f"Dirty cash: {format_money(dirty)}")
    typer.echo(f"Clean cash: {format_money(clean)}")
    typer.echo(f"Status: {state.meta.status}")


@app.command("saves")
def list_cmd() -> None:
    for s in saves.list_saves(get_settings().resolved_save_dir()):
        typer.echo(f"{s.slug}\t{s.org_name}\t{s.date_label}\t{s.status}")


if __name__ == "__main__":
    app()
