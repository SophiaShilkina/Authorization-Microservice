from dataclasses import dataclass
import re

from ..expections import DomainValidationError


@dataclass(frozen=True)
class UsernameVO:
    value: str

    def __post_init__(self):
        if len(self.value) < 3:
            raise DomainValidationError('Username must be at least 3 characters long')
        if not self._is_valid_username(self.value):
            raise DomainValidationError('A username can only contain numbers, dashes, underscores, and Latin letters')

    @staticmethod
    def _is_valid_username(username: str) -> bool:
        pattern = r'^[a-zA-Z0-9_-]+$'
        return bool(re.match(pattern, username))

    def __str__(self) -> str:
        return self.value
