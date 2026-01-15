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
class UserLoggedInEvent(DomainEvent):
    user_id: UUID
    ip_address: str
    user_agent: str
    success: bool


@dataclass
class UserLoginFailedEvent(DomainEvent):
    email: str
    ip_address: str
    user_agent: str
    reason: str


@dataclass
class CreateRefreshSessionEvent(DomainEvent):
    session_id: UUID
    user_id: UUID
    expires_at: datetime
