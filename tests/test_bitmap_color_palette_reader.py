import io
import os.path

from constants import ROOT_DIR
from bmp_window_info_header import BMPColorDepthType
from bmp_color_palette import BMPPalette
from bmp_window_color_palette_reader import (
    BMPWindowColorPaletteReader,
    BMPWindowColorPaletteWriter,
)
from bmp_window_info_header_reader import BMPWindowInfoHeaderReader


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
    color_palette = BMPPalette(0, 450, 450)
    nbytes = writer.write(color_palette=color_palette)
    expected_nbytes_size = (width * height) * BMPColorDepthType.BITS_24

    assert nbytes == expected_nbytes_size
