from auth_service.domain.value_objects import EmailVO, UsernameVO
from auth_service.domain.entities import UserDM
from ..dto import RegisterUserCommand, RegisterUserResult
from ..ports import IUnitOfWork, IUserRepository, IPasswordHasher, IEmailService, IClock
from ..services import RateLimitService
from ..security.policies import PasswordPolicy, RateLimitPolicy
from ..exceptions import AlreadyExists


class RegisterUserUseCase:
    def __init__(self,
                 uow: IUnitOfWork,
                 user_repo: IUserRepository,
                 password_hasher: IPasswordHasher,
                 email_service: IEmailService,
                 rate_limit_service: RateLimitService,
                 email_rate_limit_policy: RateLimitPolicy,
                 ip_rate_limit_policy: RateLimitPolicy,
                 clock: IClock
                 ):
        self._uow = uow
        self._user_repo = user_repo
        self._password_hasher = password_hasher
        self._email_service = email_service
        self._rate_limit_service = rate_limit_service
        self._email_policy = email_rate_limit_policy
        self._ip_policy = ip_rate_limit_policy
        self._clock = clock

    async def execute(self, cmd: RegisterUserCommand) -> RegisterUserResult:
        await self._rate_limit_service.check(f'register:email:{cmd.email}', self._email_policy)
        await self._rate_limit_service.check(f'register:ip:{cmd.context.ip}', self._ip_policy)

        async with self._uow:
            email = EmailVO(cmd.email)

            if await self._user_repo.exists_by_email(email):
                raise AlreadyExists('User with this email already exists')

            password_hash = self._password_hasher.get_password_hash(PasswordPolicy(cmd.password))

            user = UserDM.register(
                email=email,
                username=UsernameVO(cmd.username),
                password_hash=password_hash,
                occurred_at=self._clock.now(),
            )
            await self._user_repo.create(user)

            await self._email_service.send_verification_email(
                email=user.email.value,
                username=user.username.value,
            )

            return RegisterUserResult(
                id=user.id,
                email=user.email.value,
                username=user.username.value,
            )
