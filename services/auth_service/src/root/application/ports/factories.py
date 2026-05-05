from typing import Protocol

from root.domain.events import DomainEvent
from ..schemas.models import OutboxMessage


class IOutboxMessageFactory(Protocol):
    async def create_many(self, events: list[DomainEvent]) -> list[OutboxMessage]: ...
