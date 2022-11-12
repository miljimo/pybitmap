import io
import typing

from binary_streaming.reader import ReaderBase


class BinaryStreamReader(ReaderBase):
    """
    The class is a trait from reading a primitive objects from memory.
    """

    def __init__(self, buffer: io.BytesIO):
        super().__init__()
        self._buffer = buffer
        self._size = self._buffer.seek(0, io.SEEK_END)
        self._buffer.seek(0, io.SEEK_SET)

    def read(self) -> typing.Any:
        return self._buffer.read()

    @property
    def position(self):
        return self._buffer.tell()

    def seek(self, npos: int) -> int:
        return self._buffer.seek(npos, io.SEEK_SET)

    @property
    def size(self) -> int:
        return self._size

    def read_bytes(self, nbyte: int = 1) -> bytearray:
        return self._buffer.read(nbyte)

    def read_string(self, length: int) -> str:
        bytes_array = self.read_bytes(length)
        return bytes_array.decode(encoding="utf-8")

    def readint_32(self) -> int:
        """
         read int32 from stream.
        :param stream:
        :return:
        """
        values = self.read_bytes(4)
        return (
            ((0xFFFFFFFF & values[3]) << 24)
            | ((0xFFFFFFFF & values[2]) << 16)
            | ((0xFFFFFFFF & values[1]) << 8)
            | (0xFFFFFFFF & values[0])
        )

    def readint_16(self) -> int:
        values = self.read_bytes(2)
        return ((0xFFFF & values[1]) << 8) | (0xFFFF & values[0])

    def readint_8(self) -> int:
        return ord(self.read_bytes(1))

    def eof(self) -> bool:
        return self.position >= (self.size - 1)
