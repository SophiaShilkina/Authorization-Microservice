from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from root.domain.entities import UserDM
from root.domain.value_objects import EmailVO
from root.application.ports import IUserRepository
from root.application.exceptions import UserAlreadyExists
from ..models import UserORM
from .base import SqlAlchemyRepository


class SqlAlchemyUserRepository(IUserRepository, SqlAlchemyRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: UserDM) -> None:
        orm_user = UserORM.from_domain(user)
        self._session.add(orm_user)

        try:
            await self._session.flush()
        except IntegrityError as exc:
            mapped = self._map_integrity_error(exc)
            if mapped is not None:
                raise mapped from exc
            raise

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

    @staticmethod
    def _map_integrity_error(exc: IntegrityError) -> Exception:
        uq_constraints = ('uq_users_email',)

        constraint_name = SqlAlchemyRepository._extract_constraint_name(exc, uq_constraints)

        match constraint_name:
            case 'uq_users_email':
                return UserAlreadyExists('User already exists')

        return exc
