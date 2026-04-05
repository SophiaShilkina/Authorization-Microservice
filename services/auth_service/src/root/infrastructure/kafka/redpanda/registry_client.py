import httpx

from ..ports import ISchemaRegistryClient


class RedpandaSchemaRegistryClient(ISchemaRegistryClient):
    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")
        self._headers = {
            "Content-Type": "application/vnd.schemaregistry.v1+json",
            "Accept": "application/vnd.schemaregistry.v1+json",
        }
        self._cache: dict[str, int] = {}

    async def get_or_register(self, subject: str, schema_str: str) -> int:
        _id = self._cache.get(subject)
        if _id is not None:
            return _id

        async with httpx.AsyncClient(base_url=self._base_url, headers=self._headers) as client:
            lookup_resp = await client.post(
                f"/subjects/{subject}",
                json={"schema": schema_str},
            )
            if lookup_resp.status_code == 200:
                schema_id = lookup_resp.json()["id"]
                self._cache[subject] = schema_id
                return schema_id

            reg_resp = await client.post(
                f"/subjects/{subject}/versions",
                json={"schema": schema_str},
            )
            reg_resp.raise_for_status()
            schema_id = reg_resp.json()["id"]
            self._cache[subject] = schema_id
            return schema_id

    def cache(self, subject: str) -> int | None:
        cached = self._cache.get(subject)
        if cached is not None:
            return cached
        return None
