import logging
from typing import Type, Any
from uuid import UUID

from sqlalchemy import select, update, delete, and_, insert
from collections.abc import Sequence
from sqlalchemy.sql import ColumnElement
from sqlalchemy.orm import DeclarativeBase

from auth_service.infrastructure.database import async_session

logger = logging.getLogger(__name__)


class BaseRepository:
    def __init__(self, model: Type[DeclarativeBase]):
        self.model = model

    # =========== GET методы ===========

    async def _get_by_id(self, id_: int, columns: Sequence | None = None) -> dict | None:
        """
        Получить по ID
        :param id_: ID получаемой записи
        :param columns: Поля, которые нужно получить. None - получаем все поля
        :return: Словарь в формате: {Название_поля: Значение, ...}
        """

        async with async_session() as session:
            result = await session.execute(
                select(
                    *(columns or self.model.__table__.columns)
                ).where(self.model.id == id_)  # type: ignore[attr-defined]
            )
            row = result.mappings().one_or_none()
            return dict(row) if row else None

    async def _get_one(self, *, filters: Sequence[ColumnElement[bool]] | None = None, columns: Sequence | None = None) -> dict | None:
        """
        Получить одну строку
        :param filters: По каким полям фильтровать
        :param columns: Поля, которые нужно получить. None - получаем все поля
        :return: Словарь в формате: {Название_поля: Значение, ...}
        """

        async with async_session() as session:
            stmt = select(*(columns or self.model.__table__.columns))

            if filters:
                stmt = stmt.where(and_(*filters))

            result = await session.execute(stmt)
            row = result.mappings().one_or_none()
            return dict(row) if row else None

    async def _get_many(self, *, filters: Sequence[ColumnElement[bool]] | None = None, columns: Sequence | None = None) -> list[dict]:
        """
        Получить множество строку
        :param filters: По каким полям фильтровать
        :param columns: Поля, которые нужно получить. None - получаем все поля
        :return: Список словарей в формате: [{Название_поля: Значение, ...}, ...]
        """

        async with async_session() as session:
            stmt = select(*(columns or self.model.__table__.columns))

            if filters:
                stmt = stmt.where(and_(*filters))

            result = await session.execute(stmt)
            return [dict(row) for row in result.mappings().all()]

    # =========== CREATE методы ===========

    async def create(self, data: dict[str, Any]) -> int | UUID:
        """
        Создать новую запись
        :param data: Данные для заполнения в формате словаря
        :return: ID новой записи
        :exception Exception: Ошибка при занесении данных в базу (конфликт)
        """

        try:
            async with async_session() as session:
                async with session.begin():
                    stmt = (
                        insert(self.model)
                        .values(**data)
                        .returning(self.model.id)  # type: ignore[attr-defined]
                    )
                    result = await session.execute(stmt)
                    return result.scalar_one()

        except Exception:
            logger.exception(f'Create error')
            raise


    async def bulk_create(self, items: list[dict[str, Any]]) -> list[int]:
        """
        Создать несколько новых записей за одно обращение к БД
        :param items: Данные для заполнения в формате списка словарей
        :return: Список ID новых записей
        :exception Exception: Ошибка при занесении данных в базу (конфликт)
        """

        try:
            async with async_session() as session:
                async with session.begin():
                    stmt = (
                        insert(self.model)
                        .values(items)
                        .returning(self.model.id)  # type: ignore[attr-defined]
                    )
                    result = await session.execute(stmt)
                    return list(result.scalars().all())

        except Exception:
            logger.exception(f'Bulk create error')
            raise

    # =========== UPDATE методы ===========

    async def update_by_id(self, id_: int, values: dict[str, Any]) -> bool:
        """
        Обновить запись по ID
        :param id_: ID обновляемой записи
        :param values: Обновляемые данные в формате словаря
        :return: True - если была обновлена одна строка, False - остальное
        """

        async with async_session() as session:
            async with session.begin():
                stmt = (
                    update(self.model)
                    .where(self.model.id == id_)  # type: ignore[attr-defined]
                    .values(**values)
                )
                result = await session.execute(stmt)
                return result.rowcount == 1  # type: ignore[attr-defined]

    async def _update_where(self, *, values: dict[str, Any], filters: Sequence[ColumnElement[bool]]) -> int:
        """
        Обновить записи с фильтрацией
        :param values: Обновляемые данные в формате словаря
        :param filters: По каким полям фильтровать обновление
        :return: Количество затронутых операцией строк (даже если значение не изменилось)
        """

        async with async_session() as session:
            async with session.begin():
                stmt = (
                    update(self.model)
                    .values(**values)
                    .where(and_(*filters))
                )
                result = await session.execute(stmt)
                return result.rowcount  # type: ignore[attr-defined]

    # =========== DELETE методы ===========

    async def delete_by_id(self, id_: int) -> bool:
        """
        Удалить запись по ID
        :param id_: ID удаляемой записи
        :return: True - если была удалена одна строка, False - остальное
        """

        async with async_session() as session:
            async with session.begin():
                stmt = delete(self.model).where(self.model.id == id_)  # type: ignore[attr-defined]
                result = await session.execute(stmt)
                return result.rowcount == 1  # type: ignore[attr-defined]

    async def _delete_where(self, filters: Sequence[ColumnElement[bool]]) -> int:
        """
        Удалить записи с фильтрацией
        :param filters: По каким полям фильтровать удаление
        :return: Количество затронутых операцией строк
        """

        async with async_session() as session:
            async with session.begin():
                stmt = delete(self.model).where(and_(*filters))
                result = await session.execute(stmt)
                return result.rowcount  # type: ignore[attr-defined]
