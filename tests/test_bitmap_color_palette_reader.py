import io

from bmp_window_color_palette_reader import BMPWindowColorPaletteReader
from bmp_window_info_header_reader import BMPWindowInfoHeaderReader


def test_window_bitmap_color_palette_loaded():
    filename = "./fixtures/images/wisdom.bmp"
    with open(filename, mode="rb") as fs:
        buffer = fs.read()
        header_reader = BMPWindowInfoHeaderReader(buffer=buffer)
        header = header_reader.read()
        fs.seek(header.start_address, io.SEEK_SET)
        # read the color palette data from the images
        color_palette_buffer = fs.read(header.image_size)
        color_palette_reader = BMPWindowColorPaletteReader(color_palette_buffer)
        color_palette = color_palette_reader.read()
