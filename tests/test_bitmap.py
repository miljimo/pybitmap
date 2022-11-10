import io
import os
from pathlib import Path

import pytest

import constants
from binary_reader import BinaryStream, create_from_bytes, create_from_file
from bitmap_reader import BitmapReader


@pytest.fixture(scope="session")
def filename():
    return Path(
        os.path.join(constants.ROOT_DIR, "tests/fixtures/images/dock.bmp")
    ).absolute()


def test_read_int32_from_stream():
    expected = 50
    reader = create_from_bytes(b"\x32\x00\x00\x00")
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
