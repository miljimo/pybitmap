import os
from bmp_file_header_reader import BMPFileHeaderReader
from bmp_window_info_header_reader import BMPWindowInfoHeaderReader
from bmp_file_header import BMPFileType


def test_bitmap_header_reader_from_file_success_loaded():
    # Window bmp file start_address , mostly when it's created with paint
    # should all start address for pixel at 54.
    filenames = [
        "./fixtures/images/dock.bmp",
        "./fixtures/images/wisdom.bmp",
        "./fixtures/images/javascript.bmp",
    ]
    expected_start_address = 54
    for filename in filenames:
        with open(filename, mode="rb") as fs:
            print(f"\ntesting filename : {filename}")
            buffer = fs.read()
            reader = BMPFileHeaderReader(buffer=buffer)
            header = reader.read()
            assert header.file_size == len(buffer)
            assert header.start_address == expected_start_address
            assert header.type == BMPFileType.BM.name
            assert header.reserved2 == 0
            assert header.reserved1 == 0


def test_window_bitmap_info_header_success_loaded():
    filename = "./fixtures/images/wisdom.bmp"
    expected_width = 359
    expected_height = 550
    expected_start_address = 54
    expected_image_bits = 24  # meaning RGB image
    expected_standard_header_size_for_window_bitmap = 40
    expected_color_used = 16777216  # this basically pow(2,expected_image_bits)
    expected_vertical_resolution = 7087
    expected_horizontal_resolution = 7087
    expected_image_size = 594000
    with open(filename, mode="rb") as fs:
        buffer = fs.read()
        reader = BMPWindowInfoHeaderReader(buffer=buffer)
        header = reader.read()
        assert header.file_size == len(buffer)
        assert header.start_address == expected_start_address
        assert header.type == BMPFileType.BM.name
        assert header.reserved2 == 0
        assert header.reserved1 == 0
        # Information assert
        assert header.size == expected_standard_header_size_for_window_bitmap
        assert header.bits_per_pixels == expected_image_bits
        assert header.color_used == expected_color_used
        assert header.compression_type == 0  # common compression is no compression
        assert header.colors_important == 0
        assert header.height == expected_height
        assert header.width == expected_width
        assert header.vertical_resolution == expected_vertical_resolution
        assert header.horizontal_resolution == expected_horizontal_resolution
        assert header.imgsize == expected_image_size
