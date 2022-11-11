"""
 ~Descriptions
  Write and read a bitmap (Device Independent Bitmap(DIB) file format
"""
from imaging.image import Image
from imaging.size import Size
from bmp_color_palette import BMPColorPalette
from bmp_window_info_header import BMPWindowInfoHeader


class BMPImage(Image):
    """
    The data structure that hold the bitmap file format.
    Supported Formats
    1) Support for Window Bitmap implemented.
    2)
    """

    def __init__(self, header: BMPWindowInfoHeader, color_palette: BMPColorPalette):
        self._header = header
        self._color_palette = color_palette
        self._size = Size(self._header.width, self._header.height)

    @property
    def type(self):
        return self._header.type

    @property
    def size(self) -> Size:
        return self._size

    @property
    def pixels(self) -> BMPColorPalette:
        return self._color_palette

    def __repr__(self) -> str:
        return "Bitmap(type={0},width={1},height={2}, pixels={3})".format(
            self._header.type, self.width, self.height, self._color_palette.length
        )
