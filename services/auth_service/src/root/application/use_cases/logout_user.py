from root.domain.value_objects import TokenVO
from ..schemas.commands import LogoutUserCommand
from ..ports import IRefreshSessionRepository, IRefreshTokenService, IClock
from ..exceptions import AuthenticationFailed, TokenExpired


class LogoutUserUseCase:
    def __init__(self,
                 refresh_session_repo: IRefreshSessionRepository,
                 refresh_token_service: IRefreshTokenService,
                 clock: IClock,
                 ):
        self._refresh_session_repo = refresh_session_repo
        self._refresh_token_service = refresh_token_service
        self._clock = clock

    async def execute(self, cmd: LogoutUserCommand) -> None:
        refresh_hash = self._refresh_token_service.hash(TokenVO(cmd.refresh_token))

        session = await self._refresh_session_repo.get_by_hash(refresh_hash)
        if not session:
            raise AuthenticationFailed('Invalid or revoked token')

        if session.is_expired(self._clock.now()):
            raise TokenExpired('Token expired')

        session.revoke()

        await self._refresh_session_repo.update(session)
