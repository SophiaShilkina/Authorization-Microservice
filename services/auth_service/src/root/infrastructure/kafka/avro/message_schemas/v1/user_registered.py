from datetime import timezone

from root.domain.events import UserRegisteredEvent
from root.application.schemas.models import OutboxMessage
from ....ports import ISchemaLoader, ISchemaRegistryClient, IWireFormatSerializer


async def create_user_registered(
        schema_loader: ISchemaLoader,
        schema_registry: ISchemaRegistryClient,
        avro_serializer: IWireFormatSerializer,
        event: UserRegisteredEvent,
) -> OutboxMessage:
    schemas = await schema_loader.load_and_cache('v1', 'auth.user.registered.v1')

    occurred_at_millis = int(event.occurred_at.astimezone(timezone.utc).timestamp() * 1000)

    envelope = {
        "event_id": str(event.event_id),
        "event_type": "auth.user.registered",
        "schema_version": 1,
        "occurred_at": occurred_at_millis,
        "correlation_id": None,
        "causation_id": None,
        "payload": {
            "user_id": str(event.user_id),
            "email": event.email,
            "registered_at": occurred_at_millis,
        },
    }

    subject = "outbox.event.auth.user.registered.v1-value"
    schema_id = await schema_registry.get_or_register(
        subject=subject,
        schema_str=schemas.raw_json,
    )

    payload_bytes = avro_serializer.serialize(
        schema_id=schema_id,
        schema_dict=schemas.parsed,
        payload=envelope,
    )

    return OutboxMessage(
        id=event.event_id,
        aggregate_type="user",
        aggregate_id=str(event.user_id),
        event_type="auth.user.registered",
        payload=payload_bytes,
        occurred_at=event.occurred_at,
    )
