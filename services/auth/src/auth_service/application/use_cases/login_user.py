from auth_service.domain.value_objects import EmailVO, ExpiresAtVO
from auth_service.domain.entities import RefreshSessionDM
from ..dto import LoginUserCommand, LoginUserResult
from ..ports import IUserRepository, IRefreshSessionRepository, IPasswordHasher, ITokenService, IClock
from ..exceptions import AuthenticationFailed
from ..security.policies import TokenPolicy, PasswordPolicy
from ..security.models import AccessTokenPayload


class LoginUserUseCase:
    def __init__(self,
                 user_repo: IUserRepository,
                 refresh_session_repo: IRefreshSessionRepository,
                 password_hasher: IPasswordHasher,
                 token_service: ITokenService,
                 policy: TokenPolicy,
                 clock: IClock,
                 ):
        self._user_repo = user_repo
        self._refresh_session_repo = refresh_session_repo
        self._password_hasher = password_hasher
        self._token_service = token_service
        self._policy = policy
        self._clock = clock

    async def execute(self, cmd: LoginUserCommand) -> LoginUserResult:
        password = PasswordPolicy(cmd.password)

        user = await self._user_repo.get_by_email(EmailVO(cmd.email))

        if not user:
            self._password_hasher.dummy_verify(password)
            raise AuthenticationFailed('Invalid email or password')

        if not self._password_hasher.verify(password, user.password_hash):
            raise AuthenticationFailed('Invalid email or password')

        user.ensure_can_login()

        now = self._clock.now()

        raw_refresh, refresh_hash = self._token_service.issue_refresh_token()

        session = RefreshSessionDM.create(
            user_id=user.id,
            token_hash=refresh_hash,
            expires_at=ExpiresAtVO(now + self._policy.refresh_ttl),
            occurred_at=now,
        )
        await self._refresh_session_repo.create(session)

        payload = AccessTokenPayload(
            user_id=user.id,
            issued_at=now,
            expires_at=ExpiresAtVO(now + self._policy.access_ttl),
        )
        access_token = self._token_service.issue_access_token(payload)

        return LoginUserResult(
            access_token=access_token.token,
            refresh_token=raw_refresh.value,
            expires_at=access_token.expires_at,
        )
