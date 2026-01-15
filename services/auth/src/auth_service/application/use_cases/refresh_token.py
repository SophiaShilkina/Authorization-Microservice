from auth_service.domain import expections
from ..dto import RefreshTokenCommand, RefreshTokenResult, AccessTokenPayloadDTO
from ..ports import IRefreshSessionRepository, ITokenService, IClock
from ..policies import TokenPolicy


class RefreshTokenUseCase:
    def __init__(self,
                 refresh_session_repo: IRefreshSessionRepository,
                 token_service: ITokenService,
                 policy: TokenPolicy,
                 clock: IClock,
                 ):
        self._refresh_session_repo = refresh_session_repo
        self._token_service = token_service
        self._policy = policy
        self._clock = clock

    async def execute(self, cmd: RefreshTokenCommand) -> RefreshTokenResult:
        refresh_hash = self._token_service.hash_token(cmd.refresh_token)

        now = self._clock.now()

        session = await self._refresh_session_repo.get_by_hash(refresh_hash)

        if not session or not session.is_valid(now):
            raise expections.Unauthorized('Invalid or revoked token')

        new_raw_refresh, new_refresh_hash = self._token_service.issue_refresh_token()
        new_session = session.rotate(
            new_token_hash=new_refresh_hash,
            expires_at=now + self._policy.refresh_ttl,
        )

        async with self._refresh_session_repo.transaction():
            await self._refresh_session_repo.update(session)
            await self._refresh_session_repo.create(new_session)

        payload = AccessTokenPayloadDTO(
            user_id=session.user_id,
            issued_at=now,
            expires_at=now + self._policy.access_ttl,
        )
        access_token = self._token_service.issue_access_token(payload)

        return RefreshTokenResult(
            access_token=access_token.value,
            refresh_token=new_raw_refresh,
            expires_at=access_token.expires_at,
        )
