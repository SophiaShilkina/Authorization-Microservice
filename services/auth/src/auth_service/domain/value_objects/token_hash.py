from dataclasses import dataclass

from ..exceptions import InvalidTypeError, EmptyValueError, InvalidLengthError


@dataclass(frozen=True, slots=True)
class TokenHashVO:
    value: str

    _MIN_LENGTH = 32

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise InvalidTypeError('Token hash must be a string')

        if not self.value.strip():
            raise EmptyValueError('Token hash cannot be empty')

        if len(self.value) < self._MIN_LENGTH:
            raise InvalidLengthError('Token hash is too short')

    def __str__(self):
        return '********'

    def __repr__(self):
        return 'TokenHashVO(value="********")'
