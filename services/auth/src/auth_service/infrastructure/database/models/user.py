from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy import func, CheckConstraint

from .base import Base
from .mixins import IdUUIDPKMixin


class User(IdUUIDPKMixin, Base):
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True)
    role: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String(length=1024))

    is_active: Mapped[bool] = mapped_column(Boolean, server_default='true')
    is_verified: Mapped[bool] = mapped_column(Boolean, server_default='false')
    is_blocked: Mapped[bool] = mapped_column(Boolean, server_default='false')

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now())

    __table_args__ = (
        CheckConstraint(
            role.in_(["user", "volunteer", "shelter_worker"]),
            name="role"
        ),
        {'schema': 'public'}
    )
