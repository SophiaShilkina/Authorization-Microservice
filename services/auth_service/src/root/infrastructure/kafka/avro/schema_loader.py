import json
from pathlib import Path

from ..ports import ISchemaLoader
from ..models import LoadedSchema
from ...exceptions import SchemaNotFoundError


class FileSystemAvroSchemaLoader(ISchemaLoader):
    def __init__(self, base_dir: Path):
        self._schemas_dir = base_dir / 'contracts' / 'avro'
        self._cache: dict[str, LoadedSchema] = {}

    async def load_and_cache(self, schema_version: str, schema_name: str) -> LoadedSchema:
        key = f"{schema_version}:{schema_name}"
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        path = self._schemas_dir / schema_version / f'{schema_name}.avsc'
        if not path.exists():
            raise SchemaNotFoundError(f'Schema not found: {path}')

        raw_json = path.read_text(encoding="utf-8")
        parsed = json.loads(raw_json)

        loaded = LoadedSchema(raw_json=raw_json, parsed=parsed)
        self._cache[schema_name] = loaded
        return loaded
