import io
import os
from binary_reader import ReaderBase, BinaryStreamBase, BinaryStream
from bmp_file_header import BMPInfoHeader, BMPFileType, BMPFileHeader


class BMPInfoHeaderReader(ReaderBase):
    """
    Namespace for the bitmap image file header reader.
    The bitmap file have multi-file headers base on versions.
    """

    class __BMPInfoHeaderReader(ReaderBase):
        """
        The bitmap information header reader, reads the
        """

        def __init__(self, reader: BinaryStreamBase):
            self._reader = reader

        def read(self) -> BMPInfoHeader:

            header = BMPInfoHeader()
            header.header_size = self._reader.readint_32()
            header.width = self._reader.readint_32()
            header.height = self._reader.readint_32()
            header.color_planes = self._reader.readint_16()
            header.bits_per_pixels = self._reader.readint_16()
            header.compression_type = self._reader.readint_32()
            header.imgsize = self._reader.readint_32()
            header.horizontal_resolution = self._reader.readint_32()
            header.vertical_resolution = self._reader.readint_32()
            header.color_used = self._reader.readint_32()
            header.colors_important = self._reader.readint_32()

            if self.has_os22_header(header):
                # Let read the additional BA information for OS/2 OS22XBIMAPHEADER2
                hvunits = self._reader.readint_16()
                padding = self._reader.readint_16()
                direction = self._reader.readint_16()  # no supported in windows.
                halftoning_algo = self._reader.readint_16()
                param1 = self._reader.readint_32()
                param2 = self._reader.readint_32()
                color_encoding_type = self._reader.readint_32()  # 0 means RGB
                app_identifier = self._reader.read_bytes(4)
            return header

        def has_os22_header(self, header: BMPFileHeader) -> bool:
            return False

    @staticmethod
    def from_file(filename: str) -> __BMPInfoHeaderReader:
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)
        with open(filename, mode="rb") as fs:
            return BMPInfoHeaderReader.from_bytes(fs.read())

    @staticmethod
    def from_bytes(buffer: bytearray) -> __BMPInfoHeaderReader:
        return BMPInfoHeaderReader.__BMPInfoHeaderReader(
            BinaryStream(io.BytesIO(buffer))
        )
