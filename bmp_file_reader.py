import io
import os
from bitmap import Bitmap
from binary_stream_reader import ReaderBase
from bmp_window_info_header import BMPColorDepthType, BMPCompressionType
from bmp_window_info_header_reader import BMPWindowInfoHeaderReader
from bmp_window_color_palette_reader import BMPWindowColorPaletteReader

BMP_FILE_HEADER_BYTE_SIZE = 12


class BMPFileReader(ReaderBase):
    def __init__(self, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)
        self.__filename = filename

    @property
    def filename(self) -> str:
        return self.__filename

    def read(self) -> Bitmap:

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

            # move the cursor to the start address of the color palette
            fs.seek(header.start_address, io.SEEK_SET)
            color_palette = BMPWindowColorPaletteReader(
                fs.read(header.image_size), header=header
            ).read()
            return Bitmap(header=header, color_palette=color_palette)
