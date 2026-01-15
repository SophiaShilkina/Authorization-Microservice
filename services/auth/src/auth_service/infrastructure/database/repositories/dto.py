from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UserAllDTO:
    id: UUID
    email: str
    hashed_password: str
    is_active: bool
    is_verified: bool
    is_blocked: bool
    role: str
