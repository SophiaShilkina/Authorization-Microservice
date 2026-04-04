from root.domain.value_objects import EmailVO, ExpiresAtVO
from root.domain.entities import RefreshSessionDM
from root.domain.exceptions import InvariantViolation
from ..dto import LoginUserCommand, LoginUserResult
from ..ports import (IUnitOfWork, IOutboxRepository, IOutboxMessageFactory, IUserRepository, IRefreshSessionRepository,
                     IPasswordHasher, IRefreshTokenService, IAccessTokenService, IClock)
from ..services import RateLimitService
from ..exceptions import AuthenticationFailed
from ..security.policies import TokenPolicy, PasswordPolicy, LoginIPRateLimit, LoginEmailRateLimit
from ..security.models import AccessTokenPayload


class LoginUserUseCase:
    def __init__(self,
                 uow: IUnitOfWork,
                 user_repo: IUserRepository,
                 refresh_session_repo: IRefreshSessionRepository,
                 outbox: IOutboxRepository,
                 outbox_message_factory: IOutboxMessageFactory,
                 password_hasher: IPasswordHasher,
                 refresh_token_service: IRefreshTokenService,
                 access_token_service: IAccessTokenService,
                 rate_limit_service: RateLimitService,
                 token_policy: TokenPolicy,
                 email_rate_limit_policy: LoginEmailRateLimit,
                 ip_rate_limit_policy: LoginIPRateLimit,
                 clock: IClock,
                 ):
        self._uow = uow
        self._user_repo = user_repo
        self._refresh_session_repo = refresh_session_repo
        self._outbox = outbox
        self._outbox_message_factory = outbox_message_factory
        self._password_hasher = password_hasher
        self._refresh_token_service = refresh_token_service
        self._access_token_service = access_token_service
        self._rate_limit_service = rate_limit_service
        self._token_policy = token_policy
        self._email_policy = email_rate_limit_policy
        self._ip_policy = ip_rate_limit_policy
        self._clock = clock

    async def execute(self, cmd: LoginUserCommand) -> LoginUserResult:
        await self._rate_limit_service.check(f"login:email:{cmd.email}", self._email_policy)
        await self._rate_limit_service.check(f"login:ip:{cmd.context.ip}", self._ip_policy)

        password = PasswordPolicy(cmd.password)

        async with self._uow:
            user = await self._user_repo.get_by_email(EmailVO(cmd.email))

            if not user:
                self._password_hasher.dummy_verify(password)
                raise AuthenticationFailed('Invalid email or password')

            if not self._password_hasher.verify(password, user.password_hash):
                raise AuthenticationFailed('Invalid email or password')

            try:
                user.ensure_can_login()
            except InvariantViolation as error:
                raise AuthenticationFailed(str(error))

            raw_refresh, refresh_hash = self._refresh_token_service.generate()

            now = self._clock.now()

            session = RefreshSessionDM.create(
                user_id=user.id,
                token_hash=refresh_hash,
                expires_at=ExpiresAtVO(now + self._token_policy.refresh_ttl),
                occurred_at=now,
            )
            await self._refresh_session_repo.create(session)

            events = session.pull_domain_events()
            if events:
                messages = await self._outbox_message_factory.create_many(events)
                await self._outbox.add(messages)

        payload = AccessTokenPayload(
            user_id=user.id,
        )
        access_token = self._access_token_service.issue(payload, now)

        return LoginUserResult(
            access_token=access_token.value,
            refresh_token=raw_refresh.value,
        )
