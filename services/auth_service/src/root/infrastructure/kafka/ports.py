from typing import Protocol

from .models import LoadedSchema


class ISchemaRegistryClient(Protocol):
    async def get_or_register(self, subject: str, schema_str: str) -> int: ...


class IWireFormatSerializer(Protocol):
    def serialize(self, schema_id: int, schema_dict: dict, payload: dict) -> bytes: ...


class ISchemaLoader(Protocol):
    async def load_and_cache(self, schema_version: str, schema_name: str) -> LoadedSchema: ...
