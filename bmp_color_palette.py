from imaging.pixel_array import PixelArray
from imaging.size import Size


class BMPPalette(object):
    """
    The BITMAPINFOHEADER structure may be followed by an array of palette entries or color masks.
    The rules depend on the value of biCompression.
    """

    def __init__(
        self, width: int, height: int, buffer: bytes, bits_per_pixel: int = 24
    ):
        self.__width = width
        self.__height = height
        self.__palettes = buffer
        self.__bits_per_pixel = bits_per_pixel

    @property
    def data(self) -> bytes:
        return self.__palettes

    def decode_pixels(self) -> PixelArray:
        """
         The function will decode the pixels data in the color panel
         and return a list of the expected image pixel.
         this part is not yet understand by me .
        :return:
        """
        pixels = PixelArray(Size(self.__width, self.__height))
        # Still don't understand it yet.
        stride = (((self.__width * self.__bits_per_pixel) + 31) & ~31) >> 3

        for index in range(0, len(self.data), 3):
            blue = self.data[index]
            green = self.data[index + 1]
            red = self.data[index + 2]
            pixels.add_pixel(red, green, blue)
        return pixels
