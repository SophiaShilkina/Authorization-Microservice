from dataclasses import dataclass
import re

from ..expections import DomainValidationError


@dataclass(frozen=True, slots=True)
class UsernameVO:
    value: str

    _MIN_LENGTH = 3
    _MAX_LENGTH = 30
    _PATTERN = r'^[a-zA-Z0-9_-]+$'

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise DomainValidationError(f'Username must be a string, got {type(self.value)}')

        if len(self.value) < self._MIN_LENGTH or len(self.value) > self._MAX_LENGTH:
            raise DomainValidationError('Username does not fit the length')

        if not self._is_valid_username(self.value):
            raise DomainValidationError('Username can only contain numbers, dashes, underscores, and Latin letters')

        if set(self.value) <= {'_', '-'}:
            raise DomainValidationError('Username cannot consist only of special characters')

        if self.value.startswith(('_', '-')) or self.value.endswith(('_', '-')):
            raise DomainValidationError('Username cannot start or end with underscore or hyphen')

    def _is_valid_username(self, username: str) -> bool:
        return bool(re.match(self._PATTERN, username))

    def __str__(self) -> str:
        return self.value
