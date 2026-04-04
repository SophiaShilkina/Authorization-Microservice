from datetime import timedelta

from root.application.ports import IRateLimitStorage
from .base import RedisStorage


class RedisRateLimitStorage(RedisStorage, IRateLimitStorage):
    async def increment(self, key: str, window: timedelta) -> int:
        """Atomic INCR + EXPIRE"""
        async with self._redis.pipeline(transaction=True) as pipe:
            pipe.incr(key)
            pipe.expire(key, int(window.total_seconds()))
            value, _ = await pipe.execute()

        return int(value)

    async def reset(self, key: str) -> None:
        await self._redis.delete(key)
