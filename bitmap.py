"""
 ~Descriptions
  Write and read a bitmap (Device Independent Bitmap(DIB) file format
"""
from collections import Collection
from bmp_file_header import BMPFileHeader


class Pixel(object):
    def __init__(self, red: int, green: int, blue: int, alpha: int = 1):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
        pass

    def __repr__(self):
        return "Pixel(red={0}, green={1}, blue={2})".format(
            self.red, self.green, self.blue
        )


class BMPColorPalette(object):
    """
    The BITMAPINFOHEADER structure may be followed by an array of palette entries or color masks.
    The rules depend on the value of biCompression.
    """

    def __init__(self, compression: int):
        self.__compression = compression
        self._pixels = list()

    def add_pixel(self, red: int, green: int, blue: int) -> None:
        self._pixels.append(Pixel(red=red, green=green, blue=blue))

    @property
    def length(self) -> int:
        return len(self._pixels)


class Bitmap(object):
    """
    The data structure that hold the bitmap file format.
    Supported Formats
    1) Support for Window Bitmap implemented.
    2)
    """

    def __init__(self, header: BMPFileHeader, color_palette: BMPColorPalette):
        self.bmp_header = header
        self.color_palette = color_palette


if __name__ == "__main__":
    pass
