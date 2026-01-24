from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.domain.entities import RefreshSessionDM
from auth_service.domain.value_objects import TokenHashVO
from auth_service.application.ports import IRefreshSessionRepository
from ..models import RefreshSessionORM


class SqlAlchemyRefreshSessionRepository(IRefreshSessionRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, refresh_session: RefreshSessionDM) -> None:
        orm_refresh_session = RefreshSessionORM.from_domain(refresh_session)
        self._session.add(orm_refresh_session)

    async def update(self, refresh_session: RefreshSessionDM) -> None:
        stmt = update(RefreshSessionORM).where(
            RefreshSessionORM.token_hash == refresh_session.token_hash
        ).values(
            is_revoked=True,
            updated_at=datetime.now(timezone.utc)
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
            updated_at=datetime.now(timezone.utc)
        )
        result = await self._session.execute(stmt)
        return result.rowcount  # type: ignore

