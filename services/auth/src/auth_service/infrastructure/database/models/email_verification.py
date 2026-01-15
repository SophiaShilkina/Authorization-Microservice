from datetime import datetime
import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy import func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .base import Base
from .mixins import IdIntPKMixin


class EmailVerification(IdIntPKMixin, Base):
    user_id: Mapped[uuid.UUID] = mapped_column(UUID,
                                               ForeignKey("public.users.id",
                                                          onupdate="CASCADE",
                                                          ondelete="SET NULL"))
    code_hash: Mapped[str] = mapped_column(String)

    is_used: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
