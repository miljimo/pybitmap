import io

from binary_reader import BinaryStream, ReaderBase
from bmp_file_header import BMPFileHeader


class BMPFileHeaderReader(ReaderBase):
    """
    The class will read only the basic common header
    information common among all bitmap
    which the first section of the bitmap file format.
    """

    def __init__(
        self, buffer: bytearray, header_class_type: BMPFileHeader = BMPFileHeader
    ):
        if type(buffer) != bytes:
            raise TypeError("@BMPFileHeader reader expecting a bytearray parameter")
        self.__stream = BinaryStream(io.BytesIO(buffer))
        self._header_class_type = header_class_type

    @property
    def stream(self) -> BinaryStream:
        return self.__stream

    def read(self) -> BMPFileHeader:
        """
          The function read the first section header of the bitmap image file format.
          into the data structure BMPFileHeader.
        :return:
        """
        header = self._header_class_type(self.stream.read_string(2))
        header.file_size = self.stream.readint_32()
        header.reserved1 = self.stream.readint_16()
        header.reserved2 = self.stream.readint_16()
        header.start_address = self.stream.readint_32()
        return header
