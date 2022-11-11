import io

from bitmap import Bitmap
from bmp_file_header import BMPFileType


class BMPFileWriter(object):
    def write(self, filename: str, bitmap: Bitmap):
        if bitmap.type != BMPFileType.BM:
            raise TypeError("bitmap file type not supported yet")

        writer = BinaryStreamWriter()
        # write the bitmap header
        writer.write_string(bitmap.type)
        writer.write_int32(bitmap._header.file_size)
        writer.write_int16(bitmap._header.reserved1)
        writer.write_int16(bitmap._header.reserved2)
        writer.write_int32(bitmap._header.start_address)

        #

        pass
