from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import datetime

from .base import BaseDM
from ..value_objects import EmailVO, PasswordHashVO
from ..exceptions import InvariantViolation, BusinessRuleViolation
from ..events import UserRegisteredEvent


@dataclass(slots=True)
class UserDM(BaseDM):
    _id: UUID
    _email: EmailVO
    _password_hash: PasswordHashVO
    _active: bool
    _blocked: bool
    _verified: bool

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def email(self) -> EmailVO:
        return self._email

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
            password_hash: PasswordHashVO,
            occurred_at: datetime
    ) -> 'UserDM':

        user = cls(
            _id=uuid4(),
            _email=email,
            _password_hash=password_hash,
            _active=True,
            _verified=False,
            _blocked=False,
        )

        user._add_domain_event(
            UserRegisteredEvent(
                event_id=uuid4(),
                user_id=user.id,
                email=user.email.value,
                occurred_at=occurred_at
            )
        )

        return user

    @classmethod
    def hydrate(
            cls,
            *,
            id_: UUID,
            email: EmailVO,
            password_hash: PasswordHashVO,
            is_active: bool,
            is_verified: bool,
            is_blocked: bool,
    ) -> 'UserDM':
        return cls(
            _id=id_,
            _email=email,
            _password_hash=password_hash,
            _active=is_active,
            _verified=is_verified,
            _blocked=is_blocked,
        )

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

    def change_password_hash(self, new_password_hash: PasswordHashVO):
        self._password_hash = new_password_hash
