from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.application.ports import IOutboxRepository, IClock
from auth_service.domain.events import DomainEvent


class SqlAlchemyOutboxRepository(IOutboxRepository):
    def __init__(self,
                 session: AsyncSession,
                 clock: IClock,):
        self._session = session
        self._clock = clock

    async def add(self, events: list[DomainEvent]) -> None:
        pass
