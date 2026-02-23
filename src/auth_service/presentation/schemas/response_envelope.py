from pydantic import BaseModel


class ResponseEnvelope[T](BaseModel):
    status: str
    data: T
    meta: dict | None = None
