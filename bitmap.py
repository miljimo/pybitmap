"""
 ~Descriptions
  Write and read a bitmap (Device Independent Bitmap(DIB) file format
"""
from bmp_file_header import BMPFileHeader


class ColorPalette(object):
    """ """

    pass


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


class PixelArray(object):
    def __init__(self):
        self._pixels = list()

    def append(self, pixel: Pixel):
        self._pixels.append(pixel)

    @property
    def length(self):
        return len(self._pixels)


class Bitmap(object):
    """
    The data structure that hold the bitmap file format.

    """

    def __init__(self, header: BMPFileHeader):
        self.bmp_header = header
        self.pixels = PixelArray()

    def pixels(self) -> PixelArray:
        pass


if __name__ == "__main__":
    pass
