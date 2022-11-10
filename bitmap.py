"""
 ~Descriptions
  Write and read a bitmap (Device Independent Bitmap(DIB) file format
"""
from bmp_window_info_header import BMPWindowInfoHeader
from bmp_color_palette import BMPColorPalette


class Bitmap(object):
    """
    The data structure that hold the bitmap file format.
    Supported Formats
    1) Support for Window Bitmap implemented.
    2)
    """

    def __init__(self, header: BMPWindowInfoHeader, color_palette: BMPColorPalette):
        self._header = header
        self._color_palette = color_palette

    @property
    def type(self):
        return self._header.type

    @property
    def width(self) -> int:
        return self._header.width

    @property
    def height(self) -> int:
        return self._header.height

    @property
    def color_palette(self) -> BMPColorPalette:
        return self._color_palette

    def __repr__(self) -> str:
        return "Bitmap(type={0},width={1},height={2}, pixels={3})".format(
            self._header.type, self.width, self.height, self._color_palette.length
        )
