from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True, slots=True)
class RateLimitPolicy:
    attempts: int
    window: timedelta
