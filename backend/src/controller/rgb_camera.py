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
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        return camera is not None

    def capture_image(self, output_dir: str, quality: int, img_format: ImageFormat):
        if not self.is_available():
            raise RuntimeError("Unable to capture image - camera is not available")

        # check directory and create one if it does not exist
        filename = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
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

            if img_format == ImageFormat.PNG:
                filename = f"{output_dir}/{filename}_%d.png"
                image.Save(pylon.ImageFileFormat_Png, filename)
            elif img_format == ImageFormat.RAW:
                filename = f"{output_dir}/{filename}_%d.raw"
                image.Save(pylon.ImageFileFormat_Raw, filename)
            elif img_format == ImageFormat.TIFF:
                filename = f"{output_dir}/{filename}_%d.tiff"
                image.Save(pylon.ImageFileFormat_Tiff, filename)
            else:
                logging.warn("Invalid image format used")

            image.Release()
        self.device.StopGrabbing()

    def __enter__(self):
        tlf = pylon.TlFactory.GetInstance()
        self.device = pylon.InstantCamera(tlf.CreateFirstDevice())

        if self.device is None:
            raise RuntimeError('No RgbCamera device found')

        self.device.Open()
        self.device.Width.Value = self.width
        self.device.Height.Value = self.height

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.device is not None:
            self.device.Close()
            self.device = None
