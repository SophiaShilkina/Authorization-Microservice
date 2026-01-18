from auth_service.domain.value_objects import EmailVO, UsernameVO
from auth_service.domain import exceptions
from auth_service.domain.entities import UserDM
from ..dto import RegisterUserCommand, RegisterUserResult
from ..ports import IUserRepository, IPasswordHasher, IEmailService
from ..policies import PasswordPolicy


class RegisterUserUseCase:
    def __init__(self,
                 user_repo: IUserRepository,
                 password_hasher: IPasswordHasher,
                 email_service: IEmailService,
                 ):
        self._user_repo = user_repo
        self._password_hasher = password_hasher
        self._email_service = email_service

    async def execute(self, cmd: RegisterUserCommand) -> RegisterUserResult:
        email = EmailVO(cmd.email)
        password = PasswordPolicy(cmd.password)
        username = UsernameVO(cmd.username)

        if await self._user_repo.exists_by_email(email):
            raise exceptions.EmailAlreadyExistsExc('User with this email already exists')

        password_hash = self._password_hasher.get_password_hash(password.value)

        user = UserDM.register(
            email=email,
            username=username,
            password_hash=password_hash,
        )
        user_id = await self._user_repo.create(user)

        await self._email_service.send_verification_email(
            email=user.email.value,
            username=user.username.value,
        )

        return RegisterUserResult(
            id=user_id,
            email=user.email.value,
            username=user.username.value,
        )
