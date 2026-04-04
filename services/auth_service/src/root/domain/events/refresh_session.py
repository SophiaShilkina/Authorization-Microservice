from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .base import DomainEvent


@dataclass(slots=True, kw_only=True, frozen=True)
class RefreshSessionDomainEvent(DomainEvent):
    pass


@dataclass(slots=True, kw_only=True, frozen=True)
class RefreshSessionCreatedEvent(RefreshSessionDomainEvent):
    user_id: UUID
    token_hash: str
    expires_at: datetime
