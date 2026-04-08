from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import httpx

@asynccontextmanager
async def open_client(schema_registry_base_url: str) -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(
            base_url=schema_registry_base_url.rstrip("/"),
            headers={
                "Content-Type": "application/vnd.schemaregistry.v1+json",
                "Accept": "application/vnd.schemaregistry.v1+json",
            },
            timeout=5.0,
    ) as client:
        yield client
