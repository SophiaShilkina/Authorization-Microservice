from typing import AsyncGenerator

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from ...persistence.postgres.client import PostgresClient
from ...persistence.redis.client import RedisClient

from ...persistence.postgres.repositories import SqlAlchemyUserRepository, SqlAlchemyRefreshSessionRepository
from ...persistence.redis.storages import RedisRateLimitStorage
from ...security.tokens import JoseAccessTokenService, RandomTokenService
from ...security.password import ArgonPasswordHasher
from ...clock import SystemClock

from ...config import Config

from auth_service.application.services import RateLimitService
from auth_service.application.ports import (
    IUserRepository,
    IRefreshSessionRepository,
    IRateLimitStorage,
    IRefreshTokenService,
    IAccessTokenService,
    IPasswordHasher,
    IClock,
)


class InfrastructureProvider(Provider):
    def __init__(self, config: Config):
        self._config = config

    @provide(scope=Scope.APP)
    def postgres_client(self) -> PostgresClient:
        return PostgresClient(
            url='postgresql+asyncpg://user:pass@localhost/db',
            echo=False,
            echo_pool=False,
            pool_size=5,
            max_overflow=10,
        )

    @provide(scope=Scope.REQUEST)
    async def session_provider(self, postgres_client: PostgresClient) -> AsyncGenerator[AsyncSession, None]:
        async with postgres_client.session_factory() as session:
            yield session

    @provide(scope=Scope.APP)
    def redis_client(self) -> RedisClient:
        return RedisClient(
            url='redis://localhost:6379',
            encoding='utf-8',
            decode_responses=True,
        )

    @provide(scope=Scope.APP)
    def rate_limit_storage(self, redis_client: RedisClient) -> IRateLimitStorage:
        return RedisRateLimitStorage(redis_client)

    # ===============================

    @provide(scope=Scope.REQUEST)
    def user_repository(self, session: AsyncSession) -> IUserRepository:
        return SqlAlchemyUserRepository(session)

    @provide(scope=Scope.REQUEST)
    def refresh_session_repository(self, session: AsyncSession) -> IRefreshSessionRepository:
        return SqlAlchemyRefreshSessionRepository(session)

    @provide(scope=Scope.APP)
    def rate_limit_service(self, rate_limit_storage: IRateLimitStorage) -> RateLimitService:
        return RateLimitService(rate_limit_storage)

    @provide(scope=Scope.APP)
    def refresh_token_service(self) -> IRefreshTokenService:
        return RandomTokenService()

    @provide(scope=Scope.APP)
    def access_token_service(self) -> IAccessTokenService:
        return JoseAccessTokenService()

    @provide(scope=Scope.APP)
    def password_hasher(self) -> IPasswordHasher:
        return ArgonPasswordHasher()

    @provide(scope=Scope.APP)
    def clock(self) -> IClock:
        return SystemClock()
