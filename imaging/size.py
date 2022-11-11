import abc


class Size(metaclass=abc.ABCMeta):
    """
    A size is the width X height
    """

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    def __repr__(self):
        return "Size(Width={0},Height={1})".format(self.width, self.height)
