from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy import ForeignKey, CheckConstraint, func


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # -------- Metadata --------
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            role.in_(["ADMIN", "MODER"]),
            name="check_role"
        ),
        {'schema': 'public'}
    )

    # -------- Relationships --------
