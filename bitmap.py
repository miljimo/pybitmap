"""
 ~Descriptions
  Write and read a bitmap (Device Independent Bitmap(DIB) file format
"""

import abc
from enum import IntEnum


class BitmapType(IntEnum):
    BM = 0  # Windows 3.1x, 95, NT, ... etc.
    BA = 1  # OS/2 struct bitmap array
    CI = 2  # OS/2 struct color icon
    CP = 3  # OS/2 const color pointer
    IC = 4  # OS/2 struct icon
    PT = 5  # OS/2 pointer


class BitmapCompressionType(IntEnum):
    """
    Bitmap compression types
    """

    BI_RGB = 0  # Most common
    BI_RLE8 = 1  # Can be used only with 8-bit/pixel bitmaps
    BI_RLE4 = 2  # Can be used only with 4-bit/pixel bitmaps
    BI_BITFIELDS = (
        3  # BITMAPV2INFOHEADER: RGB bit field masks, BITMAPV3INFOHEADER+: RGBA
    )
    BI_JPEG = 4  # BITMAPV4INFOHEADER+: JPEG image for printing[1
    BI_PNG = 5  # BITMAPV4INFOHEADER+: PNG image for printing[
    BI_ALPHABITFIELDS = 6  # only Windows CE 5.0 with .NET 4.0 or later
    BI_CMYK = 11  # only Windows Metafile CMYK[4]
    BI_CMYKRLE8 = 12
    BI_CMYKRLE4 = 13


class Pixel(object):
    def __init__(self, red: int, green: int, blue: int, alpha: int):
        pass


class PixelArray(abc.ABCMeta):
    pass


class DIBHeader(object):
    def __init__(self):
        pass


class BitmapInfoHeader(DIBHeader):
    def __init__(self):
        self.header_size = 0
        self.width = 0
        self.height = 0
        self.color_planes = 0
        self.bits_per_pixels = 0
        self.compression_type = 0
        self.imgsize = 0
        # pixel per metre
        self.horizontal_resolution = 0
        self.vertical_resolution = 0
        self.number_of_color_palette = 0
        self.number_of_important_colors = 0


class BMPFileHeader(object):
    def __init__(self, magic: str):
        self.magic = magic
        self.file_size = 0
        # Reserved; actual value depends on the application that creates the image, if created manually can be 0
        self.reserved1 = 0
        # Reserved; actual value depends on the application that creates the image, if created manually can be 0
        self.reserved2 = 0
        # The offset, i.e. starting address, of the byte where the bitmap image data (pixel array) can be found.
        self.start_address = 0
        self.dib_info = None


class Bitmap(object):
    def __init__(self, header: BMPFileHeader):
        self.header = header
        pass


if __name__ == "__main__":
    pass
