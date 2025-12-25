from pydantic import BaseModel


class FastapiConfig(BaseModel):
    host: str
    port: int
