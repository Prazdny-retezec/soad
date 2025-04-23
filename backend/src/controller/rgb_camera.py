import logging
import os
from datetime import datetime

from common.enum import ImageFormat
from pypylon import pylon


class RgbCameraController:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.device: pylon.InstantCamera | None = None

    def is_available(self) -> bool:
        return self.device is not None

    def capture_image(self, output_dir: str, quality: int, img_format: ImageFormat):
        logging.debug("Capturing started")

        if not self.is_available():
            raise RuntimeError("Unable to capture image - camera is not available")

        # check directory and create one if it does not exist
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # setup config for image capturing
        image = pylon.PylonImage()
        ipo = pylon.ImagePersistenceOptions()
        ipo.SetQuality(quality)

        # grab image
        self.device.StartGrabbing()
        with self.device.RetrieveResult(2000) as result:
            image.AttachGrabResultBuffer(result)

            # create filename
            filename = output_dir + "/" + self.generate_name(img_format)

            # check if target format is supported and if so save the image to disk
            if img_format == ImageFormat.PNG:
                image.Save(pylon.ImageFileFormat_Png, filename)
            elif img_format == ImageFormat.RAW:
                image.Save(pylon.ImageFileFormat_Raw, filename)
            elif img_format == ImageFormat.TIFF:
                image.Save(pylon.ImageFileFormat_Tiff, filename)
            else:
                logging.warn("Invalid image format used")

            image.Release()
        self.device.StopGrabbing()

        logging.debug("Capturing ended")

    def __enter__(self):
        tlf = pylon.TlFactory.GetInstance()
        self.device = pylon.InstantCamera(tlf.CreateFirstDevice())

        if self.device is None:
            raise RuntimeError('No RgbCamera device found')

        self.device.Open()
        self.device.Width.Value = self.width
        self.device.Height.Value = self.height

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.device is not None:
            self.device.Close()
            self.device = None

    @staticmethod
    def generate_name(img_format: ImageFormat) -> str:
        return "rgb_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%SZ") + "." + img_format.value.lower()
