"""The headless CLI: `plaza new-game`, `advance --turns 360`, `inspect`."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from plaza.cli import app


def test_new_game_advance_360_turns_and_inspect(save_dir: Path) -> None:
    runner = CliRunner()
    made = runner.invoke(
        app, ["new-game", "--name", "cli", "--seed", "42", "--background", "producer"]
    )
    assert made.exit_code == 0, made.output
    assert "Jan 2006" in made.output
    played = runner.invoke(app, ["advance", "--save", "cli", "--turns", "360"])
    assert played.exit_code == 0, played.output
    assert "360 turn(s) played; Dec 2035 (campaign_complete)" in played.output
    shown = runner.invoke(app, ["inspect", "--save", "cli"])
    assert "Dirty cash: $100,000.00" in shown.output and "campaign_complete" in shown.output
    again = runner.invoke(app, ["advance", "--save", "cli", "--turns", "1"])
    assert "0 turn(s) played" in again.output
    listed = runner.invoke(app, ["saves"])
    assert "cli\t" in listed.output
