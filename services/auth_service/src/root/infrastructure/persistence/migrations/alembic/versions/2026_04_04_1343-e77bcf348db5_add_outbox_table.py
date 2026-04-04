"""Add Outbox table

Revision ID: e77bcf348db5
Revises: bd5665e15344
Create Date: 2026-04-04 13:43:50.673445

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e77bcf348db5"
down_revision: Union[str, Sequence[str], None] = "bd5665e15344"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "outbox",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("aggregate_type", sa.String(), nullable=False),
        sa.Column("aggregate_id", sa.String(), nullable=False),
        sa.Column("event_type", sa.String(), nullable=False),
        sa.Column("payload", sa.LargeBinary(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_outbox")),
        schema="public",
    )
    op.drop_constraint(
        op.f("fk_refresh_sessions_user_id_users"),
        "refresh_sessions",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("fk_refresh_sessions_user_id_users"),
        "refresh_sessions",
        "users",
        ["user_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
        onupdate="CASCADE",
        ondelete="SET NULL",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        op.f("fk_refresh_sessions_user_id_users"),
        "refresh_sessions",
        schema="public",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("fk_refresh_sessions_user_id_users"),
        "refresh_sessions",
        "users",
        ["user_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="SET NULL",
    )
    op.drop_table("outbox", schema="public")
