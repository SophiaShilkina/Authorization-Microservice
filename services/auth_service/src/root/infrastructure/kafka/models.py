from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class LoadedSchema:
    raw_json: str
    parsed: dict[str, Any]
