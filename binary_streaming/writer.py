import abc
import typing


class WriterBase(metaclass=abc.ABCMeta):
    """
    The base class template or traits for reading all the binary object from memory or file.
    """

    @abc.abstractmethod
    def write(self, data: typing.Any) -> typing.Any:
        pass
