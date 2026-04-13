from typing import Awaitable, Callable
from uuid import UUID

from ..ports import ITransactionManager, IInboxRepository


class KafkaExecutor:
    def __init__(self,
        tx: ITransactionManager,
        inbox_repo: IInboxRepository,
    ):
        self._tx = tx
        self._inbox_repo = inbox_repo

    async def execute[T](self, message_id: UUID, action: Callable[[], Awaitable[T]]) -> T | None:
        async def wrapped() -> T | None:
            if await self._inbox_repo.exists(message_id):
                return None

            result = await action()
            await self._inbox_repo.add_processed(message_id)
            return result

        return await self._tx.run(wrapped)
