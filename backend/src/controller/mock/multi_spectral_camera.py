import os
import random
import shutil
import time

from common.enum import ImageFormat
from controller.mock import MOCK_DATA_DIR
from controller.multi_spectral_camera import MultiSpectralCameraController


class MultiSpectralCameraMockController(MultiSpectralCameraController):

    def start_capturing(self, img_format: ImageFormat, width: int, height: int, interval: int, exposure_time: int):
        # mock exposure
        time.sleep(exposure_time)

        path = f"{MOCK_DATA_DIR}/ms"
        files = os.listdir(path)
        file_extension = img_format.value.lower()

        # filter only photos with correct file extension
        files = [file for file in files if file_extension in file]

        fake_photo = random.choice(files)
        mocked_photo_name = self.generate_name(img_format)
        shutil.copy(os.path.join(path, fake_photo), os.path.join(self.output_dir, mocked_photo_name))

    def stop_capturing(self):
        pass
