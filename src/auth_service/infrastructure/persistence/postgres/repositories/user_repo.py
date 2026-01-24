from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.domain.entities import UserDM
from auth_service.domain.value_objects import EmailVO
from auth_service.application.ports import IUserRepository
from ..models import UserORM


class SqlAlchemyUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: UserDM) -> None:
        orm_user = UserORM.from_domain(user)
        self._session.add(orm_user)

    async def get_by_email(self, email: EmailVO) -> UserDM | None:
        stmt = select(UserORM).where(UserORM.email == email.value)
        result = await self._session.execute(stmt)
        orm_user = result.scalar_one_or_none()
        return orm_user.to_domain() if orm_user else None

    async def exists_by_email(self, email: EmailVO) -> bool:
        stmt = select(UserORM).where(UserORM.email == email.value)
        result = await self._session.execute(stmt)
        orm_user = result.scalar_one_or_none()
        return bool(orm_user)
