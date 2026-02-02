from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from ...persistence.redis.client import RedisClient

from ...persistence.postgres.uow import SqlAlchemyUnitOfWork
from ...persistence.postgres.repositories import SqlAlchemyUserRepository, SqlAlchemyRefreshSessionRepository
from ...persistence.redis.storages import RedisRateLimitStorage
from ...security.tokens import JoseAccessTokenService, RandomRefreshTokenService
from ...security.password import ArgonPasswordHasher
from ...email_service.fake_email_service import FakeEmailService
from ...clock import SystemClock

from ...config import Config

from auth_service.application.services import RateLimitService
from auth_service.application.ports import (
    IUserRepository,
    IRefreshSessionRepository,
    IRateLimitStorage,
    IRefreshTokenService,
    IAccessTokenService,
    IEmailService,
    IPasswordHasher,
    IClock, IUnitOfWork,
)


class InfrastructureProvider(Provider):

    @provide(scope=Scope.APP)
    def redis_client(self, config: Config) -> RedisClient:
        r = config.redis
        return RedisClient(
            url=r.dsn,
            encoding=r.encoding,
            decode_responses=r.decode_responses,
        )

    @provide(scope=Scope.APP)
    def rate_limit_storage(self, redis_client: RedisClient) -> IRateLimitStorage:
        return RedisRateLimitStorage(redis_client)

    # ===============================

    @provide(scope=Scope.REQUEST)
    def uow(self, session: AsyncSession) -> IUnitOfWork:
        return SqlAlchemyUnitOfWork(session)

    @provide(scope=Scope.REQUEST)
    def user_repository(self, session: AsyncSession) -> IUserRepository:
        return SqlAlchemyUserRepository(session)

    @provide(scope=Scope.REQUEST)
    def refresh_session_repository(self, session: AsyncSession, clock: IClock) -> IRefreshSessionRepository:
        return SqlAlchemyRefreshSessionRepository(session, clock)

    @provide(scope=Scope.REQUEST)
    def rate_limit_service(self, rate_limit_storage: IRateLimitStorage) -> RateLimitService:
        return RateLimitService(rate_limit_storage)

    @provide(scope=Scope.APP)
    def refresh_token_service(self) -> IRefreshTokenService:
        return RandomRefreshTokenService()

    @provide(scope=Scope.APP)
    def access_token_service(self, config: Config) -> IAccessTokenService:
        at = config.access_token
        return JoseAccessTokenService(
            public_key=at.public_key.get_secret_value(),
            private_key=at.private_key.get_secret_value(),
            algorithm=at.algorithm,
            ttl_minutes=at.ttl_minutes,
        )

    @provide(scope=Scope.APP)
    def email_service(self) -> IEmailService:
        return FakeEmailService()

    @provide(scope=Scope.APP)
    def password_hasher(self) -> IPasswordHasher:
        return ArgonPasswordHasher()

    @provide(scope=Scope.APP)
    def clock(self) -> IClock:
        return SystemClock()
