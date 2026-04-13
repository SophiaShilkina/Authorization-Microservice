from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from root.domain.entities import RefreshSessionDM
from root.domain.value_objects import TokenHashVO
from root.application.ports import IRefreshSessionRepository, IClock
from root.infrastructure.persistence.postgres.sqlalchemy.models import RefreshSessionORM


class SqlAlchemyRefreshSessionRepository(IRefreshSessionRepository):
    def __init__(self,
                 session: AsyncSession,
                 clock: IClock,
                 ):
        self._session = session
        self._clock = clock

    async def create(self, refresh_session: RefreshSessionDM) -> None:
        orm_refresh_session = RefreshSessionORM.from_domain(refresh_session)
        self._session.add(orm_refresh_session)

    async def update(self, refresh_session: RefreshSessionDM) -> None:
        stmt = update(RefreshSessionORM).where(
            RefreshSessionORM.token_hash == refresh_session.token_hash.value
        ).values(
            is_revoked=True,
            updated_at=self._clock.now()
        )
        await self._session.execute(stmt)

    async def get_by_hash(self, refresh_hash: TokenHashVO) -> RefreshSessionDM | None:
        stmt = select(RefreshSessionORM).where(RefreshSessionORM.token_hash == refresh_hash.value)
        result = await self._session.execute(stmt)
        orm_refresh_session = result.scalar_one_or_none()
        return orm_refresh_session.to_domain() if orm_refresh_session else None

    async def revoke_all_by_user_id(self, user_id: UUID) -> int:
        stmt = update(RefreshSessionORM).where(
            RefreshSessionORM.user_id == user_id,
            RefreshSessionORM.is_revoked == False,
        ).values(
            is_revoked=True,
            updated_at=self._clock.now()
        )
        result = await self._session.execute(stmt)
        return result.rowcount  # type: ignore
