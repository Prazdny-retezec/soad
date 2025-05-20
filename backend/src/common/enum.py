from enum import StrEnum, Enum


class ImageFormat(StrEnum):
    BMP = "BMP"  # TODO unsupported by RGB Camera
    JPEG = "JPEG"  # TODO unsupported by RGB Camera
    TIFF = "TIFF"
    PNG = "PNG"
    RAW = "RAW"

class OrderDir(str, Enum):
    asc = "asc"
    desc = "desc"