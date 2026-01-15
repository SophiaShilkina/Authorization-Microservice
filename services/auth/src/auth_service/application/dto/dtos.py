from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass(frozen=True)
class AccessTokenPayloadDTO:
    user_id: UUID
    roles: tuple[str, ...]
    issued_at: datetime
    expires_at: datetime
