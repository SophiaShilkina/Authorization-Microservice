from typing import Protocol
from datetime import datetime


class IClock(Protocol):
    """Interface (port) for clock service"""

    def now(self) -> datetime: ...
