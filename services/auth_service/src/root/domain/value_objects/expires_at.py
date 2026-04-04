from dataclasses import dataclass
from datetime import datetime

from ..exceptions import InvalidTypeError, InvariantViolation, TypeMismatch


@dataclass(frozen=True, slots=True)
class ExpiresAtVO:
    value: datetime

    def __post_init__(self):
        if not isinstance(self.value, datetime):
            raise InvalidTypeError('Expires_at must be a datetime')

        if self.value.tzinfo is None:
            raise TypeMismatch('Expires_at must be timezone-aware')

    def _is_same_tz(self, time: datetime) -> None:
        if time.tzinfo is None:
            raise TypeMismatch('Time must be timezone-aware')

        if time.utcoffset() != self.value.utcoffset():
            raise InvariantViolation('Expires_at must be in same timezone')

    def is_expired(self, now: datetime) -> bool:
        self._is_same_tz(now)
        return now >= self.value

    def is_active(self, now: datetime) -> bool:
        return not self.is_expired(now)

    def __str__(self) -> str:
        return self.value.isoformat()
