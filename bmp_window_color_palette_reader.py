import io
from bmp_window_info_header import BMPCompressionType
from binary_reader import BinaryStream, ReaderBase
from bitmap import BMPColorPalette


class BMPWindowColorPaletteReader(ReaderBase):
    def __init__(self, buffer: bytearray):
        if type(buffer) != bytes:
            raise TypeError("@BitmapColorPaletteReader: expecting a bytes array")
        self.__stream = BinaryStream(io.BytesIO(buffer))
        self._size = len(buffer)

    @property
    def stream(self) -> BinaryStream:
        return self.__stream

    def read(self) -> BMPColorPalette:
        """
        :return:
        """
        color_palette = BMPColorPalette(compression=0)
        ncounter = 0
        for _ in range(0, self._size, 3):
            blue = self.stream.readint_8()
            green = self.stream.readint_8()
            red = self.stream.readint_8()
            color_palette.add_pixel(red, green, blue)

        return color_palette
