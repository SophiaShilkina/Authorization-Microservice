from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class AccessToken:
    token: str
    expires_at: datetime

    def is_expired(self, now: datetime) -> bool:
        return now >= self.expires_at

    def __str__(self) -> str:
        if len(self.token) <= 8:
            return '***'
        return f'{self.token[:4]}...{self.token[-4:]}'
