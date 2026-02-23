from auth_service.domain.value_objects import TokenVO, ExpiresAtVO
from ..dto import RefreshTokenCommand, RefreshTokenResult
from ..ports import IUnitOfWork, IRefreshSessionRepository, IRefreshTokenService, IAccessTokenService, IClock
from ..services import RateLimitService
from ..exceptions import AuthenticationFailed
from ..security.policies import TokenPolicy, RefreshTokenRateLimit, RefreshTokenUserIDRateLimit
from ..security.models import AccessTokenPayload


class RefreshTokenUseCase:
    def __init__(self,
                 uow: IUnitOfWork,
                 refresh_session_repo: IRefreshSessionRepository,
                 refresh_token_service: IRefreshTokenService,
                 access_token_service: IAccessTokenService,
                 rate_limit_service: RateLimitService,
                 token_policy: TokenPolicy,
                 token_rate_limit_policy: RefreshTokenRateLimit,
                 user_id_rate_limit_policy: RefreshTokenUserIDRateLimit,
                 clock: IClock,
                 ):
        self._uow = uow
        self._refresh_session_repo = refresh_session_repo
        self._refresh_token_service = refresh_token_service
        self._access_token_service = access_token_service
        self._rate_limit_service = rate_limit_service
        self._token_policy = token_policy
        self._token_rl_policy = token_rate_limit_policy
        self._user_id_policy = user_id_rate_limit_policy
        self._clock = clock

    async def execute(self, cmd: RefreshTokenCommand) -> RefreshTokenResult:
        refresh_hash = self._refresh_token_service.hash(TokenVO(cmd.refresh_token))

        await self._rate_limit_service.check(f'refresh:token:{refresh_hash.value}', self._token_rl_policy)

        now = self._clock.now()

        async with self._uow:
            session = await self._refresh_session_repo.get_by_hash(refresh_hash)

            if not session or not session.is_valid(now):
                raise AuthenticationFailed('Invalid or revoked token')

            await self._rate_limit_service.check(f'register:user_id:{session.user_id}', self._user_id_policy)

            new_raw_refresh, new_refresh_hash = self._refresh_token_service.generate()
            new_session = session.rotate(
                new_token_hash=new_refresh_hash,
                expires_at=ExpiresAtVO(now + self._token_policy.refresh_ttl),
                occurred_at=now
            )

            await self._refresh_session_repo.update(session)
            await self._refresh_session_repo.create(new_session)

        payload = AccessTokenPayload(
            user_id=session.user_id,
        )
        access_token = self._access_token_service.issue(payload, now)

        return RefreshTokenResult(
            access_token=access_token.value,
            refresh_token=new_raw_refresh.value,
        )
