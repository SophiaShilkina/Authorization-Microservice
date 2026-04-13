from typing import Protocol, Awaitable, Callable
from uuid import UUID


class IInboxRepository(Protocol):
    async def exists(self, message_id: UUID) -> None: ...

    async def add_processed(self, message_id: UUID) -> None: ...


class ITransactionManager:
    async def run[T](self, action: Callable[[], Awaitable[T]]) -> T: ...
