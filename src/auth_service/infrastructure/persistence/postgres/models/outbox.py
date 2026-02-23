from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String, Integer, JSON

from .base import BaseORM
from .mixins import IdUUIDPKMixin


class OutboxORM(IdUUIDPKMixin, BaseORM):
    topic: Mapped[str] = mapped_column(String)
    key: Mapped[str] = mapped_column(String)

    payload: Mapped[str] = mapped_column(JSON)

    status: Mapped[str] = mapped_column(String, default='pending')
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        {'schema': 'public'}
    )