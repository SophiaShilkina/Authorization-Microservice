from root.domain.value_objects import EmailVO
from root.domain.entities import UserDM
from ..dto import RegisterUserCommand, RegisterUserResult
from ..ports import IOutboxRepository, IOutboxMessageFactory, IUserRepository, IPasswordHasher, IClock
from ..services import RateLimitService
from ..security.policies import PasswordPolicy, RegisterEmailRateLimit, RegisterIPRateLimit
from ..exceptions import UserAlreadyExists


class RegisterUserUseCase:
    def __init__(self,
                 user_repo: IUserRepository,
                 outbox_repo: IOutboxRepository,
                 outbox_message_factory: IOutboxMessageFactory,
                 password_hasher: IPasswordHasher,
                 rate_limit_service: RateLimitService,
                 email_rate_limit_policy: RegisterEmailRateLimit,
                 ip_rate_limit_policy: RegisterIPRateLimit,
                 clock: IClock
                 ):
        self._user_repo = user_repo
        self._outbox = outbox_repo
        self._outbox_message_factory = outbox_message_factory
        self._password_hasher = password_hasher
        self._rate_limit_service = rate_limit_service
        self._email_policy = email_rate_limit_policy
        self._ip_policy = ip_rate_limit_policy
        self._clock = clock

    async def execute(self, cmd: RegisterUserCommand) -> RegisterUserResult:
        await self._rate_limit_service.check(f'register:email:{cmd.email}', self._email_policy)
        await self._rate_limit_service.check(f'register:ip:{cmd.context.ip}', self._ip_policy)

        email = EmailVO(cmd.email)
        password_hash = self._password_hasher.get_password_hash(PasswordPolicy(cmd.password))

        user = UserDM.register(
            email=email,
            password_hash=password_hash,
            occurred_at=self._clock.now(),
        )

        try:
            await self._user_repo.create(user)
        except UserAlreadyExists:
            raise

        events = user.pull_domain_events()
        if events:
            messages = await self._outbox_message_factory.create_many(events)
            await self._outbox.add(messages)

        return RegisterUserResult(
            id=user.id,
            email=user.email.value,
        )
