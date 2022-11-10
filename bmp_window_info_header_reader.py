from bmp_file_header_reader import BMPFileHeaderReader
from bmp_window_info_header import BMPWindowInfoHeader


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
        header.bits_per_pixels = self.stream.readint_16()
        header.compression_type = self.stream.readint_32()
        header.imgsize = self.stream.readint_32()
        header.horizontal_resolution = self.stream.readint_32()
        header.vertical_resolution = self.stream.readint_32()
        header.color_used = self.stream.readint_32()
        header.colors_important = self.stream.readint_32()

        # This header comes with different types base on the bits_per_pixels,compression_type
        return header
