from typing import Protocol
from datetime import datetime, date


class IClock(Protocol):
    """Interface (port) for clock service"""

    def now(self) -> datetime: ...
    def today(self) -> date: ...
