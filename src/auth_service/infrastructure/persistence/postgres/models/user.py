from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean

from .base import BaseORM
from .mixins import IdUUIDPKMixin, CUDateTimeMixin
from auth_service.domain.entities import UserDM
from auth_service.domain.value_objects import EmailVO, UsernameVO, PasswordHashVO


class UserORM(IdUUIDPKMixin, CUDateTimeMixin, BaseORM):
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)

    is_active: Mapped[bool] = mapped_column(Boolean)
    is_verified: Mapped[bool] = mapped_column(Boolean)
    is_blocked: Mapped[bool] = mapped_column(Boolean)

    __table_args__ = (
        {'schema': 'public'}
    )

    @classmethod
    def from_domain(cls, user: UserDM) -> 'UserORM':
        return cls(
            id=user.id,
            email=user.email.value,
            username=user.username.value,
            hashed_password=user.password_hash.value,
            is_active=user.is_active,
            is_verified=user.is_verified,
            is_blocked=user.is_blocked,
        )

    def to_domain(self) -> UserDM:
        return UserDM.hydrate(
            id_=self.id,
            email=EmailVO(self.email),
            username=UsernameVO(self.username),
            password_hash=PasswordHashVO(self.hashed_password),
            is_active=self.is_active,
            is_verified=self.is_verified,
            is_blocked=self.is_blocked,
        )
