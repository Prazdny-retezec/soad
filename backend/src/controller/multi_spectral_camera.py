import subprocess
from datetime import datetime
from subprocess import Popen

from common.enum import ImageFormat


class MultiSpectralCameraController:

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self._process: Popen | None = None

    def start_capturing(self, img_format: ImageFormat, width: int, height: int, interval: int, exposure_time: int):
        if self._process is None:
            # TODO použít spíš přímo LabViewController?
            self._process = subprocess.Popen([
                "python", "../../../labview/labview-control/camera-control.py",
                "--image_path", f"{self.output_dir}",
                "--interval", f"{interval}",
                "--exposure_time", f"{exposure_time}",
                "--width", f"{width}",
                "--height", f"{height}"
            ])

    def stop_capturing(self):
        if self._process is not None:
            self._process.kill()

    @staticmethod
    def generate_name(img_format: ImageFormat) -> str:
        return "ms_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%SZ") + "." + img_format.value.lower()
