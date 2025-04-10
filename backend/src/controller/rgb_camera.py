from common.enum import ImageFormat


class RgbCameraController:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def connect(self):
        pass

    def is_available(self) -> bool:
        pass

    def capture_image(self, output_dir: str, quality: int, format: ImageFormat):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
