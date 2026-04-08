from collections.abc import AsyncIterator

from dishka import Provider, provide, Scope
import httpx

from root.application.ports import IOutboxMessageFactory
from ...kafka.ports import ISchemaLoader, ISchemaRegistryClient, IWireFormatSerializer

from ...kafka.avro import FileSystemAvroSchemaLoader, AvroWireFormatSerializer, AvroOutboxMessageFactory
from ...kafka.redpanda.schema_registry import RedpandaSchemaRegistryClient, open_client

from ...config import Config


class KafkaProvider(Provider):

    @provide(scope=Scope.APP)
    def schema_loader(self, config: Config) -> ISchemaLoader:
        app = config.app
        return FileSystemAvroSchemaLoader(base_dir=app.base_dir)

    @provide(scope=Scope.APP)
    async def http_client(self, config: Config) -> AsyncIterator[httpx.AsyncClient]:
        redpanda = config.redpanda
        async with open_client(
                schema_registry_base_url=redpanda.shema_registry_dsn
        ) as client:
            yield client

    @provide(scope=Scope.APP)
    def registry_client(self, http_client: httpx.AsyncClient,) -> ISchemaRegistryClient:
        return RedpandaSchemaRegistryClient(http_client=http_client)

    @provide(scope=Scope.APP)
    def serializer(self) -> IWireFormatSerializer:
        return AvroWireFormatSerializer()

    @provide(scope=Scope.APP)
    def message_factory(self,
                   schema_registry: ISchemaRegistryClient,
                   avro_serializer: IWireFormatSerializer,
                   schema_loader: ISchemaLoader) -> IOutboxMessageFactory:
        return AvroOutboxMessageFactory(schema_registry, avro_serializer, schema_loader)
