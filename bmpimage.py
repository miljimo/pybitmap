"""
 ~Descriptions
  Write and read a bitmap (Device Independent Bitmap(DIB) file format
"""
from imaging.image import Image
from imaging.size import Size
from imaging.pixel_array import PixelArray
from bmp_color_palette import BMPPalette
from bmp_window_info_header import BMPWindowInfoHeader


class BMPImage(Image):
    """
    The data structure that hold the bitmap file format.
    Supported Formats
    1) Support for Window Bitmap implemented.
    2)
    """

    def __init__(
        self, header: BMPWindowInfoHeader, pixels: PixelArray = PixelArray(Size(0, 0))
    ):
        self._header = header
        self.__size = Size(self._header.width, self._header.height)
        self.__resolution = Size(
            self._header.horizontal_resolution, self._header.vertical_resolution
        )
        self.__pixels = pixels

    def resolution(self) -> Size:
        return self.__resolution

    @property
    def compression_type(self) -> int:
        return self._header.compression_type

    @property
    def bits_per_pixel(self) -> int:
        return self._header.bits_per_pixels

    @property
    def type(self):
        return self._header.type

    @property
    def size(self) -> Size:
        return self.__size

    @property
    def pixels(self) -> PixelArray:
        return self.__pixels

    def __repr__(self) -> str:
        return "Bitmap(type={0},width={1},height={2}, pixels={3})".format(
            self._header.type, self.size.width, self.size.height, self.pixels.length
        )
