from auth_service.domain import expections
from ..ports import IRefreshSessionRepository, ITokenService
from ..dto import LogoutUserCommand, LogoutUserResult


class LogoutUserUseCase:
    def __init__(self,
                 refresh_session_repo: IRefreshSessionRepository,
                 token_service: ITokenService,
                 ):
        self._refresh_session_repo = refresh_session_repo
        self._token_service = token_service

    async def execute(self, cmd: LogoutUserCommand) -> LogoutUserResult:
        refresh_hash = self._token_service.hash_token(cmd.refresh_token)

        session = await self._refresh_session_repo.get_by_hash(refresh_hash)
        if not session or not session.is_revoked():
            raise expections.Unauthorized('Invalid or revoked token')

        session.revoke()

        await self._refresh_session_repo.update(session)

        return LogoutUserResult(
            check=True
        )
