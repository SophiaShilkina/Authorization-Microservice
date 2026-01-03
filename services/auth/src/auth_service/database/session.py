from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

from auth_service import config


class EngineManagement:
    def __init__(
            self,
            url: str,
            echo: bool,
            echo_pool: bool,
            pool_size: int,
            max_overflow: int
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


engine_management: EngineManagement = EngineManagement(
    url=config.postgres.dsn,
    echo=config.postgres.echo,
    echo_pool=config.postgres.echo_pool,
    pool_size=config.postgres.pool_size,
    max_overflow=config.postgres.max_overflow,
)
