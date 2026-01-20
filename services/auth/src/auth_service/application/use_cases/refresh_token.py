from auth_service.domain.value_objects import TokenVO, ExpiresAtVO
from ..dto import RefreshTokenCommand, RefreshTokenResult
from ..ports import IRefreshSessionRepository, ITokenService, IClock
from ..services import RateLimitService
from ..exceptions import AuthenticationFailed
from ..security.policies import TokenPolicy, RateLimitPolicy
from ..security.models import AccessTokenPayload


class RefreshTokenUseCase:
    def __init__(self,
                 refresh_session_repo: IRefreshSessionRepository,
                 token_service: ITokenService,
                 rate_limit_service: RateLimitService,
                 token_policy: TokenPolicy,
                 token_rate_limit_policy: RateLimitPolicy,
                 user_id_rate_limit_policy: RateLimitPolicy,
                 clock: IClock,
                 ):
        self._refresh_session_repo = refresh_session_repo
        self._token_service = token_service
        self._rate_limit_service = rate_limit_service
        self._token_policy = token_policy
        self._token_rl_policy = token_rate_limit_policy
        self._user_id_policy = user_id_rate_limit_policy
        self._clock = clock

    async def execute(self, cmd: RefreshTokenCommand) -> RefreshTokenResult:
        refresh_hash = self._token_service.hash_token(TokenVO(cmd.refresh_token))

        await self._rate_limit_service.check(f'refresh:token:{refresh_hash}', self._token_rl_policy)

        now = self._clock.now()

        session = await self._refresh_session_repo.get_by_hash(refresh_hash)
        if not session or not session.is_valid(now):
            raise AuthenticationFailed('Invalid or revoked token')

        await self._rate_limit_service.check(f'register:user_id:{session.user_id}', self._user_id_policy)

        new_raw_refresh, new_refresh_hash = self._token_service.issue_refresh_token()
        new_session = session.rotate(
            new_token_hash=new_refresh_hash,
            expires_at=ExpiresAtVO(now + self._token_policy.refresh_ttl),
            occurred_at=now
        )

        async with self._refresh_session_repo.transaction():
            await self._refresh_session_repo.update(session)
            await self._refresh_session_repo.create(new_session)

        payload = AccessTokenPayload(
            user_id=session.user_id,
            issued_at=now,
            expires_at=ExpiresAtVO(now + self._token_policy.access_ttl),
        )
        access_token = self._token_service.issue_access_token(payload)

        return RefreshTokenResult(
            access_token=access_token.token,
            refresh_token=new_raw_refresh.value,
            expires_at=access_token.expires_at,
        )
