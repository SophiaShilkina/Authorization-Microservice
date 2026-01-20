from ..dto import LogoutAllUserCommand, LogoutAllUserResult
from ..ports import IRefreshSessionRepository, ITokenService
from ..services import RateLimitService
from ..security.models import AccessToken
from  ..security.policies import RateLimitPolicy


class LogoutAllUserUseCase:
    def __init__(self,
                 refresh_session_repo: IRefreshSessionRepository,
                 token_service: ITokenService,
                 rate_limit_service: RateLimitService,
                 user_id_rate_limit_policy: RateLimitPolicy,
                 ):
        self._refresh_session_repo = refresh_session_repo
        self._token_service = token_service
        self._rate_limit_service = rate_limit_service
        self._user_id_policy = user_id_rate_limit_policy

    async def execute(self, cmd: LogoutAllUserCommand) -> LogoutAllUserResult:
        payload = self._token_service.verify_access_token(AccessToken(
            token=cmd.access_token,
            expires_at=cmd.access_token_expires_at)
        )

        await self._rate_limit_service.check(f'logout_all:user_id:{payload.user_id}', self._user_id_policy)

        revoked_count = await self._refresh_session_repo.revoke_all_by_user_id(
            payload.user_id
        )

        return LogoutAllUserResult(
            revoked_sessions=revoked_count
        )
