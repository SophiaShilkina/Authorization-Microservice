from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs

from auth_service.utils import camel_case_to_snake_case


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore
        return f'{camel_case_to_snake_case(cls.__name__)}s'

    id: Mapped[int] = mapped_column(primary_key=True)
