"""Schema v1 (PL-M0): save meta, organisation, the two-book ledger, snapshots, turn log.

Revision ID: 0001_initial
Revises:
Create Date: 2026-11-27
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "save_meta",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("game", sa.String(20), nullable=False),
        sa.Column("master_seed", sa.BigInteger, nullable=False),
        sa.Column("start_year", sa.Integer, nullable=False),
        sa.Column("start_month", sa.Integer, nullable=False),
        sa.Column("start_turn", sa.Integer, nullable=False),
        sa.Column("current_turn", sa.Integer, nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("scenario_id", sa.String(40), nullable=False),
        sa.Column("difficulty", sa.String(20), nullable=False),
        sa.Column("ironman", sa.Boolean, nullable=False),
        sa.Column("campaign_turns", sa.Integer, nullable=False),
        sa.Column("ended_turn", sa.Integer, nullable=True),
    )
    op.create_table(
        "organisation",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("leader_name", sa.String(120), nullable=False),
        sa.Column("background", sa.String(40), nullable=False),
        sa.Column("is_player", sa.Boolean, nullable=False),
    )
    op.create_table(
        "ledger_entry",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("turn", sa.Integer, nullable=False, index=True),
        sa.Column(
            "entity_id", sa.Integer, sa.ForeignKey("organisation.id"), nullable=False, index=True
        ),
        sa.Column("book", sa.String(20), nullable=False, index=True),
        sa.Column("memo", sa.Text, nullable=False),
        sa.Column("link", sa.String(80), nullable=True),
    )
    op.create_table(
        "ledger_line",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "entry_id", sa.Integer, sa.ForeignKey("ledger_entry.id"), nullable=False, index=True
        ),
        sa.Column("account", sa.String(40), nullable=False, index=True),
        sa.Column("amount_cents", sa.BigInteger, nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("dims_json", sa.Text, nullable=False),
    )
    op.create_table(
        "turn_snapshot",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("turn", sa.Integer, nullable=False, index=True),
        sa.Column(
            "entity_id", sa.Integer, sa.ForeignKey("organisation.id"), nullable=False, index=True
        ),
        sa.Column("kpis_json", sa.Text, nullable=False),
    )
    op.create_table(
        "turn_log",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("turn", sa.Integer, nullable=False, index=True),
        sa.Column("entity_id", sa.Integer, nullable=True),
        sa.Column("kind", sa.String(60), nullable=False),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column("template", sa.String(60), nullable=True),
        sa.Column("params_json", sa.Text, nullable=False),
        sa.Column("link_kind", sa.String(40), nullable=True),
        sa.Column("link_id", sa.Integer, nullable=True),
    )


def downgrade() -> None:
    for table in (
        "turn_log",
        "turn_snapshot",
        "ledger_line",
        "ledger_entry",
        "organisation",
        "save_meta",
    ):
        op.drop_table(table)
