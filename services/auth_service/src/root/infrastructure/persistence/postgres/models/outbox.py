from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, LargeBinary

from root.application.security.models import OutboxMessage
from .base import BaseORM
from .mixins import IdUUIDPKMixin, CDateTimeMixin


class OutboxORM(IdUUIDPKMixin, CDateTimeMixin, BaseORM):
    aggregate_type: Mapped[str] = mapped_column(String)
    aggregate_id: Mapped[str] = mapped_column(String)
    event_type: Mapped[str] = mapped_column(String)
    payload: Mapped[bytes] = mapped_column(LargeBinary)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __tablename__ = 'outbox'
    __table_args__ = (
        {'schema': 'public'}
    )

    @classmethod
    def from_app(cls, message: OutboxMessage) -> 'OutboxORM':
        return cls(
            id=message.id,
            aggregate_type=message.aggregate_type,
            aggregate_id=message.aggregate_id,
            event_type=message.event_type,
            payload=message.payload,
            occurred_at=message.occurred_at,
        )

    def to_app(self) -> OutboxMessage:
        return OutboxMessage(
            id=self.id,
            aggregate_type=self.aggregate_type,
            aggregate_id=self.aggregate_id,
            event_type=self.event_type,
            payload=self.payload,
            occurred_at=self.occurred_at,
        )
