import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from config import config as proj_config
from src.ct_backend.database.models import Base

dsn = proj_config.postgres.dsn

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
EXCLUDED_SCHEMAS = {"tiger", "topology", "tiger_data"}
EXCLUDED_TABLES = {"spatial_ref_sys", "alembic_version"}


def run_migrations_offline() -> None:
    """Миграции в offline-режиме."""
    context.configure(
        url=dsn,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Конфигурируем Alembic для работы с соединением."""
    context.configure(connection=connection,
                      target_metadata=target_metadata,
                      include_object=include_object,
                      compare_type=True,
                      compare_server_default=True,
                      compare_index=True,
                      version_table_schema="public",
                      transactional=True)

    with context.begin_transaction():
        context.run_migrations()


def include_object(object, name, type_, reflected, compare_to):
    if reflected:
        if hasattr(object, 'schema') and object.schema != 'public':
            return False

    if type_ == "table" and name in EXCLUDED_TABLES:
        return False

    return True


async def run_async_migrations() -> None:
    """Миграции в online-режиме с asyncpg."""
    connectable = create_async_engine(
        dsn,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
