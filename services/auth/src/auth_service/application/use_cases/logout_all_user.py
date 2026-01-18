from ..dto import LogoutAllUserCommand, LogoutAllUserResult
from ..ports import IRefreshSessionRepository, ITokenService
from ..security.models import AccessToken


class LogoutAllUserUseCase:
    def __init__(self,
                 refresh_session_repo: IRefreshSessionRepository,
                 token_service: ITokenService,
                 ):
        self._refresh_session_repo = refresh_session_repo
        self._token_service = token_service

    async def execute(self, cmd: LogoutAllUserCommand) -> LogoutAllUserResult:
        payload = self._token_service.verify_access_token(AccessToken(
            token=cmd.access_token,
            expires_at=cmd.access_token_expires_at)
        )

        revoked_count = await self._refresh_session_repo.revoke_all_by_user_id(
            payload.user_id
        )

        return LogoutAllUserResult(
            revoked_sessions=revoked_count
        )
