from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from auth_service.domain.entities import UserDM, RefreshSessionDM
from auth_service.domain.value_objects import EmailVO


class IUserRepository(Protocol):
    """Repository interface (port) for User aggregate"""

    @abstractmethod
    async def create(self, user: UserDM) -> UUID: ...

    @abstractmethod
    async def get_by_email(self, email: EmailVO) -> UserDM | None: ...

    @abstractmethod
    async def exists_by_email(self, email: EmailVO) -> bool: ...


class IRefreshSessionRepository(Protocol):
    """Repository interface (port) for Token aggregate"""

    @abstractmethod
    async def create(self, session: RefreshSessionDM) -> UUID: ...
