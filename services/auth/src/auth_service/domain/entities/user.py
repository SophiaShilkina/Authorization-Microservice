from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime

from ..value_objects import EmailVO, UsernameVO
from ..expections import DomainValidationError
from ..events import UserRegisteredEvent


@dataclass
class UserDM:
    id: UUID
    email: EmailVO
    username: UsernameVO
    hashed_password: str
    active: bool
    blocked: bool
    verified: bool
    _domain_events: list = field(default_factory=list, init=False, repr=False)

    @classmethod
    def register(
            cls,
            email: EmailVO,
            username: UsernameVO,
            hashed_password: str,
    ) -> 'UserDM':

        user = cls(
            id=uuid4(),
            email=email,
            username=username,
            hashed_password=hashed_password,
            active=True,
            verified=False,
            blocked=False,
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

    def is_active(self) -> bool:
        return self.active

    def is_blocked(self) -> bool:
        return self.blocked

    def is_verified(self) -> bool:
        return self.verified

    def ensure_can_login(self) -> None:
        if not self.is_active() or self.is_blocked():
            raise DomainValidationError('The user is blocked or deactivate')

    def deactivate(self) -> None:
        if not self.is_active():
            raise DomainValidationError('User is already deactivated')
        self.active = False

    def block(self) -> None:
        if self.is_blocked():
            raise DomainValidationError('User is already blocked')
        self.blocked = True

    def verify(self) -> None:
        if self.is_verified():
            raise DomainValidationError('User is already verified')
        self.verified = True

    def add_domain_event(self, event) -> None:
        self._domain_events.append(event)

    def pull_domain_events(self) -> list:
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events
