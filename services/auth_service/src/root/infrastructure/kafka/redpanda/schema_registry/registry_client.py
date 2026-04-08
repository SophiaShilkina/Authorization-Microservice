import httpx

from root.infrastructure.kafka.ports import ISchemaRegistryClient


class RedpandaSchemaRegistryClient(ISchemaRegistryClient):
    def __init__(self, http_client: httpx.AsyncClient):
        self._client = http_client
        self._cache: dict[str, int] = {}

    async def get_or_register(self, subject: str, schema_str: str) -> int:
        schema_id = self._cache.get(subject)
        if schema_id is not None:
            return schema_id

        lookup_resp = await self._client.post(
            f"/subjects/{subject}",
            json={"schema": schema_str},
        )
        if lookup_resp.status_code == 200:
            schema_id = lookup_resp.json()["id"]
            self._cache[subject] = schema_id
            return schema_id

        reg_resp = await self._client.post(
            f"/subjects/{subject}/versions",
            json={"schema": schema_str},
        )
        reg_resp.raise_for_status()
        schema_id = reg_resp.json()["id"]
        self._cache[subject] = schema_id
        return schema_id
