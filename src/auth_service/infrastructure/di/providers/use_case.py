from dishka import Provider, provide, Scope

from auth_service.application.ports import (
    IUnitOfWork,
    IUserRepository,
    IRefreshSessionRepository,
    IRefreshTokenService,
    IAccessTokenService,
    IEmailService,
    IPasswordHasher,
    IClock,
)
from auth_service.application.security.policies import (
    TokenPolicy,
    LoginIPRateLimit,
    LoginEmailRateLimit,
    RegisterIPRateLimit,
    RegisterEmailRateLimit,
    RefreshTokenRateLimit,
    RefreshTokenUserIDRateLimit,
    LogoutAllRateLimit
)
from auth_service.application.services import RateLimitService
from auth_service.application.use_cases import (
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
        uow: IUnitOfWork,
        user_repo: IUserRepository,
        refresh_session_repo: IRefreshSessionRepository,
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
            uow=uow,
            user_repo=user_repo,
            refresh_session_repo=refresh_session_repo,
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
        uow: IUnitOfWork,
        user_repo: IUserRepository,
        password_hasher: IPasswordHasher,
        email_service: IEmailService,
        rate_limit_service: RateLimitService,
        email_rate_limit_policy: RegisterEmailRateLimit,
        ip_rate_limit_policy: RegisterIPRateLimit,
        clock: IClock,
    ) -> RegisterUserUseCase:
        return RegisterUserUseCase(
            uow=uow,
            user_repo=user_repo,
            password_hasher=password_hasher,
            email_service=email_service,
            rate_limit_service=rate_limit_service,
            email_rate_limit_policy=email_rate_limit_policy,
            ip_rate_limit_policy=ip_rate_limit_policy,
            clock=clock,
        )

    @provide(scope=Scope.REQUEST)
    async def refresh_token_uc(
        self,
        uow: IUnitOfWork,
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
            uow=uow,
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
        uow: IUnitOfWork,
        refresh_session_repo: IRefreshSessionRepository,
        refresh_token_service: IRefreshTokenService,
        clock: IClock,
    ) -> LogoutUserUseCase:
        return LogoutUserUseCase(
            uow=uow,
            refresh_session_repo=refresh_session_repo,
            refresh_token_service=refresh_token_service,
            clock=clock,
        )

    @provide(scope=Scope.REQUEST)
    async def logout_all_user_uc(
        self,
        uow: IUnitOfWork,
        refresh_session_repo: IRefreshSessionRepository,
        access_token_service: IAccessTokenService,
        rate_limit_service: RateLimitService,
        user_id_rate_limit_policy: LogoutAllRateLimit,
        clock: IClock,
    ) -> LogoutAllUserUseCase:
        return LogoutAllUserUseCase(
            uow=uow,
            refresh_session_repo=refresh_session_repo,
            access_token_service=access_token_service,
            rate_limit_service=rate_limit_service,
            user_id_rate_limit_policy=user_id_rate_limit_policy,
            clock=clock,
        )
