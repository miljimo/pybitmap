import io

from bmp_window_color_palette_reader import BMPWindowColorPaletteReader
from bmp_window_info_header_reader import BMPWindowInfoHeaderReader


def test_window_bitmap_color_palette_pixels_loaded():
    filename = "./fixtures/images/wisdom.bmp"
    with open(filename, mode="rb") as fs:
        buffer = fs.read()
        header_reader = BMPWindowInfoHeaderReader(buffer=buffer)
        header = header_reader.read()
        fs.seek(header.start_address, io.SEEK_SET)
        color_palette_buffer = fs.read(header.image_size)
        color_palette_reader = BMPWindowColorPaletteReader(
            color_palette_buffer, width=header.width, height=header.height
        )
        color_palette = color_palette_reader.read()
        expected_number_of_pixels = header.width * header.height
        assert color_palette.length == expected_number_of_pixels