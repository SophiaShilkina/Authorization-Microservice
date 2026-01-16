from dataclasses import dataclass

from auth_service.domain.exceptions import DomainValidationError


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
        if len(self.value) < self._MIN_LENGTH or len(self.value) > self._MAX_LENGTH:
            raise DomainValidationError('Password does not fit the length')

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
        lowered = self.value.lower()
        for common in self._COMMON:
            if common in lowered:
                raise DomainValidationError('Password is too common')

    def __str__(self):
        return '********'

    def __repr__(self):
        return 'PasswordVO(value="********")'
