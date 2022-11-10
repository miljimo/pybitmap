import io
import os
from bmp_file_reader import BMPFileReader


def test_bitmap_image_load_from_file():
    filename = "./fixtures/images/dock.bmp"
    reader = BMPFileReader(filename=filename)
    bitmap = reader.read()
    print(bitmap)
