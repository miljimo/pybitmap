import io
import os
import constants
import pytest
from pathlib import Path

from bitmap_reader import BinaryStream, BitmapReader


@pytest.fixture(scope="session")
def filename():
    return Path(
        os.path.join(constants.ROOT_DIR, "tests/fixtures/images/dock.bmp")
    ).absolute()


def test_read_int32_from_stream():
    buffer = io.BytesIO(b"\x32\x00\x00\x00")
    expected = 50
    reader = BinaryStream(buffer)
    actual = reader.readint_32()
    assert actual == expected


def test_number_of_colour_used_matches_bitmap_header(filename):
    reader = BitmapReader(filename=filename)
    header = reader.read_header()
    expected_color_used = 16777216
    actual = 1 << header.dib_info.bits_per_pixels
    assert expected_color_used == actual


def test_bitmap_image_reader(filename):
    reader = BitmapReader(filename=filename)
    bitmap = reader.read()
    print(bitmap)
