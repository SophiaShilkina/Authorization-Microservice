from sqlalchemy.ext.asyncio import AsyncSession

from root.application.ports import IOutboxRepository
from root.application.schemas.models import OutboxMessage
from root.infrastructure.persistence.postgres.sqlalchemy.models import OutboxORM


class SqlAlchemyOutboxRepository(IOutboxRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, messages: list[OutboxMessage]) -> None:
        inserts = []
        for message in messages:
            inserts.append(OutboxORM.from_app(message))
        self._session.add_all(inserts)
