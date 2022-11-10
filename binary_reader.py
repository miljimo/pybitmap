import abc
import io
import os
import typing
from abc import ABCMeta


class ReaderBase(metaclass=ABCMeta):
    @abc.abstractmethod
    def read(self) -> typing.Any:
        pass


class BinaryStreamBase(ReaderBase):
    """
    An interface to a binary stream , reading numbers, chracters and floating points
    """

    @abc.abstractmethod
    def read_bytes(self, nbyte: int) -> bytearray:
        pass

    @abc.abstractmethod
    def readint_32(self):
        pass

    @abc.abstractmethod
    def readint_16(self):
        pass

    @abc.abstractmethod
    def readint_8(self):
        pass

    @abc.abstractmethod
    def eof(cls):
        pass

    @abc.abstractmethod
    def size(self) -> int:
        pass

    @property
    @abc.abstractmethod
    def position(self) -> int:
        pass


class BinaryStream(ReaderBase):
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


def create_from_bytes(buffer: bytearray):
    return BinaryStream(io.BytesIO(buffer))


def create_from_file(filename: str) -> BinaryStream:
    """
     create a new binary buffer reader from a filename
    :param filename:
    :return:
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(filename)

    with open(filename, mode="rb") as stream:
        return create_from_bytes(stream.read())
