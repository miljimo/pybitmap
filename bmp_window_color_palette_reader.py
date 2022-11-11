import io
from imaging.pixel_array import PixelArray
from binary_stream_reader import (
    BinaryStreamReader,
    ReaderBase,
    WriterBase,
    BinaryStreamWriter,
)
from bmpimage import BMPPalette
from bmp_window_info_header import BMPWindowInfoHeader


class BMPWindowColorPaletteReader(ReaderBase):
    def __init__(self, buffer: bytearray, header: BMPWindowInfoHeader):
        if type(buffer) != bytes:
            raise TypeError("@BitmapColorPaletteReader: expecting a bytes array")
        self.__stream = BinaryStreamReader(io.BytesIO(buffer))
        self._header = header

    @property
    def stream(self) -> BinaryStreamReader:
        return self.__stream

    def read(self) -> BMPPalette:
        """
        :return:
        """
        color_palette = BMPPalette(
            width=self._header.width,
            height=self._header.height,
            buffer=self.stream.read(),
        )


class BMPWindowColorPaletteWriter(WriterBase):
    def __init__(self):
        self.__stream = BinaryStreamWriter()

    @property
    def stream(self) -> BinaryStreamWriter:
        return self.__stream

    def write(self, pixels: PixelArray) -> int:
        for pixel in pixels:
            # RGB -> BGR
            self.__stream.write_int8(pixel.blue)
            self.__stream.write_int8(pixel.green)
            self.__stream.write_int8(pixel.red)
