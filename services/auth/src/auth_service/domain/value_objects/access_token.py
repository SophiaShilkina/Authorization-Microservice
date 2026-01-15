from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AccessTokenVO:
    value: str
    expires_at: datetime
