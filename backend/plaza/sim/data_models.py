"""Pydantic schemas for Plaza's seed and balance data (TST ADR-0008; SC-0006's DataRegistry).

`plaza.loader` reads the YAML files in `backend/plaza/data/`; `DATA` validates each section
here, and invalid data fails at start-up. Money is integer cents; rates are basis points.
"""

from __future__ import annotations

from typing import Final, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from simcore.data import DataRegistry, DataSet

type AccountType = Literal["asset", "liability", "equity", "income", "cost"]
type BookCode = Literal["dirty", "clean"]

# ADR PL-0003 section 6: an account belongs to its book by its code's first letter.
BOOK_PREFIX: Final[dict[str, str]] = {"dirty": "D", "clean": "C"}
MONTHS_PER_YEAR: Final = 12  # tunable-exempt: the calendar


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


# --- accounts.yaml -------------------------------------------------------------------------


class Account(_Strict):
    code: str
    name: str
    type: AccountType
    book: BookCode

    @model_validator(mode="after")
    def _code_matches_book(self) -> Account:
        if not self.code.startswith(BOOK_PREFIX[self.book]):
            raise ValueError(
                f"account {self.code}: {self.book}-book codes start with {BOOK_PREFIX[self.book]}"
            )
        return self


class Accounts(_Strict):
    accounts: tuple[Account, ...]

    @model_validator(mode="after")
    def _unique(self) -> Accounts:
        codes = [a.code for a in self.accounts]
        if len(codes) != len(set(codes)):
            raise ValueError("duplicate account codes")
        return self

    def by_code(self) -> dict[str, Account]:
        return {a.code: a for a in self.accounts}


# --- scenarios.yaml ------------------------------------------------------------------------


class Scenario(_Strict):
    id: str
    name: str
    description: str
    start_ym: tuple[int, int]  # ADR PL-0002 section 1: turn 0 is data
    campaign_turns: int = Field(gt=0)  # months played from turn 0

    @field_validator("start_ym")
    @classmethod
    def _month(cls, value: tuple[int, int]) -> tuple[int, int]:
        if not 1 <= value[1] <= MONTHS_PER_YEAR:
            raise ValueError("start month must be 1..12")
        return value


class Difficulty(_Strict):
    id: str
    name: str
    description: str


class Background(_Strict):
    id: str
    name: str
    lean: str  # the starting lean shown to the player (spec 2.1); mechanics from PL-M1a


class Scenarios(_Strict):
    scenarios: tuple[Scenario, ...]
    difficulties: tuple[Difficulty, ...]
    backgrounds: tuple[Background, ...]
    default_scenario: str
    default_difficulty: str

    @model_validator(mode="after")
    def _consistent(self) -> Scenarios:
        for label, keys in (
            ("scenario", [s.id for s in self.scenarios]),
            ("difficulty", [d.id for d in self.difficulties]),
            ("background", [b.id for b in self.backgrounds]),
        ):
            if len(keys) != len(set(keys)):
                raise ValueError(f"duplicate {label} ids")
        if self.scenario(self.default_scenario) is None:
            raise ValueError(f"default scenario {self.default_scenario!r} is not listed")
        if self.difficulty(self.default_difficulty) is None:
            raise ValueError(f"default difficulty {self.default_difficulty!r} is not listed")
        return self

    def scenario(self, scenario_id: str) -> Scenario | None:
        return next((s for s in self.scenarios if s.id == scenario_id), None)

    def difficulty(self, difficulty_id: str) -> Difficulty | None:
        return next((d for d in self.difficulties if d.id == difficulty_id), None)

    def background(self, background_id: str) -> Background | None:
        return next((b for b in self.backgrounds if b.id == background_id), None)


# --- balance.yaml --------------------------------------------------------------------------


class StartBalance(_Strict):
    dirty_stake_cents: int = Field(gt=0)


class LaunderingBalance(_Strict):
    fee_bp: int = Field(ge=0, le=10_000)
    leakage_bp: int = Field(ge=0, le=10_000)


class BackupBalance(_Strict):
    every_turns: int = Field(gt=0)
    keep_periodic: int = Field(gt=0)


class Balance(_Strict):
    start: StartBalance
    laundering: LaunderingBalance
    backups: BackupBalance


# --- the registry --------------------------------------------------------------------------

SECTIONS: Final = (("accounts", Accounts), ("balance", Balance), ("scenarios", Scenarios))


def registry() -> DataRegistry:
    reg = DataRegistry()
    for name, model in SECTIONS:
        reg.register(name, model)
    return reg


class GameData:
    """The validated data a game runs on: typed access to each section."""

    __slots__ = ("_set",)

    def __init__(self, data: DataSet) -> None:
        self._set = data

    @property
    def accounts(self) -> Accounts:
        return self._set.section("accounts", Accounts)

    @property
    def balance(self) -> Balance:
        return self._set.section("balance", Balance)

    @property
    def scenarios(self) -> Scenarios:
        return self._set.section("scenarios", Scenarios)
