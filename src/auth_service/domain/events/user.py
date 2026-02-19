from dataclasses import dataclass
from uuid import UUID

from .base import DomainEvent


@dataclass
class UserDomainEvent(DomainEvent):
    user_id: UUID


@dataclass
class UserRegisteredEvent(UserDomainEvent):
    email: str
    username: str
