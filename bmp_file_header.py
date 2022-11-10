from enum import IntEnum


class BMPFileType(IntEnum):
    BM = 0  # Windows 3.1x, 95, NT, ... etc.
    BA = 1  # OS/2 struct bitmap array
    CI = 2  # OS/2 struct color icon
    CP = 3  # OS/2 const color pointer
    IC = 4  # OS/2 struct icon
    PT = 5  # OS/2 pointer


class BMPFileHeader(object):
    """
    THe file header for every bitmap file.
    this header information are compulsory to every bitmap image out there.
    """

    def __init__(self, ntype: str):
        self.type = ntype
        self.file_size = 0
        self.reserved1 = 0
        self.reserved2 = 0
        self.start_address = 0

    def __repr__(self):
        return "BMPFileHeader(Type={0}, FileSize={1}, Offset={2})".format(
            self.type, self.file_size, self.start_address
        )
