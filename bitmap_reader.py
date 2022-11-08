import io
import os
from header import BitmapInfoHeader, BitmapType, BMPFileHeader
from bitmap import Bitmap, Pixel


class BinaryStream(object):
    def __init__(self, buffer: io.BytesIO):
        self._buffer = buffer
        self._size = self._buffer.seek(0, io.SEEK_END)
        self._buffer.seek(0, io.SEEK_SET)

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


class BitmapReader(object):
    _MAGIC_CHARACTER_LENGTH = 2

    def __init__(self, filename: str):
        if not os.path.exists(filename):
            raise FileExistsError(filename)
        self._filename = filename
        with open(self._filename, mode="rb") as stream:
            buffer = io.BytesIO(stream.read())
            self._reader = BinaryStream(buffer)

    def read_magic_character(self) -> str:
        return self._reader.read_string(self._MAGIC_CHARACTER_LENGTH).upper().strip()

    def read_header(self) -> BMPFileHeader:
        bitmap_magic_type = self.read_magic_character()
        if not self.is_valid_type(bitmap_magic_type):
            raise ValueError(
                f"@reader unable to read bitmap file {self._filename}, unknown bitmap type"
            )
        header = BMPFileHeader(bitmap_magic_type)
        header.file_size = self._reader.readint_32()
        header.reserved1 = self._reader.readint_16()
        header.reserved2 = self._reader.readint_16()
        header.start_address = self._reader.readint_32()

        if (header.type == BitmapType.BM.name) or header.type == BitmapType.BA.name:
            # reading DIB header (bitmap information header) for  Windows BITMAPINFOHEADER
            header.dib_info = BitmapInfoHeader()
            header.dib_info.header_size = self._reader.readint_32()
            header.dib_info.width = self._reader.readint_32()
            header.dib_info.height = self._reader.readint_32()
            header.dib_info.color_planes = self._reader.readint_16()
            header.dib_info.bits_per_pixels = self._reader.readint_16()
            header.dib_info.compression_type = self._reader.readint_32()
            header.dib_info.imgsize = self._reader.readint_32()
            header.dib_info.horizontal_resolution = self._reader.readint_32()
            header.dib_info.vertical_resolution = self._reader.readint_32()
            header.dib_info.color_used = self._reader.readint_32()
            header.dib_info.colors_important = self._reader.readint_32()

            if header.type == BitmapType.BA.name:
                # Let read the additional BA information for OS/2 OS22XBIMAPHEADER2
                hvunits = self._reader.readint_16()
                padding = self._reader.readint_16()
                direction = self._reader.readint_16()  # no supported in windows.
                halftoning_algo = self._reader.readint_16()
                param1 = self._reader.readint_32()
                param2 = self._reader.readint_32()
                color_encoding_type = self._reader.readint_32()  # 0 means RGB
                app_identifier = self._reader.read_bytes(4)

                pass

        return header

    def is_valid_type(self, ntype: str) -> bool:
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

        header = self.read_header()
        # The Color Palette , is the colours ranges use in the bitmap image.

        self._reader.seek(header.start_address)
        bitmap = Bitmap(header=header)
        with open("../bin/data.txt", mode="w+") as file:
            while not self._reader.eof():
                if header.dib_info.bits_per_pixels == 24:
                    """
                    The format for 24bit BMP Image Colour orders.
                    """
                    blue = self._reader.readint_8()
                    green = self._reader.readint_8()
                    red = self._reader.readint_8()
                    pixel = Pixel(red=red, blue=blue, green=green)
                    bitmap.pixels.append(pixel)
                    file.write(str(pixel))
                    file.write("\n")
            file.write("Total = {0}".format(bitmap.pixels.length))
        return bitmap
