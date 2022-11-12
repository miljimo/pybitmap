import io

from binary_streaming.writer import WriterBase


class BinaryStreamWriter(WriterBase):
    """
    The class is used to write objects into memory.
    """

    def __init__(self):
        self.__buffer = io.BytesIO()

    def seek(self, npos: int) -> int:
        self.__buffer.seek(0, io.SEEK_SET)

    def write_string(self, value: str) -> int:
        return self.__buffer.write(value.encode(encoding="utf"))

    def write_int32(self, value: int) -> None:
        # using little intial
        buffer = bytearray()
        buffer.append((value >> 24) & 0xFF)
        buffer.append((value >> 16) & 0xFF)
        buffer.append((value >> 8) & 0xFF)
        buffer.append(value & 0xFF)
        return self.__buffer.write(buffer)

    def write_int16(self, value: int) -> int:
        buffer = bytearray()
        buffer.append((value >> 8) & 0xFF)
        buffer.append(value & 0xFF)
        return self.__buffer.write(buffer)

    def write_int8(self, value: int) -> int:
        value = 0xFF & value
        return self.__buffer.write(value)

    @property
    def position(self) -> int:
        return self.__buffer.tell()

    @property
    def get_bytes(self) -> bytes:
        return self.__buffer.read()
