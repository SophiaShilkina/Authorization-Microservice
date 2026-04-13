from typing import Awaitable, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from ..ports import ITransactionManager


class SqlAlchemyTransactionManager(ITransactionManager):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def run[T](self, action: Callable[[], Awaitable[T]]) -> T:
        try:
            result = await action()
            await self._session.commit()
            return result
        except Exception:
            await self._session.rollback()
            raise
