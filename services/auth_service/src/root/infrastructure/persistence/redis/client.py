import redis.asyncio as redis


class RedisClient:
    def __init__(self,
                 url: str,
                 encoding: str,
                 decode_responses: bool,):
        self._redis = redis.from_url(
            url,
            encoding=encoding,
            decode_responses=decode_responses,
        )

    @property
    def client(self):
        return self._redis
