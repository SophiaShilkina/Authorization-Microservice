from typing import AsyncGenerator

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine

from auth_service.infrastructure.config import Config


class PostgresProvider(Provider):

    @provide(scope=Scope.APP)
    def engine(self, config: Config) -> AsyncEngine:
        pg = config.postgres
        return create_async_engine(
            pg.dsn,
            echo=pg.echo,
            echo_pool=pg.echo_pool,
            pool_size=pg.pool_size,
            max_overflow=pg.max_overflow,
        )

    @provide(scope=Scope.APP)
    def session_factory(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    @provide(scope=Scope.REQUEST)
    async def session(
            self,
            session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session
