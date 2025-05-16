import os
import random
import shutil

from controller.multi_spectral_camera import MultiSpectralCameraController
from settings import AppSettings


class MultiSpectralCameraMockController(MultiSpectralCameraController):

    def start_capturing(self):
        super()

        path = os.path.join(AppSettings().mock_data_dir, "ms")
        files = os.listdir(path)
        file_extension = self._img_format.value.lower()

        # filter only photos with correct file extension
        files = [file for file in files if file_extension in file]

        fake_photo = random.choice(files)
        mocked_photo_name = self.get_full_image_name()
        shutil.copy(os.path.join(path, fake_photo), os.path.join(self.output_dir, mocked_photo_name))
