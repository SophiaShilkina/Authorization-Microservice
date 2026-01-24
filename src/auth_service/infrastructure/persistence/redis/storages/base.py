class RedisStorage:
    def __init__(self, client):
        self._redis = client
