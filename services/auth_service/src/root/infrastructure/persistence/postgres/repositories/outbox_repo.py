from sqlalchemy.ext.asyncio import AsyncSession

from root.application.ports import IOutboxRepository
from root.application.security.models import OutboxMessage
from ..models import OutboxORM


class SqlAlchemyOutboxRepository(IOutboxRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, events: list[OutboxMessage]) -> None:
        inserts = []
        for event in events:
            inserts.append(OutboxORM.from_app(event))
        self._session.add_all(inserts)
