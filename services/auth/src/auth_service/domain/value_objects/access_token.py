from dataclasses import dataclass
from datetime import datetime

from ..exceptions import InvalidTypeError, EmptyValueError


@dataclass(frozen=True, slots=True)
class AccessTokenVO:
    value: str
    expires_at: datetime

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise InvalidTypeError('Token must be a string')

        if not isinstance(self.expires_at, datetime):
            raise InvalidTypeError('expires_at must be a datetime')

        if not self.value.strip():
            raise EmptyValueError('Token value cannot be empty')

        if self.expires_at.tzinfo is None:
            raise InvalidTypeError('expires_at must be timezone-aware')

    def is_expired(self, now: datetime) -> bool:
        return now >= self.expires_at

    def is_active(self, now: datetime) -> bool:
        return not self.is_expired(now)

    def __str__(self) -> str:
        if len(self.value) <= 8:
            return '***'
        return f'{self.value[:4]}...{self.value[-4:]}'

    def __repr__(self) -> str:
        return f'AccessTokenVO(expires_at={self.expires_at.isoformat()})'
