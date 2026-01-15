from dataclasses import dataclass

from ..expections import DomainValidationError


@dataclass(frozen=True)
class PasswordVO:
    value: str

    def __post_init__(self):
        if len(self.value) < 8:
            raise DomainValidationError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in self.value):
            raise DomainValidationError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in self.value):
            raise DomainValidationError('Password must contain at least one digit')
