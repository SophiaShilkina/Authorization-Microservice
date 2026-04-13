from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyInboxRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
