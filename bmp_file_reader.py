import io
import os

from binary_streaming.memory_reader import BinaryStreamReader
from binary_streaming.reader import ReaderBase
from bmp_image import (
    BMPImage,
    BMPColorStorage,
    BMPFileHeader,
    BMPWindowInfoHeader,
    BMPCompressionType,
    BMPColorDepthType,
)

BMP_FILE_HEADER_BYTE_SIZE = 12


class BMPFileHeaderReader(ReaderBase):
    """
    The class will read only the basic common header
    information common among all bitmap
    which the first section of the bitmap file format.
    """

    def __init__(
        self, buffer: bytearray, header_class_type: BMPFileHeader = BMPFileHeader
    ):
        if type(buffer) != bytes:
            raise TypeError("@BMPFileHeader reader expecting a bytearray parameter")
        self.__stream = BinaryStreamReader(io.BytesIO(buffer))
        self._header_class_type = header_class_type

    @property
    def stream(self) -> BinaryStreamReader:
        return self.__stream

    def read(self) -> BMPFileHeader:
        """
          The function read the first section header of the bitmap image file format.
          into the data structure BMPFileHeader.
        :return:
        """
        header = self._header_class_type(self.stream.read_string(2))
        header.file_size = self.stream.readint_32()
        header.reserved1 = self.stream.readint_16()
        header.reserved2 = self.stream.readint_16()
        header.start_address = self.stream.readint_32()
        return header


class BMPWindowInfoHeaderReader(BMPFileHeaderReader):

    """
    The class is used to read the window bitmap image file header
    alongside the information sections of the header.

    """

    def __init__(
        self,
        buffer: bytearray,
        header_class_type: BMPWindowInfoHeader = BMPWindowInfoHeader,
    ):
        super().__init__(buffer, header_class_type=header_class_type)

    def read(self) -> BMPWindowInfoHeader:
        header: BMPWindowInfoHeader = super().read()
        header.size = self.stream.readint_32()
        header.width = self.stream.readint_32()
        header.height = self.stream.readint_32()
        header.color_planes = self.stream.readint_16()
        # The color depth , this should be
        header.bits_per_pixels = self.stream.readint_16()
        header.compression_type = self.stream.readint_32()
        header.image_size = self.stream.readint_32()
        header.horizontal_resolution = self.stream.readint_32()
        header.vertical_resolution = self.stream.readint_32()
        header.color_used = self.stream.readint_32()
        header.colors_important = self.stream.readint_32()

        """
        # Still trying to understand this part.
        The BITMAPINFOHEADER structure may be followed by an array of palette entries or color masks. 
        The rules depend on the value of biCompression.
        """
        if header.compression_type == BMPCompressionType.BI_BITFIELDS:
            """
            The bitmap uses three DWORD color masks (red, green, and blue, respectively),
            which specify the byte layout of the pixels.
            The 1 bits in each mask indicate the bits for that color within the pixel.
            """
            pass
        if header.compression_type == BMPCompressionType.BI_ALPHABITFIELDS:

            pass
        return header


class BMPWindowColorPaletteReader(ReaderBase):
    def __init__(self, buffer: bytearray, header: BMPWindowInfoHeader):
        if type(buffer) != bytes:
            raise TypeError("@BitmapColorPaletteReader: expecting a bytes array")
        self.__stream = BinaryStreamReader(io.BytesIO(buffer))
        self._header = header

    @property
    def stream(self) -> BinaryStreamReader:
        return self.__stream

    def read(self) -> BMPColorStorage:
        """
        :return:
        """
        color_palette = BMPColorStorage(
            width=self._header.width,
            height=self._header.height,
            buffer=self.stream.read(),
        )


class BMPFileReader(ReaderBase):
    def __init__(self, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)
        self.__filename = filename

    @property
    def filename(self) -> str:
        return self.__filename

    def read(self) -> BMPImage:

        with open(self.filename, mode="rb") as fs:
            # Read the file header information, to check if the file is a valid bitmap file.
            bmp_buffer = fs.read()
            header = BMPWindowInfoHeaderReader(bmp_buffer).read()
            if header.compression_type != BMPCompressionType.BI_RGB:
                raise TypeError(
                    "at the moment the bitmap compression type not implemented"
                )
            if header.bits_per_pixels != BMPColorDepthType.BITS_24:
                raise TypeError("unsupported color depth bitmap detected.")

            fs.seek(header.start_address, io.SEEK_SET)
            color_palette = BMPWindowColorPaletteReader(
                fs.read(header.image_size), header=header
            ).read()
            return BMPImage(header=header, pixels=color_palette.decode_pixels())
