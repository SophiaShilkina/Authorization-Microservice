"""Initial migration

Revision ID: bd5665e15344
Revises:
Create Date: 2026-02-02 13:25:16.139697

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bd5665e15344"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("is_blocked", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
        schema="public",
    )
    op.create_index(
        op.f("ix_public_users_email"),
        "users",
        ["email"],
        unique=True,
        schema="public",
    )
    op.create_table(
        "refresh_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("token_hash", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_revoked", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["public.users.id"],
            name=op.f("fk_refresh_sessions_user_id_users"),
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_refresh_sessions")),
        schema="public",
    )
    op.create_index(
        op.f("ix_public_refresh_sessions_token_hash"),
        "refresh_sessions",
        ["token_hash"],
        unique=False,
        schema="public",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_public_refresh_sessions_token_hash"),
        table_name="refresh_sessions",
        schema="public",
    )
    op.drop_table("refresh_sessions", schema="public")
    op.drop_index(
        op.f("ix_public_users_email"), table_name="users", schema="public"
    )
    op.drop_table("users", schema="public")
