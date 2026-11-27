"""Plaza's domain errors. Each subclasses a `simcore.kernel.errors` error and keeps a stable
`code` the API maps to an HTTP status."""

from __future__ import annotations

from simcore.kernel.errors import InvalidDataError, NotFoundError, SimError


class SaveNotFoundError(NotFoundError):
    code = "save_not_found"


class SaveExistsError(SimError):
    code = "save_exists"


class InvalidSaveNameError(SimError):
    code = "invalid_save_name"


class GameOverError(SimError):
    """The campaign has ended; no further turn can be played."""

    code = "game_over"


class UnknownScenarioError(InvalidDataError):
    code = "unknown_scenario"


class UnknownDifficultyError(InvalidDataError):
    code = "unknown_difficulty"


class UnknownBackgroundError(InvalidDataError):
    code = "unknown_background"


class UnknownKpiError(NotFoundError):
    code = "unknown_kpi"
