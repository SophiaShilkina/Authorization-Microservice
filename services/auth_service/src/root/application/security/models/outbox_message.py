from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass(slots=True, kw_only=True, frozen=True)
class OutboxMessage:
    id: UUID
    aggregate_type: str
    aggregate_id: str
    event_type: str
    payload: bytes
    occurred_at: datetime
