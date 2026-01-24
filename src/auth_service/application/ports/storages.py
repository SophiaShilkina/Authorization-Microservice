from typing import Protocol
from datetime import timedelta


class IRateLimitStorage(Protocol):
    async def increment(self, key: str, window: timedelta) -> int: ...

    async def reset(self, key: str) -> None: ...
