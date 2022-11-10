from enum import IntEnum

from bmp_file_header import BMPFileHeader

NO_COMPRESSION_NEEDED = 0


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


class ColorDepth:
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
        return self.compression_type != NO_COMPRESSION_NEEDED
