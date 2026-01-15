from dataclasses import dataclass

from ..expections import DomainValidationError


@dataclass(frozen=True, slots=True)
class PasswordVO:
    value: str

    _MIN_LENGTH = 8
    _MAX_LENGTH = 64
    _COMMON = {'password', '123456', 'qwerty', 'admin'}

    def __post_init__(self):
        self._validate_basic()
        self._check_common()

    def _validate_basic(self):
        if len(self.value) < self._MIN_LENGTH:
            raise DomainValidationError(f'Password must be at least {self._MIN_LENGTH} characters long')

        if len(self.value) > self._MAX_LENGTH:
            raise DomainValidationError(f'Password must be at not exceed {self._MAX_LENGTH} characters long')

        if ' ' in self.value:
            raise DomainValidationError('Password must not contain spaces')

        if not any(c.isupper() for c in self.value):
            raise DomainValidationError('Password must contain at least one uppercase letter')

        if not any(c.islower() for c in self.value):
            raise DomainValidationError('Password must contain at least one lowercase letter')

        if not any(c.isdigit() for c in self.value):
            raise DomainValidationError('Password must contain at least one digit')

        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?`~' for c in self.value):
            raise DomainValidationError('Password must contain at least one special character')

    def _check_common(self):
        if self.value.lower() in self._COMMON:
            raise DomainValidationError('Password is too common')

    def __str__(self):
        return '********'

    def __repr__(self):
        return 'PasswordVO(value="********")'
