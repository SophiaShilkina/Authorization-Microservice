from dishka import Provider, provide, Scope

from root.application.ports import (
    IUserRepository,
    IRefreshSessionRepository,
    IOutboxRepository,
    IOutboxMessageFactory,
    IRefreshTokenService,
    IAccessTokenService,
    IPasswordHasher,
    IClock,
)
from root.application.security.policies import (
    TokenPolicy,
    LoginIPRateLimit,
    LoginEmailRateLimit,
    RegisterIPRateLimit,
    RegisterEmailRateLimit,
    RefreshTokenRateLimit,
    RefreshTokenUserIDRateLimit,
    LogoutAllRateLimit
)
from root.application.services import RateLimitService
from root.application.use_cases import (
    LoginUserUseCase,
    RegisterUserUseCase,
    RefreshTokenUseCase,
    LogoutUserUseCase,
    LogoutAllUserUseCase,
)


class UseCaseProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def login_user_uc(
        self,
        user_repo: IUserRepository,
        refresh_session_repo: IRefreshSessionRepository,
        outbox_repo: IOutboxRepository,
        outbox_message_factory: IOutboxMessageFactory,
        password_hasher: IPasswordHasher,
        refresh_token_service: IRefreshTokenService,
        access_token_service: IAccessTokenService,
        rate_limit_service: RateLimitService,
        token_policy: TokenPolicy,
        email_rate_limit_policy: LoginEmailRateLimit,
        ip_rate_limit_policy: LoginIPRateLimit,
        clock: IClock,
    ) -> LoginUserUseCase:
        return LoginUserUseCase(
            user_repo=user_repo,
            refresh_session_repo=refresh_session_repo,
            outbox_repo=outbox_repo,
            outbox_message_factory=outbox_message_factory,
            password_hasher=password_hasher,
            refresh_token_service=refresh_token_service,
            access_token_service=access_token_service,
            rate_limit_service=rate_limit_service,
            token_policy=token_policy,
            email_rate_limit_policy=email_rate_limit_policy,
            ip_rate_limit_policy=ip_rate_limit_policy,
            clock=clock,
        )

    @provide(scope=Scope.REQUEST)
    async def register_user_uc(
        self,
        user_repo: IUserRepository,
        outbox_repo: IOutboxRepository,
        outbox_message_factory: IOutboxMessageFactory,
        password_hasher: IPasswordHasher,
        rate_limit_service: RateLimitService,
        email_rate_limit_policy: RegisterEmailRateLimit,
        ip_rate_limit_policy: RegisterIPRateLimit,
        clock: IClock,
    ) -> RegisterUserUseCase:
        return RegisterUserUseCase(
            user_repo=user_repo,
            outbox_repo=outbox_repo,
            outbox_message_factory=outbox_message_factory,
            password_hasher=password_hasher,
            rate_limit_service=rate_limit_service,
            email_rate_limit_policy=email_rate_limit_policy,
            ip_rate_limit_policy=ip_rate_limit_policy,
            clock=clock,
        )

    @provide(scope=Scope.REQUEST)
    async def refresh_token_uc(
        self,
        refresh_session_repo: IRefreshSessionRepository,
        refresh_token_service: IRefreshTokenService,
        access_token_service: IAccessTokenService,
        rate_limit_service: RateLimitService,
        token_policy: TokenPolicy,
        token_rate_limit_policy: RefreshTokenRateLimit,
        user_id_rate_limit_policy: RefreshTokenUserIDRateLimit,
        clock: IClock,
    ) -> RefreshTokenUseCase:
        return RefreshTokenUseCase(
            refresh_session_repo=refresh_session_repo,
            refresh_token_service=refresh_token_service,
            access_token_service=access_token_service,
            rate_limit_service=rate_limit_service,
            token_policy=token_policy,
            token_rate_limit_policy=token_rate_limit_policy,
            user_id_rate_limit_policy=user_id_rate_limit_policy,
            clock=clock,
        )

    @provide(scope=Scope.REQUEST)
    async def logout_user_uc(
        self,
        refresh_session_repo: IRefreshSessionRepository,
        refresh_token_service: IRefreshTokenService,
        clock: IClock,
    ) -> LogoutUserUseCase:
        return LogoutUserUseCase(
            refresh_session_repo=refresh_session_repo,
            refresh_token_service=refresh_token_service,
            clock=clock,
        )

    @provide(scope=Scope.REQUEST)
    async def logout_all_user_uc(
        self,
        refresh_session_repo: IRefreshSessionRepository,
        access_token_service: IAccessTokenService,
        rate_limit_service: RateLimitService,
        user_id_rate_limit_policy: LogoutAllRateLimit,
        clock: IClock,
    ) -> LogoutAllUserUseCase:
        return LogoutAllUserUseCase(
            refresh_session_repo=refresh_session_repo,
            access_token_service=access_token_service,
            rate_limit_service=rate_limit_service,
            user_id_rate_limit_policy=user_id_rate_limit_policy,
            clock=clock,
        )
