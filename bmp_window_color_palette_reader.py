import io
from bmp_window_info_header import BMPWindowInfoHeader
from binary_stream_reader import BinaryStreamReader, ReaderBase
from bitmap import BMPColorPalette


class BMPWindowColorPaletteReader(ReaderBase):
    def __init__(self, buffer: bytearray, header: BMPWindowInfoHeader):
        if type(buffer) != bytes:
            raise TypeError("@BitmapColorPaletteReader: expecting a bytes array")
        self.__stream = BinaryStreamReader(io.BytesIO(buffer))
        self._header = header

    @property
    def stream(self) -> BinaryStreamReader:
        return self.__stream

    def read(self) -> BMPColorPalette:
        """
        :return:
        """
        color_palette = BMPColorPalette(
            compression=0, width=self._header.width, height=self._header.height
        )
        for _ in range(0, self._header.image_size, 3):
            blue = self.stream.readint_8()
            green = self.stream.readint_8()
            red = self.stream.readint_8()
            color_palette.add_pixel(red, green, blue)

        return color_palette
