from auth_service.domain.value_objects import EmailVO, PasswordVO
from auth_service.domain import expections
from auth_service.domain.entities import RefreshSessionDM
from ..dto import LoginCommand, LoginResult, AccessTokenPayloadDTO
from ..ports import IUserRepository, IRefreshSessionRepository, IPasswordHasher, ITokenService, IClock
from ..policies import TokenPolicy


class LoginUseCase:
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

    async def execute(self, cmd: LoginCommand) -> LoginResult:
        email = EmailVO(cmd.email)
        password = PasswordVO(cmd.password)

        user = await self._user_repo.get_by_email(email)

        if not user:
            self._password_hasher.dummy_verify(password)
            raise expections.AuthenticationFailed('Invalid email or password')

        if not self._password_hasher.verify(password, user.hashed_password):
            raise expections.AuthenticationFailed('Invalid email or password')

        user.ensure_can_login()

        now = self._clock.now()

        raw_refresh, refresh_hash = self._token_service.issue_refresh_token()

        session = RefreshSessionDM.create(
            user_id=user.id,
            token_hash=refresh_hash,
            expires_at=now + self._policy.refresh_ttl,
        )
        await self._refresh_session_repo.create(session)

        payload = AccessTokenPayloadDTO(
            user_id=user.id,
            issued_at=now,
            expires_at=now + self._policy.access_ttl,
        )
        access_token = self._token_service.issue_access_token(payload)

        return LoginResult(
            access_token=access_token.value,
            refresh_token=raw_refresh,
            expires_at=access_token.expires_at,
        )
