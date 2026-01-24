from dataclasses import dataclass

from ...exceptions import InvalidLengthError, InvalidFormatError, InvalidTypeError, EmptyValueError


@dataclass(frozen=True, slots=True)
class PasswordPolicy:
    value: str

    _MIN_LENGTH = 8
    _MAX_LENGTH = 64
    _COMMON = {'password', '123456', 'qwerty', 'admin'}

    def __post_init__(self):
        self._validate_basic()
        self._check_common()

    def _validate_basic(self):
        if not isinstance(self.value, str):
            raise InvalidTypeError('Password must be a string')

        if not self.value.strip():
            raise EmptyValueError('Token value cannot be empty')

        if ' ' in self.value:
            raise InvalidFormatError('Password must not contain spaces')

        if len(self.value) < self._MIN_LENGTH or len(self.value) > self._MAX_LENGTH:
            raise InvalidLengthError('Password does not fit the length')

        if not any(c.isupper() for c in self.value):
            raise InvalidFormatError('Password must contain at least one uppercase letter')

        if not any(c.islower() for c in self.value):
            raise InvalidFormatError('Password must contain at least one lowercase letter')

        if not any(c.isdigit() for c in self.value):
            raise InvalidFormatError('Password must contain at least one digit')

        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?`~' for c in self.value):
            raise InvalidFormatError('Password must contain at least one special character')

    def _check_common(self):
        lowered = self.value.lower()
        for common in self._COMMON:
            if common in lowered:
                raise InvalidFormatError('Password is too common')

    def __str__(self):
        return '********'

    def __repr__(self):
        return 'PasswordPolicy(value="********")'
