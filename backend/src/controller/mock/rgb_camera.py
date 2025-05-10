from common.enum import ImageFormat
from controller.mock import MOCK_DATA_DIR
from controller.rgb_camera import RgbCameraController
import os
import random
import shutil


class RgbCameraMockController(RgbCameraController):
    def is_available(self) -> bool:
        return True

    def capture_image(self, quality: int, img_format: ImageFormat):
        path = f"{MOCK_DATA_DIR}/rgb"
        files = os.listdir(path)
        file_extension = img_format.value.lower()

        # filter only photos with correct file extension
        files = [file for file in files if file_extension in file]

        fake_photo = random.choice(files)
        mocked_photo_name = self.generate_name(img_format)
        shutil.copy(os.path.join(path, fake_photo), os.path.join(self.output_dir, mocked_photo_name))

    def __enter__(self) -> RgbCameraController:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
