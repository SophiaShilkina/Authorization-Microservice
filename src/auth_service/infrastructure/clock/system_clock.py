from datetime import datetime, timezone

from auth_service.application.ports import IClock


class SystemClock(IClock):
    def now(self) -> datetime:
        return datetime.now(tz=timezone.utc)
