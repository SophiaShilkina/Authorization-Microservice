from dataclasses import dataclass
import re

from ..exceptions import InvalidTypeError, EmptyValueError, InvalidLengthError, InvalidFormatError


@dataclass(frozen=True, slots=True)
class UsernameVO:
    value: str

    _MIN_LENGTH = 3
    _MAX_LENGTH = 30
    _PATTERN = r'^[a-zA-Z0-9_-]+$'

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise InvalidTypeError('Username must be a string')

        if not self.value.strip():
            raise EmptyValueError('Username cannot be empty')

        if len(self.value) < self._MIN_LENGTH or len(self.value) > self._MAX_LENGTH:
            raise InvalidLengthError('Username does not fit the length')

        if not self._is_valid_username(self.value):
            raise InvalidFormatError('Username can only contain numbers, dashes, underscores, and Latin letters')

        if set(self.value) <= {'_', '-'}:
            raise InvalidFormatError('Username cannot consist only of special characters')

        if self.value.startswith(('_', '-')) or self.value.endswith(('_', '-')):
            raise InvalidFormatError('Username cannot start or end with underscore or hyphen')

    def _is_valid_username(self, username: str) -> bool:
        return bool(re.match(self._PATTERN, username))

    def __str__(self) -> str:
        return self.value
