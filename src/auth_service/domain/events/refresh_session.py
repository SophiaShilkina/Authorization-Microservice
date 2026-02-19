from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .base import DomainEvent


@dataclass
class RefreshSessionDomainEvent(DomainEvent):
    pass


@dataclass
class CreateRefreshSessionEvent(RefreshSessionDomainEvent):
    user_id: UUID
    expires_at: datetime
