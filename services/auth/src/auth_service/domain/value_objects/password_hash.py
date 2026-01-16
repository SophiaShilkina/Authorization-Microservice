from dataclasses import dataclass

from ..exceptions import InvalidTypeError, EmptyValueError, InvalidLengthError


@dataclass(frozen=True, slots=True)
class PasswordHashVO:
    value: str

    _MIN_LENGTH = 32

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise InvalidTypeError('Password hash must be a string')

        if not self.value.strip():
            raise EmptyValueError('Password hash cannot be empty')

        if len(self.value) < self._MIN_LENGTH:
            raise InvalidLengthError('Password hash is too short')

    def __str__(self):
        return '********'

    def __repr__(self):
        return 'HashedPasswordVO(value="********")'
