from datetime import datetime
import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Boolean, JSON
from sqlalchemy import func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, INET

from .base import Base
from .mixins import IdIntPKMixin


class RefreshToken(IdIntPKMixin, Base):
    user_id: Mapped[uuid.UUID] = mapped_column(UUID,
                                               ForeignKey("public.users.id",
                                                          onupdate="CASCADE",
                                                          ondelete="SET NULL"))
    token_hash: Mapped[str] = mapped_column(String, index=True)

    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    is_under_investigation: Mapped[bool] = mapped_column(Boolean, default=False)

    device_info: Mapped[dict] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[str] = mapped_column(INET, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_used_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
