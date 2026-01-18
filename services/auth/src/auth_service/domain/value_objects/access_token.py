from dataclasses import dataclass

from .expires_at import ExpiresAtVO
from ..exceptions import InvalidTypeError, EmptyValueError


@dataclass(frozen=True, slots=True)
class AccessTokenVO:
    value: str
    expires_at: ExpiresAtVO

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise InvalidTypeError('Token must be a string')

        if not self.value.strip():
            raise EmptyValueError('Token value cannot be empty')

    def __str__(self) -> str:
        if len(self.value) <= 8:
            return '***'
        return f'{self.value[:4]}...{self.value[-4:]}'
