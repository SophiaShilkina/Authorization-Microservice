from auth_service.domain.value_objects import TokenVO
from ..ports import IRefreshSessionRepository, ITokenService, IClock
from ..dto import LogoutUserCommand
from ..exceptions import AuthenticationFailed, TokenExpired


class LogoutUserUseCase:
    def __init__(self,
                 refresh_session_repo: IRefreshSessionRepository,
                 token_service: ITokenService,
                 clock: IClock,
                 ):
        self._refresh_session_repo = refresh_session_repo
        self._token_service = token_service
        self._clock = clock

    async def execute(self, cmd: LogoutUserCommand) -> None:
        refresh_hash = self._token_service.hash_token(TokenVO(cmd.refresh_token))

        session = await self._refresh_session_repo.get_by_hash(refresh_hash)
        if not session:
            raise AuthenticationFailed('Invalid or revoked token')

        now = self._clock.now()

        if session.is_expired(now):
            raise TokenExpired('Token expired')

        session.revoke()

        await self._refresh_session_repo.update(session)
