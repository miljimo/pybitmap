import io
import os

import pytest

from bitmap_reader import BinaryStream, BitmapReader


@pytest.fixture(scope="session")
def filename():
    return os.path.join("./", "data/images/dock.bmp")


def test_read_int32_from_stream():
    buffer = io.BytesIO(b"\x32\x00\x00\x00")
    expected = 50
    reader = BinaryStream(buffer)
    actual = reader.readint_32()
    assert actual == expected


def test_read_bitmap_header(filename):
    if not os.path.exists(filename):
        raise FileExistsError(filename)
    reader = BitmapReader(filename=filename)
    bitmap = reader.read()

    assert bitmap.header.start_address == 54
