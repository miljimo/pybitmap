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
        color_palette_reader = BMPWindowColorPaletteReader(
            color_palette_buffer, width=header.width, height=header.height
        )
        color_palette = color_palette_reader.read()
        print(color_palette.length)
        print(f"Width : {header.width}")
        print(f"Height : {header.height}")
        print(f"Height Cal : {int(color_palette.length  / header.width) -1 }")

        print((header.bits_per_pixels * header.width * 3) / 24)

        for row in range(header.height):
            for column in range(header.width):
                pixel = color_palette.at(row, column)
            print(f"\nROW = {row}")
