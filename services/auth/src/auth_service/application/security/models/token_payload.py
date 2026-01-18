from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from auth_service.domain.value_objects import ExpiresAtVO


@dataclass(frozen=True, slots=True)
class AccessTokenPayload:
    user_id: UUID
    issued_at: datetime
    expires_at: ExpiresAtVO
