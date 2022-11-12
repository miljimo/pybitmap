import abc

from imaging.pixel import Pixel
from imaging.size import Size


class PixelArray(metaclass=abc.ABCMeta):
    """
    A collection that hold image pixels and helper functions to manipulated and access them.
    """

    def __init__(self, size: Size, pixels: list = []):
        self.__pixels = pixels
        self.__size = size

    def add_pixel(self, red: int, green: int, blue: int) -> None:
        self.__pixels.append(Pixel(red=red, green=green, blue=blue))

    @property
    def length(self) -> int:
        return len(self.__pixels)

    def at(self, row_index: int, column_index: int):
        index = (row_index * self.__size.width) + column_index
        if index >= self.length:
            raise IndexError(f"row = {row_index}, column={column_index}")
        return self.__pixels[index]

    def __len__(self) -> int:
        return self.length
