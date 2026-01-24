from datetime import datetime
import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseORM
from .mixins import IdIntPKMixin, CUDateTimeMixin
from auth_service.domain.entities import RefreshSessionDM
from auth_service.domain.value_objects import TokenHashVO, ExpiresAtVO


class RefreshSessionORM(IdIntPKMixin, CUDateTimeMixin, BaseORM):
    user_id: Mapped[uuid.UUID] = mapped_column(UUID,
                                               ForeignKey('public.users.id',
                                                          onupdate='CASCADE',
                                                          ondelete='SET NULL'))
    token_hash: Mapped[str] = mapped_column(String, index=True)

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        {'schema': 'public'}
    )

    @classmethod
    def from_domain(cls, session: RefreshSessionDM) -> 'RefreshSessionORM':
        return cls(
            user_id=session.user_id,
            token_hash=session.token_hash.value,
            expires_at=session.expires_at.value,
            revoked=session.is_revoked,
        )

    def to_domain(self) -> RefreshSessionDM:
        return RefreshSessionDM.hydrate(
            user_id=self.user_id,
            token_hash=TokenHashVO(self.token_hash),
            expires_at=ExpiresAtVO(self.expires_at),
            revoked=self.is_revoked
        )
