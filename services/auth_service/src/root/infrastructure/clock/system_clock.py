from datetime import datetime, date
from zoneinfo import ZoneInfo

from root.application.ports import IClock


class SystemClock(IClock):
    def __init__(self, tz: str = 'UTC') -> None:
        self._tz = ZoneInfo(tz)

    def now(self) -> datetime:
        return datetime.now(tz=self._tz)

    def today(self) -> date:
        return self.now().date()
