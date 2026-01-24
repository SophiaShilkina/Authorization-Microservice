from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class DomainEvent:
    occurred_at: datetime


@dataclass
class UserRegisteredEvent(DomainEvent):
    user_id: UUID
    email: str
    username: str


@dataclass
class CreateRefreshSessionEvent(DomainEvent):
    user_id: UUID
    expires_at: datetime
