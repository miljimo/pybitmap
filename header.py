from enum import IntEnum


class BitmapType(IntEnum):
    BM = 0  # Windows 3.1x, 95, NT, ... etc.
    BA = 1  # OS/2 struct bitmap array
    CI = 2  # OS/2 struct color icon
    CP = 3  # OS/2 const color pointer
    IC = 4  # OS/2 struct icon
    PT = 5  # OS/2 pointer


class BitmapCompressionType(IntEnum):
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


class DIBHeader(object):
    def __init__(self):
        pass

    @property
    def is_compressed(self) -> bool:
        return False


class BitmapInfoHeader(DIBHeader):
    def __init__(self):
        self.header_size = 0
        self.width = 0
        self.height = 0
        self.color_planes = 0
        self.bits_per_pixels = 0
        # Fields added for Windows 3.x follow this line (BMP Version 3 (Microsoft Windows 3.x)) */
        self.compression_type = 0  # 0 indicates that the data is uncompressed;
        self.imgsize = 0
        # pixel per metre
        self.horizontal_resolution = 0
        self.vertical_resolution = 0
        self._color_used = 0
        self.colors_important = 0

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
        return self.compression_type != 0


class BMPFileHeader(object):
    def __init__(self, ntype: str):
        self.type = ntype
        self.file_size = 0
        # Reserved; actual value depends on the application that creates the image, if created manually can be 0
        self.reserved1 = 0
        # Reserved; actual value depends on the application that creates the image, if created manually can be 0
        self.reserved2 = 0
        # The offset in bits from the begining of the file i.e.
        # the starting address, of the byte where the bitmap image data (pixel array) can be found.
        self.start_address = 0

        # Additional information that described the BMP Image.
        self.dib_info = BitmapInfoHeader()

    def __repr__(self):
        return "BMPFileHeader(Type={0}, FileSize={1}, Offset={2})".format(
            self.type, self.file_size, self.start_address
        )
