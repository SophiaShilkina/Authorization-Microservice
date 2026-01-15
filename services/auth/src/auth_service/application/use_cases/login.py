from auth_service.domain.value_objects import EmailVO, PasswordVO
from auth_service.domain import expections
from auth_service.domain.entities import RefreshSessionDM
from ..dto import LoginCommand, LoginResult
from ..ports import IUserRepository, IPasswordHasher, ITokenService, IClock


class LoginUseCase:
    def __init__(self,
                 user_repo: IUserRepository,
                 password_hasher: IPasswordHasher,
                 token_service: ITokenService,
                 clock: IClock
                 ):
        self._user_repo = user_repo
        self._password_hasher = password_hasher
        self._token_service = token_service
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
            expires_at=now + timedelta(seconds=cmd.expires_at)
        )

