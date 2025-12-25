import logging
from typing import Type, Any, Optional, List, Dict

from sqlalchemy import select, update, delete, and_

from ...database import async_session

logger = logging.getLogger(__name__)


class BaseRepository:
    def __init__(self, model: Type):
        self.model = model

    @staticmethod
    async def _get_session():
        """Генератор сессии для использования в контекстах."""

        async with async_session() as session:
            async with session.begin():
                yield session

    # =========== GET методы ===========

    async def get_by_id(self, id_: int) -> Optional[Any]:
        """Получить по ID"""
        async for session in self._get_session():
            result = await session.execute(
                select(self.model).where(self.model.id == id_)  # type: ignore
            )
            return result.scalar_one_or_none()

    async def _get_by_field(self, field_name: str, value: Any) -> Optional[Any]:
        """Получить по любому полю"""
        async for session in self._get_session():
            field = getattr(self.model, field_name, None)
            if not field:
                raise AttributeError(f"Field {field_name} not found in {self.model}")

            result = await session.execute(
                select(self.model).where(field == value)
            )
            return result.scalar_one_or_none()

    async def _get_all(self, filters: Optional[List] = None) -> List[Any] | None:
        """Получить все записи с возможностью фильтрации"""
        async for session in self._get_session():
            query = select(self.model)

            if filters:
                query = query.where(and_(*filters))

            result = await session.execute(query)
            return result.scalars().all()

    # =========== CREATE методы ===========

    async def create(self, data: Dict) -> Any | None:
        """Создать новую запись"""
        try:
            async for session in self._get_session():
                instance = self.model(**data)
                session.add(instance)
                return instance
        except Exception as error:
            logger.error(f"Create error: {error}")
            raise

    async def bulk_create(self, items: List[Dict]) -> List[Any] | None:
        """Создать несколько записей за раз"""
        try:
            async for session in self._get_session():
                instances = [self.model(**item) for item in items]
                session.add_all(instances)
                return instances
        except Exception as error:
            logger.error(f"Bulk create error: {error}")
            raise

    # =========== UPDATE методы ===========

    async def update_by_id(self, id_: int, data: Dict) -> bool | None:
        """Обновить запись по ID"""
        async for session in self._get_session():
            result = await session.execute(
                select(self.model).where(self.model.id == id_).with_for_update()  # type: ignore
            )
            instance = result.scalar_one_or_none()

            if instance:
                for key, value in data.items():
                    setattr(instance, key, value)
                return True
            return False

    async def _update_where(self, values: Dict, filters: List | None = None) -> int | None:
        """Обновить записи с возможностью фильтрации"""
        async for session in self._get_session():
            query = update(self.model).values(**values)

            if filters:
                query = query.where(and_(*filters))

            result = await session.execute(query)
            return result.rowcount

    # =========== DELETE методы ===========

    async def delete_by_id(self, id_: int) -> bool | None:
        """Удалить запись по ID"""
        async for session in self._get_session():
            result = await session.execute(
                select(self.model).where(self.model.id == id_)  # type: ignore
            )
            instance = result.scalar_one_or_none()

            if instance:
                await session.delete(instance)
                return True
            return False

    async def _delete_where(self, filters: List | None = None) -> int | None:
        """Удалить записи с возможностью фильтрации"""
        async for session in self._get_session():
            query = delete(self.model)

            if filters:
                query = query.where(and_(*filters))

            result = await session.execute(query)
            return result.rowcount
