from imaging.pixel import Pixel


class BMPColorPalette(object):
    """
    The BITMAPINFOHEADER structure may be followed by an array of palette entries or color masks.
    The rules depend on the value of biCompression.
    """

    def __init__(self, compression: int, width: int, height: int):
        self.__compression = compression
        self._pixels = list()
        self._width = width
        self._height = height

    def add_pixel(self, red: int, green: int, blue: int) -> None:
        self._pixels.append(Pixel(red=red, green=green, blue=blue))

    @property
    def length(self) -> int:
        return len(self._pixels)

    def at(self, row_index: int, column_index: int):
        index = (row_index * self._width) + column_index
        if index >= self.length:
            raise IndexError(f"row = {row_index}, column={column_index}")
        return self._pixels[index]
