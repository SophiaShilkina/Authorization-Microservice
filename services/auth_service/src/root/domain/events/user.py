from dataclasses import dataclass
from uuid import UUID

from .base import DomainEvent


@dataclass(slots=True, kw_only=True, frozen=True)
class UserDomainEvent(DomainEvent):
    user_id: UUID


@dataclass(slots=True, kw_only=True, frozen=True)
class UserRegisteredEvent(UserDomainEvent):
    email: str
