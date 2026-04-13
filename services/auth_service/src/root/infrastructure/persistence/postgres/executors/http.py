from typing import Awaitable, Callable

from ..ports import ITransactionManager


class HttpExecutor:
    def __init__(self, tx: ITransactionManager):
        self._tx = tx

    async def execute[T](self, action: Callable[[], Awaitable[T]]) -> T:
        return await self._tx.run(action)
