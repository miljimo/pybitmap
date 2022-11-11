from bmp_file_header_reader import BMPFileHeaderReader, BMPFileHeaderWriter
from bmp_window_info_header import BMPCompressionType, BMPWindowInfoHeader


class BMPWindowInfoHeaderReader(BMPFileHeaderReader):

    """
    The class is used to read the window bitmap image file header
    alongside the information sections of the header.

    """

    def __init__(
        self,
        buffer: bytearray,
        header_class_type: BMPWindowInfoHeader = BMPWindowInfoHeader,
    ):
        super().__init__(buffer, header_class_type=header_class_type)

    def read(self) -> BMPWindowInfoHeader:
        header: BMPWindowInfoHeader = super().read()
        header.size = self.stream.readint_32()
        header.width = self.stream.readint_32()
        header.height = self.stream.readint_32()
        header.color_planes = self.stream.readint_16()
        # The color depth , this should be
        header.bits_per_pixels = self.stream.readint_16()
        header.compression_type = self.stream.readint_32()
        header.image_size = self.stream.readint_32()
        header.horizontal_resolution = self.stream.readint_32()
        header.vertical_resolution = self.stream.readint_32()
        header.color_used = self.stream.readint_32()
        header.colors_important = self.stream.readint_32()

        """
        # Still trying to understand this part.
        The BITMAPINFOHEADER structure may be followed by an array of palette entries or color masks. 
        The rules depend on the value of biCompression.
        """
        if header.compression_type == BMPCompressionType.BI_BITFIELDS:
            """
            The bitmap uses three DWORD color masks (red, green, and blue, respectively),
            which specify the byte layout of the pixels.
            The 1 bits in each mask indicate the bits for that color within the pixel.
            """
            pass
        if header.compression_type == BMPCompressionType.BI_ALPHABITFIELDS:

            pass
        return header


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
