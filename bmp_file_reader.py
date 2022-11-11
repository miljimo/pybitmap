import io
import os

from binary_stream_reader import ReaderBase, WriterBase, BinaryStreamWriter
from bmpimage import BMPImage
from bmp_file_header import BMPFileType
from bmp_window_color_palette_reader import BMPWindowColorPaletteReader
from bmp_window_info_header import BMPColorDepthType, BMPCompressionType
from bmp_window_info_header_reader import (
    BMPWindowInfoHeaderReader,
    BMPWindowInfoHeaderWriter,
)
from bmp_window_color_palette_reader import BMPWindowColorPaletteWriter

BMP_FILE_HEADER_BYTE_SIZE = 12


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


class BMPFileWriter(WriterBase):
    def write(self, filename: str, bitmap: BMPImage):
        if bitmap.type != BMPFileType.BM:
            raise TypeError("bitmap file type not supported yet")

        writer = BMPWindowInfoHeaderWriter()
        writer.write(bitmap._header)
        content_writer = BMPWindowColorPaletteWriter()
        content_writer.write(bitmap.pixels)

        # save the content.
        with open(filename, mode="wb") as fs:
            fs.write(writer.stream.get_bytes())
            fs.write(content_writer.stream.get_bytes())
