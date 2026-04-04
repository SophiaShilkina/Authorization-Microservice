from typing import Protocol
from uuid import UUID

from root.domain.entities import UserDM, RefreshSessionDM
from root.domain.value_objects import EmailVO, TokenHashVO
from ..security.models import OutboxMessage


class IUnitOfWork(Protocol):
    async def __aenter__(self): ...

    async def __aexit__(self, exc_type, exc, tb): ...

    async def commit(self): ...

    async def rollback(self): ...


class IOutboxRepository(Protocol):
    async def add(self, events: list[OutboxMessage]) -> None: ...


class IUserRepository(Protocol):
    """Repository interface (port) for User aggregate"""

    async def create(self, user: UserDM) -> None: ...

    async def get_by_email(self, email: EmailVO) -> UserDM | None: ...

    async def exists_by_email(self, email: EmailVO) -> bool: ...


class IRefreshSessionRepository(Protocol):
    """Repository interface (port) for Session aggregate"""

    async def create(self, session: RefreshSessionDM) -> None: ...

    async def update(self, session: RefreshSessionDM) -> None: ...

    async def get_by_hash(self, refresh_hash: TokenHashVO) -> RefreshSessionDM | None: ...

    async def revoke_all_by_user_id(self, user_id: UUID) -> int: ...
