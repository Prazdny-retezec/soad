from enum import StrEnum


class ImageFormat(StrEnum):
    BMP = "BMP"  # TODO unsupported by RGB Camera
    JPEG = "JPEG"  # TODO unsupported by RGB Camera
    TIFF = "TIFF"
    PNG = "PNG"
    RAW = "RAW"
