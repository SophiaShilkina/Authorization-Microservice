from auth_service.domain.value_objects import TokenVO
from ..dto import LogoutAllUserCommand, LogoutAllUserResult
from ..ports import IUnitOfWork, IRefreshSessionRepository, IAccessTokenService, IClock
from ..services import RateLimitService
from ..security.policies import LogoutAllRateLimit


class LogoutAllUserUseCase:
    def __init__(self,
                 uow: IUnitOfWork,
                 refresh_session_repo: IRefreshSessionRepository,
                 access_token_service: IAccessTokenService,
                 rate_limit_service: RateLimitService,
                 user_id_rate_limit_policy: LogoutAllRateLimit,
                 clock: IClock,
                 ):
        self._uow = uow
        self._refresh_session_repo = refresh_session_repo
        self._access_token_service = access_token_service
        self._rate_limit_service = rate_limit_service
        self._user_id_policy = user_id_rate_limit_policy
        self._clock = clock

    async def execute(self, cmd: LogoutAllUserCommand) -> LogoutAllUserResult:
        payload = self._access_token_service.verify(TokenVO(value=cmd.access_token))

        await self._rate_limit_service.check(f'logout_all:user_id:{payload.user_id}', self._user_id_policy)

        async with self._uow:
            revoked_count = await self._refresh_session_repo.revoke_all_by_user_id(
                payload.user_id
            )

            return LogoutAllUserResult(
                revoked_sessions=revoked_count
            )
