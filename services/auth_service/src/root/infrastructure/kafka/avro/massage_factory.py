from root.domain.events import DomainEvent, UserRegisteredEvent
from root.application.ports import IOutboxMessageFactory
from root.application.schemas.models import OutboxMessage
from ..ports import ISchemaRegistryClient, IWireFormatSerializer, ISchemaLoader
from .message_schemas import v1


class AvroOutboxMessageFactory(IOutboxMessageFactory):
    def __init__(
        self,
        schema_registry: ISchemaRegistryClient,
        avro_serializer: IWireFormatSerializer,
        schema_loader: ISchemaLoader,
    ):
        self._schema_registry = schema_registry
        self._avro_serializer = avro_serializer
        self._schema_loader = schema_loader

    async def _create(self, event: DomainEvent) -> OutboxMessage:
        match event:
            case UserRegisteredEvent():
                 return await v1.create_user_registered(self._schema_loader, self._schema_registry,
                                                        self._avro_serializer, event)
            case _:
                raise ValueError(f"Unsupported event type: {type(event).__name__}")

    async def create_many(self, events):
        result = []
        for event in events:
            result.append(await self._create(event))
        return result
