from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime

from ..value_objects import EmailVO, UsernameVO, PasswordHashVO
from ..exceptions import InvariantViolation, BusinessRuleViolation
from ..events import UserRegisteredEvent, DomainEvent


@dataclass(slots=True)
class UserDM:
    _id: UUID
    _email: EmailVO
    _username: UsernameVO
    _password_hash: PasswordHashVO
    _active: bool
    _blocked: bool
    _verified: bool
    _domain_events: list[DomainEvent] = field(default_factory=list, init=False, repr=False)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def email(self) -> EmailVO:
        return self._email

    @property
    def username(self) -> UsernameVO:
        return self._username

    @property
    def password_hash(self) -> PasswordHashVO:
        return self._password_hash

    @property
    def is_active(self) -> bool:
        return self._active

    @property
    def is_blocked(self) -> bool:
        return self._blocked

    @property
    def is_verified(self) -> bool:
        return self._verified

    @classmethod
    def register(
            cls,
            email: EmailVO,
            username: UsernameVO,
            password_hash: PasswordHashVO,
    ) -> 'UserDM':

        user = cls(
            _id=uuid4(),
            _email=email,
            _username=username,
            _password_hash=password_hash,
            _active=True,
            _verified=False,
            _blocked=False,
        )

        user.add_domain_event(
            UserRegisteredEvent(
                user_id=user.id,
                email=user.email.value,
                username=user.username.value,
                occurred_at=datetime.now()
            )
        )

        return user

    def ensure_can_login(self) -> None:
        if not self.is_active or self.is_blocked:
            raise InvariantViolation('The user is blocked or deactivate')

    def deactivate(self) -> None:
        if not self.is_active:
            raise InvariantViolation('User is already deactivated')
        self._active = False

    def activate(self) -> None:
        if self.is_active:
            raise InvariantViolation('User is already active')
        self._active = True

    def block(self) -> None:
        if self.is_blocked:
            raise InvariantViolation('User is already blocked')
        self._blocked = True

    def unblock(self) -> None:
        if not self.is_blocked:
            raise InvariantViolation('User is not blocked')
        self._blocked = False

    def verify(self) -> None:
        if self.is_verified:
            raise InvariantViolation('User is already verified')
        self._verified = True

    def change_email(self, new_email: EmailVO) -> None:
        if self._email == new_email:
            raise BusinessRuleViolation('New email is the same as current')
        self._email = new_email

    def change_username(self, new_username: UsernameVO) -> None:
        if self._username == new_username:
            raise BusinessRuleViolation('New username is the same as current')
        self._username = new_username

    def change_password_hash(self, new_password_hash: PasswordHashVO):
        self._password_hash = new_password_hash

    def add_domain_event(self, event) -> None:
        self._domain_events.append(event)

    def pull_domain_events(self) -> list:
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events
