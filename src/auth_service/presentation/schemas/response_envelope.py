from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ResponseEnvelope(BaseModel, Generic[T]):
    status: str
    data: T
    meta: dict | None = None
