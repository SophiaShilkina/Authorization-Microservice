from auth_service.domain.value_objects import EmailVO, PasswordVO, UsernameVO
from auth_service.domain import expections
from auth_service.domain.entities import UserDM
from ..dto import RegisterCommand, RegisterResult
from ..ports import IUserRepository, IPasswordHasher, IEmailService


class RegisterUseCase:
    def __init__(self,
                 user_repo: IUserRepository,
                 password_hasher: IPasswordHasher,
                 email_service: IEmailService,
                 ):
        self._user_repo = user_repo
        self._password_hasher = password_hasher
        self._email_service = email_service

    async def execute(self, cmd: RegisterCommand) -> RegisterResult:
        email = EmailVO(cmd.email)
        password = PasswordVO(cmd.password)
        username = UsernameVO(cmd.username)

        if await self._user_repo.exists_by_email(email):
            raise expections.EmailAlreadyExistsExc('User with this email already exists')

        hashed_password = self._password_hasher.get_password_hash(password)

        user = UserDM.register(
            email=email,
            username=username,
            hashed_password=hashed_password,
        )
        user_id = await self._user_repo.create(user)

        await self._email_service.send_verification_email(
            email=user.email.value,
            username=user.username.value,
        )

        return RegisterResult(
            id=user_id,
            email=user.email.value,
            username=user.username.value,
        )
