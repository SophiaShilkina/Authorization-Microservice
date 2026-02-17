from dataclasses import dataclass

from ..exceptions import InvalidTypeError, EmptyValueError


@dataclass(frozen=True, slots=True)
class TokenVO:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise InvalidTypeError('Token must be a string')

        if not self.value.strip():
            raise EmptyValueError('Token value cannot be empty')

    def __str__(self):
        return '********'

    def __repr__(self):
        return 'TokenVO(value="********")'
