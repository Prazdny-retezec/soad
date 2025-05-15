import os
from datetime import datetime

from common.enum import ImageFormat


class MultiSpectralCameraController:

    def __init__(self, output_dir: str, exposure_time: int):
        self.output_dir = output_dir
        self.exposure_time = exposure_time
        self.should_capture_photo = False
        self._img_format = ImageFormat.PNG

    def start_capturing(self):
        self.should_capture_photo = True

    def stop_capturing(self):
        self.should_capture_photo = False

    def get_full_image_name(self):
        return os.path.join(self.output_dir, self._generate_name())

    def _generate_name(self) -> str:
        return "ms_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%SZ") + "." + self._img_format.value.lower()
