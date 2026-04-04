from dishka import Provider, provide, Scope

from root.application.ports import IOutboxMessageFactory
from ...kafka.ports import ISchemaLoader, ISchemaRegistryClient, IWireFormatSerializer

from ...kafka.avro import FileSystemAvroSchemaLoader, AvroWireFormatSerializer, AvroOutboxMessageFactory
from ...kafka.redpanda import RedpandaSchemaRegistryClient

from ...config import Config


class KafkaProvider(Provider):

    @provide(scope=Scope.APP)
    def schema_loader(self, config: Config) -> ISchemaLoader:
        app = config.app
        return FileSystemAvroSchemaLoader(base_dir=app.base_dir)

    @provide(scope=Scope.APP)
    def registry_client(self, config: Config) -> ISchemaRegistryClient:
        kafka = config.kafka
        return RedpandaSchemaRegistryClient(base_url=kafka.dsn)

    @provide(scope=Scope.APP)
    def serializer(self) -> IWireFormatSerializer:
        return AvroWireFormatSerializer()

    @provide(scope=Scope.APP)
    def message_factory(self,
                   schema_registry: ISchemaRegistryClient,
                   avro_serializer: IWireFormatSerializer,
                   schema_loader: ISchemaLoader) -> IOutboxMessageFactory:
        return AvroOutboxMessageFactory(schema_registry, avro_serializer, schema_loader)
