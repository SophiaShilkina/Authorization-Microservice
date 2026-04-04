from dataclasses import dataclass
import re

from ..exceptions import InvalidTypeError, EmptyValueError, InvalidFormatError


@dataclass(frozen=True, slots=True)
class EmailVO:
    value: str

    _PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise InvalidTypeError('Email must be a string')

        if not self.value.strip():
            raise EmptyValueError('Email cannot be empty')

        normalized = self.value.strip().lower()

        if not self._is_valid_email(normalized):
            raise InvalidFormatError(f'Invalid email format: {self.value}')

        if ".." in normalized:
            raise InvalidFormatError('Email cannot contain consecutive dots')

        local, domain = normalized.split("@", 1)

        if domain.startswith('-') or domain.endswith('-'):
            raise InvalidFormatError('Domain cannot start or end with "-"')

        for label in domain.split('.'):
            if label.startswith('-') or label.endswith('-'):
                raise InvalidFormatError('Domain labels cannot start or end with "-"')

        object.__setattr__(self, "value", normalized)

    def _is_valid_email(self, email: str) -> bool:
        return bool(re.match(self._PATTERN, email))

    def __str__(self) -> str:
        return self.value
