from dataclasses import dataclass
import re

from ..expections import DomainValidationError


@dataclass(frozen=True, slots=True)
class EmailVO:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise DomainValidationError(f'Email must be a string, got {type(self.value)}')

        normalized = self.value.strip().lower()

        if not self._is_valid_email(normalized):
            raise DomainValidationError(f'Invalid email format: {self.value}')

        if ".." in normalized:
            raise DomainValidationError("Email cannot contain consecutive dots")

        local, domain = normalized.split("@", 1)

        if domain.startswith('-') or domain.endswith('-'):
            raise DomainValidationError('Domain cannot start or end with "-"')

        for label in domain.split('.'):
            if label.startswith('-') or label.endswith('-'):
                raise DomainValidationError('Domain labels cannot start or end with "-"')

        object.__setattr__(self, "value", normalized)

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def __str__(self) -> str:
        return self.value
