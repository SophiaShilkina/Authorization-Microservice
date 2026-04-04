from ..ports import IRateLimitStorage
from ..security.policies import RateLimitPolicy
from ..exceptions import RateLimitExceeded


class RateLimitService:
    def __init__(self, storage: IRateLimitStorage):
        self._storage = storage

    async def check(
        self,
        key: str,
        policy: RateLimitPolicy,
    ):
        attempts = await self._storage.increment(key, policy.window)
        if attempts > policy.attempts:
            raise RateLimitExceeded('Too many attempts. Try again later')

    async def reset(self, key: str) -> None:
        await self._storage.reset(key)
