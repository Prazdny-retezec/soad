from datetime import datetime

from common.enum import ImageFormat


class MultiSpectralCameraController:

    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def start_capturing(self, img_format: ImageFormat, width: int, height: int, interval: int, exposure_time: int):
        pass

    def stop_capturing(self):
        pass

    @staticmethod
    def generate_name(img_format: ImageFormat) -> str:
        return "ms_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%SZ") + "." + img_format.value.lower()
