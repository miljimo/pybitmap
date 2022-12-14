import io
import os.path

from bmp_file_reader import BMPWindowColorPaletteReader, BMPWindowInfoHeaderReader
from bmp_file_writer import BMPWindowColorPaletteWriter
from bmp_image import BMPColorDepthType, BMPColorStorage
from constants import ROOT_DIR


def test_bitmap_color_storage():
    storage = BMPColorStorage(300, 400, BMPColorDepthType.BITS_24)


def test_window_bitmap_color_palette_pixels_loaded():
    filename = os.path.join(ROOT_DIR, "tests/fixtures/images/wisdom.bmp")
    with open(filename, mode="rb") as fs:
        buffer = fs.read()
        header_reader = BMPWindowInfoHeaderReader(buffer=buffer)
        header = header_reader.read()
        fs.seek(header.start_address, io.SEEK_SET)

        color_palette_reader = BMPWindowColorPaletteReader(
            fs.read(header.image_size), header=header
        )
        color_palette = color_palette_reader.read()
        expected_number_of_pixels = header.width * header.height
        assert color_palette.length == expected_number_of_pixels


def test_window_write_bitmap_color_palette_pixels():
    writer = BMPWindowColorPaletteWriter()
    width = 400  # in pixel
    height = 500  # in pixel
    color_palette = BMPColorStorage(0, 450, 450)
    nbytes = writer.write(color_palette=color_palette)
    expected_nbytes_size = (width * height) * BMPColorDepthType.BITS_24

    assert nbytes == expected_nbytes_size
