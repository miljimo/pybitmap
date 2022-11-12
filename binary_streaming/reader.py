import abc
import typing


class ReaderBase(metaclass=abc.ABCMeta):
    """
    A base file from reading all the binary contents
    """

    @abc.abstractmethod
    def read(self) -> typing.Any:
        pass
