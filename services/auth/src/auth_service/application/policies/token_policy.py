from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class TokenPolicy:
    refresh_ttl: timedelta
    access_ttl: timedelta
