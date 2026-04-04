import httpx

from ..ports import ISchemaRegistryClient


class RedpandaSchemaRegistryClient(ISchemaRegistryClient):
    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")
        self._headers = {
            "Content-Type": "application/vnd.schemaregistry.v1+json",
            "Accept": "application/vnd.schemaregistry.v1+json",
        }

    async def get_or_register(self, subject: str, schema_str: str) -> int:
        async with httpx.AsyncClient(base_url=self._base_url, headers=self._headers) as client:
            lookup_resp = await client.post(
                f"/subjects/{subject}",
                json={"schema": schema_str},
            )
            if lookup_resp.status_code == 200:
                data = lookup_resp.json()
                return data["id"]

            reg_resp = await client.post(
                f"/subjects/{subject}/versions",
                json={"schema": schema_str},
            )
            reg_resp.raise_for_status()
            data = reg_resp.json()
            return data["id"]
