from binary_streaming.memory_writer import BinaryStreamWriter
from binary_streaming.writer import WriterBase
from bmp_image import BMPFileHeader, BMPFileType, BMPImage, BMPWindowInfoHeader
from imaging.pixel_array import PixelArray


class BMPFileHeaderWriter(WriterBase):
    """
    The class will be used to write back the BMPFileHeader
    back to the byte stream.
    """

    def __init__(self):
        self.__stream = BinaryStreamWriter()

    @property
    def stream(self) -> BinaryStreamWriter:
        return self.__stream

    def write(self, header: BMPFileHeader) -> int:
        self.stream.seek(0)
        self.stream.write_string(header.type)
        self.stream.write_int32(header.file_size)
        self.stream.write_int16(header.reserved1)
        self.stream.write_int16(header.reserved2)
        self.stream.write_int32(header.start_address)
        return self.stream.position


class BMPWindowInfoHeaderWriter(BMPFileHeaderWriter):

    """
    The class will be used to write back the BMP file information to a bytes stream.
    """

    def __init__(self):
        super().__init__()

    def write(self, header: BMPWindowInfoHeader) -> int:
        super().write(header)
        self.stream.write_int32(header.size)
        self.stream.write_int32(header.width)
        self.stream.write_int32(header.height)
        self.stream.write_int16(header.color_planes)
        self.stream.write_int16(header.bits_per_pixels)
        self.stream.write_int32(header.compression_type)
        self.stream.write_int32(header.image_size)
        self.stream.write_int32(header.horizontal_resolution)
        self.stream.write_int32(header.vertical_resolution)
        self.stream.write_int32(header.color_used)
        self.stream.write_int32(header.colors_important)
        return self.stream.position


class BMPWindowColorPaletteWriter(WriterBase):
    def __init__(self):
        self.__stream = BinaryStreamWriter()

    @property
    def stream(self) -> BinaryStreamWriter:
        return self.__stream

    def write(self, pixels: PixelArray) -> int:
        for pixel in pixels:
            # RGB -> BGR
            self.__stream.write_int8(pixel.blue)
            self.__stream.write_int8(pixel.green)
            self.__stream.write_int8(pixel.red)


class BMPFileWriter(WriterBase):
    def write(self, filename: str, bitmap: BMPImage):
        if bitmap.type != BMPFileType.BM.name:
            raise TypeError("bitmap file type not supported yet")

        writer = BMPWindowInfoHeaderWriter()
        writer.write(bitmap._header)
        content_writer = BMPWindowColorPaletteWriter()
        content_writer.write(bitmap.pixels)

        # save the content.
        with open(filename, mode="wb") as fs:
            fs.write(writer.stream.get_bytes())
            fs.write(content_writer.stream.get_bytes())
