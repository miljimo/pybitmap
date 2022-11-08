import io
import os
from enum import IntEnum

from bitmap import Bitmap, BitmapInfoHeader, BitmapType, BMPFileHeader


class BinaryStream(object):
    def __init__(self, buffer: io.BytesIO):
        self._buffer = buffer

    def readint_32(self) -> int:
        """
         read int32 from stream.
        :param stream:
        :return:
        """
        values = self._buffer.read(4)
        return (
            ((0xFFFFFFFF & values[3]) << 24)
            | ((0xFFFFFFFF & values[2]) << 16)
            | ((0xFFFFFFFF & values[1]) << 8)
            | (0xFFFFFFFF & values[0])
        )

    def readint_16(self) -> int:

        values = self._buffer.read(2)
        return ((0xFFFF & values[1]) << 8) | (0xFFFF & values[0])


class BitmapReader(object):
    _MAGIC_CHARACTER_LENGTH = 2

    def __init__(self, filename: str):
        if not os.path.exists(filename):
            raise FileExistsError(filename)
        self._filename = filename

    def read_magic_character(self, stream: io.BytesIO) -> str:
        return (
            stream.read(self._MAGIC_CHARACTER_LENGTH).decode(encoding="utf-8").upper()
        )

    def read_bitmap_header(
        self, reader: BinaryStream, bitmap_magic_type: str
    ) -> BMPFileHeader:
        header = BMPFileHeader(bitmap_magic_type)
        header.file_size = reader.readint_32()
        header.reserved1 = reader.readint_16()
        header.reserved2 = reader.readint_16()
        header.start_address = reader.readint_32()

        if (header.magic == BitmapType.BM.name) or header.magic == BitmapType.BA.name:
            # reading DIB header (bitmap information header) for  Windows BITMAPINFOHEADER
            header.dib_info = BitmapInfoHeader()
            header.dib_info.header_size = reader.readint_32()
            header.dib_info.width = reader.readint_32()
            header.dib_info.height = reader.readint_32()
            header.dib_info.color_planes = reader.readint_16()
            header.dib_info.bits_per_pixels = reader.readint_16()
            header.dib_info.compression_type = reader.readint_32()
            header.dib_info.imgsize = reader.readint_32()
            header.dib_info.horizontal_resolution = reader.readint_32()
            header.dib_info.vertical_resolution = reader.readint_32()
            header.dib_info.number_of_color_palette = reader.readint_32()
            header.dib_info.number_of_important_colors = reader.readint_32()

            if header.magic == BitmapType.BA.name:
                # Let read the additional BA information
                pass

        return header

    def is_valid_bitmap_type(self, ntype: str) -> bool:
        ntype = ntype.upper().strip()
        if (ntype == BitmapType.BM.name) | (ntype == BitmapType.BA.name):
            # Current support bitmap types
            return True
        return False

    def read(self) -> Bitmap:
        """
         The function will the bitmap file into memory and return
         a Bitmap object
        :return:
        """
        bitmap = None

        with open(self._filename, mode="rb") as stream:
            size = stream.seek(0, io.SEEK_END)
            stream.seek(0, io.SEEK_SET)
            bitmap_type = self.read_magic_character(stream)

            if not self.is_valid_bitmap_type(bitmap_type):
                raise ValueError(f"not a bitmap file {self._filename}")
            reader = BinaryStream(stream)
            header = self.read_bitmap_header(reader, bitmap_type)
            print(f"Compression Type= {header.dib_info.compression_type}")
            print(f"Bits per Pixel = {header.dib_info.bits_per_pixels}")
            print(f"Image Size = {header.dib_info.imgsize}")
            # read the pixel_array from the bitmap stream
            stream.seek(header.start_address, io.SEEK_SET)

            bitmap = Bitmap(header=header)

        return bitmap
