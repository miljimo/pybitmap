import io
import os

from binary_reader import create_from_file, BinaryStream, ReaderBase, BinaryStreamBase
from bmp_file_header import BMPInfoHeader, BMPFileType, BMPFileHeader
from bitmap import Bitmap, Pixel


class BitmapReader(object):
    _MAGIC_CHARACTER_LENGTH = 2

    def __init__(self, filename: str):
        if not os.path.exists(filename):
            raise FileExistsError(filename)
        self._filename = filename
        self._reader = create_from_file(filename)

    def read_magic_character(self) -> str:
        return self._reader.read_string(self._MAGIC_CHARACTER_LENGTH).upper().strip()

    def create_header_information_from(
        self, reader: BinaryStreamBase, bitmap_type: str
    ) -> BMPInfoHeader:
        if bitmap_type == BMPFileType.BM:
            header = BMPInfoHeader()
            header.header_size = reader.readint_32()
            header.width = reader.readint_32()
            header.height = reader.readint_32()
            header.color_planes = reader.readint_16()
            header.bits_per_pixels = reader.readint_16()
            header.compression_type = reader.readint_32()
            header.imgsize = reader.readint_32()
            header.horizontal_resolution = reader.readint_32()
            header.vertical_resolution = reader.readint_32()
            header.color_used = reader.readint_32()
            header.colors_important = reader.readint_32()

            if header.bits_per_pixels == 16:
                # Let read the additional BA information for OS/2 OS22XBIMAPHEADER2
                hvunits = reader.readint_16()
                padding = reader.readint_16()
                direction = reader.readint_16()  # no supported in windows.
                halftoning_algo = reader.readint_16()
                param1 = reader.readint_32()
                param2 = reader.readint_32()
                color_encoding_type = reader.readint_32()  # 0 means RGB
                app_identifier = reader.read_bytes(4)

            return header

    def read_header(self) -> BMPFileHeader:
        bitmap_magic_type = self.read_magic_character()
        if not self.is_valid_type(bitmap_magic_type):
            raise ValueError(
                f"@reader unable to read bitmap file {self._filename}, unknown bitmap type"
            )
        # The header type depends on the bitmap_magic_type
        header = BMPFileHeader(bitmap_magic_type)
        header.file_size = self._reader.readint_32()
        header.reserved1 = self._reader.readint_16()
        header.reserved2 = self._reader.readint_16()
        header.start_address = self._reader.readint_32()
        # Get all the header information bytes
        header.dib_info = self.create_header_information_from(
            BinaryStream(io.BytesIO(self._reader.read_bytes(header.start_address - 1))),
            bitmap_magic_type,
        )
        self._reader.seek(header.start_address)

        return header

    def is_valid_type(self, ntype: str) -> bool:
        ntype = ntype.upper().strip()
        if (ntype == BMPFileType.BM.name) | (ntype == BMPFileType.BA.name):
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
