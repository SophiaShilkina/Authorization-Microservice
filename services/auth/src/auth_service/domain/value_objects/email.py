from dataclasses import dataclass
import re

from ..expections import DomainValidationError


@dataclass(frozen=True)
class EmailVO:
    value: str

    def __post_init__(self):
        if not self._is_valid_email(self.value):
            raise DomainValidationError(f'Invalid email format: {self.value}')

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def __str__(self) -> str:
        return self.value
