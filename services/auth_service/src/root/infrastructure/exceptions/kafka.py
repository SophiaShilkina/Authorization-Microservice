from .base import InfrastructureError


class KafkaError(InfrastructureError):
    pass


class KafkaConsumerError(KafkaError):
    pass


class SchemaNotFoundError(KafkaError, FileNotFoundError):
    pass
