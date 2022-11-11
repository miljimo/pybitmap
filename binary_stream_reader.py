import abc
import io
import os
import typing
from abc import ABCMeta


class ReaderBase(metaclass=ABCMeta):
    @abc.abstractmethod
    def read(self) -> typing.Any:
        pass


class WriterBase(metaclass=ABCMeta):
    @abc.abstractmethod
    def write(self, data: typing.Any) -> typing.Any:
        pass


class BinaryStreamReader(ReaderBase):
    def __init__(self, buffer: io.BytesIO):
        super().__init__()
        self._buffer = buffer
        self._size = self._buffer.seek(0, io.SEEK_END)
        self._buffer.seek(0, io.SEEK_SET)

    @property
    def position(self):
        return self._buffer.tell()

    def read(self) -> typing.Any:
        return self._buffer.read()

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


class BinaryStreamWriter(object):

    """
    The class is used to write objects into memory.
    """

    def __init__(self):
        self.__buffer = io.BytesIO()

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
