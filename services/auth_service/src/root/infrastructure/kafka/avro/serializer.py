import io
import struct

from fastavro import parse_schema, schemaless_writer

from ..ports import IWireFormatSerializer


class AvroWireFormatSerializer(IWireFormatSerializer):
    MAGIC_BYTE = 0

    def serialize(self, schema_id: int, schema_dict: dict, payload: dict) -> bytes:
        parsed_schema = parse_schema(schema_dict)

        buffer = io.BytesIO()
        buffer.write(struct.pack(">bI", self.MAGIC_BYTE, schema_id))
        schemaless_writer(buffer, parsed_schema, payload)
        return buffer.getvalue()
