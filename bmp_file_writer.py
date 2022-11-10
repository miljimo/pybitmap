import io
from bitmap import Bitmap
from bmp_file_header import BMPFileType


class BinaryStreamWriter(object):
    def __init__(self):
        self.__buffer = io.BytesIO()

    def write_string(self, value: str) -> int:
        return self.__buffer.write(value.encode(encoding="utf"))


class BMPFileWriter(object):
    def write(self, filename: str, bitmap: Bitmap):
        if bitmap.type != BMPFileType.BM:
            raise TypeError("bitmap file type not supported yet")

        writer = BinaryStreamWriter()
        # write the bitmap header
        writer.write_string(bitmap.type)


        pass