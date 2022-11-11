import io
import os
from constants import ROOT_DIR
from bmp_file_reader import BMPFileReader
from bmp_file_writer import BMPFileWriter


def test_bitmap_image_load_from_file():
    filename = os.path.realpath(
        os.path.join(ROOT_DIR, "tests/fixtures/images/dock.bmp")
    )
    reader = BMPFileReader(filename=filename)
    bitmap = reader.read()
    print(bitmap.size)
    assert bitmap is not None


def test_bitmap_image_writer_can_write_bmp_images():
    filename = os.path.realpath(
        os.path.join(ROOT_DIR, "tests/fixtures/images/dock.bmp")
    )
    reader = BMPFileReader(filename=filename)
    bitmap = reader.read()
    writer = BMPFileWriter()
    status = writer.write("../bin/dock_img.bmp", bitmap)
    assert status is True
