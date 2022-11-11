import abc
from imaging.size import Size


class Pixel(metaclass=abc.ABCMeta):
    pass


class PixelArray(metaclass=abc.ABCMeta):
    def at(self, row_index: int, column_index: int) -> Pixel:
        pass


class Image(metaclass=abc.ABCMeta):
    """
    @Description
         The class is the base interface for all visual representation of an object,
         such as a body part or celestial body, for the purpose
         of medical diagnosis or data collection, using any of a variety of techniques, such as
         ultrasonography or spectroscopy.
    """

    @property
    @abc.abstractmethod
    def size(self) -> Size:
        pass

    @property
    @abc.abstractmethod
    def pixels(self) -> PixelArray:
        pass
