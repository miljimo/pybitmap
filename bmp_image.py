"""
 ~Descriptions
  Write and read a bitmap (Device Independent Bitmap(DIB) file format
"""
import io
from enum import IntEnum

from imaging.image import Image
from imaging.pixel_array import PixelArray
from imaging.size import Size


NO_COMPRESSION = 0
BYTE_SIZE_IN_BITS = 8


class BMPFileType(IntEnum):
    BM = 0  # Windows 3.1x, 95, NT, ... etc.
    BA = 1  # OS/2 struct bitmap array
    CI = 2  # OS/2 struct color icon
    CP = 3  # OS/2 const color pointer
    IC = 4  # OS/2 struct icon
    PT = 5  # OS/2 pointer


class BMPCompressionType(IntEnum):
    """
    Bitmap compression types
    """

    BI_RGB = 0  # BI_RGB is the most common, means that the data is not compressed.
    BI_RLE8 = 1  # Can be used only with 8-bit/pixel bitmaps
    BI_RLE4 = 2  # Can be used only with 4-bit/pixel bitmaps
    BI_BITFIELDS = (
        3  # BITMAPV2INFOHEADER: RGB bit field masks, BITMAPV3INFOHEADER+: RGBA
    )
    BI_JPEG = 4  # BITMAPV4INFOHEADER+: JPEG image for printing[1
    BI_PNG = 5  # BITMAPV4INFOHEADER+: PNG image for printing[
    BI_ALPHABITFIELDS = 6  # only Windows CE 5.0 with .NET 4.0 or later
    BI_CMYK = 11  # only Windows Metafile CMYK[4]
    BI_CMYKRLE8 = 12
    BI_CMYKRLE4 = 13


class HalftoningAlgorithmType(IntEnum):
    COMMON = 0
    ERROR_DIFFUSION = 1
    PANDA = 2
    SUPER_CIRCLE = 3


class BMPColorDepthType:
    """
    The colour depths of the pixel bitmap images
    RGB = 24 , meaning 8bits per each colour.
    """

    BITS_32 = 32
    BITS_24 = 24
    BITS_16 = 16
    BITS_8 = 8
    BITS_4 = 4
    BITS_1 = 1


class BMPFileHeader(object):
    """
    THe file header for every bitmap file.
    this header information are compulsory to every bitmap image out there.
    """

    def __init__(self, ntype: str):
        self.type = ntype
        self.file_size = 0
        self.reserved1 = 0
        self.reserved2 = 0
        self.start_address = 0

    def __repr__(self):
        return "BMPFileHeader(Type={0}, FileSize={1}, Offset={2})".format(
            self.type, self.file_size, self.start_address
        )


class BMPWindowInfoHeader(BMPFileHeader):
    """
    A data structure that will hold the window bitmap image file information
    details. The structure provides more information about the file you re loading
    into memory.
    """

    def __init__(self, bitmap_type: str):
        super().__init__(bitmap_type)
        self.size = 0
        self.width = 0
        self.height = 0
        self.color_planes = 0
        self.bits_per_pixels = 0
        self.compression_type = 0
        self.image_size = 0
        self.horizontal_resolution = 0
        self.vertical_resolution = 0
        self._color_used = 0
        self.colors_important = 0
        self.is_extended = False

    @property
    def color_used(self):
        return self._color_used

    @color_used.setter
    def color_used(self, nused: int):
        if nused == 0:
            # default it to 1 << bits_per_pixels
            self._color_used = 1 << self.bits_per_pixels
            return
        self._color_used = nused

    @property
    def is_compressed(self) -> bool:
        return self.compression_type != NO_COMPRESSION


class BMPColorStorage(object):
    """
    The most straightforward way of storing a bitmap is simply to list the bitmap information,
    byte after byte, row by row. Files stored by this method are often called RAW files.
    The amount of disk storage required for any bitmap is easy to calculate given the bitmap dimensions (N x M) and
    colour depth in bits (B). The formula for the file size in KBytes is
    """

    def __init__(self, width: int, height: int, bits_per_pixel: int = 24):
        self.__width = width
        self.__height = height
        self.__bits_per_pixel = bits_per_pixel
        self.__size = int(
            (self.__width * self.__height * self.__bits_per_pixel) / BYTE_SIZE_IN_BITS
        )
        self.__buffer = io.BytesIO(bytearray([0x00] * self.__size))
        self.__offset = int(bits_per_pixel / BYTE_SIZE_IN_BITS)

    @property
    def size(self) -> int:
        """
          return the disk size in bytes colors in the bitmap image
        :return:
        """
        return self.__size

    @property
    def data(self) -> bytes:
        self.__buffer.seek(0, io.SEEK_SET)
        return self.__buffer.read()


    def insert(self, row_index:int , red:int , green:int , blue:int) -> bool:
        """
          Insert the pixel colors into the given palette rows
        :param row_index:
        :param red:
        :param green:
        :param blue:
        :return:
        """
        pass


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


class BMPImage(Image):
    """
    The data structure that hold the bitmap file format.
    Supported Formats
    1) Support for Window Bitmap implemented.
    2)
    """

    def __init__(
        self, header: BMPWindowInfoHeader, pixels: PixelArray = PixelArray(Size(0, 0))
    ):
        self._header = header
        self.__size = Size(self._header.width, self._header.height)
        self.__resolution = Size(
            self._header.horizontal_resolution, self._header.vertical_resolution
        )
        self.__pixels = pixels

    def resolution(self) -> Size:
        return self.__resolution

    @property
    def compression_type(self) -> int:
        return self._header.compression_type

    @property
    def bits_per_pixel(self) -> int:
        return self._header.bits_per_pixels

    @property
    def type(self):
        return self._header.type

    @property
    def size(self) -> Size:
        return self.__size

    @property
    def pixels(self) -> PixelArray:
        return self.__pixels

    def __repr__(self) -> str:
        return "Bitmap(type={0},width={1},height={2}, pixels={3})".format(
            self._header.type, self.size.width, self.size.height, self.pixels.length
        )