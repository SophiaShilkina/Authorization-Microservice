from dishka import Provider, provide, Scope

from auth_service.application.ports import (
    IUnitOfWork,
    IUserRepository,
    IRefreshSessionRepository,
    IRateLimitStorage,
    IRefreshTokenService,
    IAccessTokenService,
    IPasswordHasher,
    IClock,
)
from auth_service.application.use_cases import (
    LoginUserUseCase,
    RegisterUserUseCase,
    RefreshTokenUseCase,
    LogoutUserUseCase,
    LogoutAllUserUseCase,
)


class UseCaseProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def login_user_uc(
        self,
        uow: IUnitOfWork,
        user_repo: IUserRepository,
        refresh_repo: IRefreshSessionRepository,
        password_hasher: IPasswordHasher,
        refresh_token_service: IRefreshTokenService,
        access_token_service: IAccessTokenService,
        rate_limit_service: IRateLimitStorage,
        rate_limit: RateLimitPolicy,
        clock: IClock,
    ) -> LoginUserUseCase:
        return LoginUserUseCase(
            uow=uow,
            user_repo=user_repo,
            refresh_session_repo=refresh_repo,
            password_hasher=password_hasher,
            refresh_token_service=refresh_token_service,
            access_token_service=access_token_service,
            rate_limit_service=rate_limit_service,
            rate_limit_storage=rate_limit_storage,
            rate_limit_policy=rate_limit,
            policy=token_policy,
            clock=clock,
        )
