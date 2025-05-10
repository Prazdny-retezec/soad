from pydantic import BaseModel

from common.enum import ImageFormat
from sensor.model import SensorSettings


class SensorSettingsDto(BaseModel):
    # rgb camera
    rgb_image_quality: int = 90
    rgb_image_count: int = 5
    rgb_image_width: int = 1920
    rgb_image_height: int = 1080
    rgb_sampling_delay: int = 2
    rgb_image_format: ImageFormat = ImageFormat.TIFF

    # multi-spectral camera
    ms_image_count: int = 2
    ms_image_width: int = 1920
    ms_image_height: int = 1080
    ms_sampling_delay: int = 5
    ms_image_format: ImageFormat = ImageFormat.TIFF

    # acoustic emission
    ae_voltage_format: int = 5
    ae_voltage_dbae: int = 1
    ae_counts_log: int = 1
    ae_counts_lin: int = 1
    ae_energy_format: int = 1

    def to_entity(self) -> SensorSettings:
        return SensorSettings(
            rgb_image_quality=self.rgb_image_quality,
            rgb_image_count=self.rgb_image_count,
            rgb_image_width=self.rgb_image_width,
            rgb_image_height=self.rgb_image_height,
            rgb_sampling_delay=self.rgb_sampling_delay,
            rgb_image_format=ImageFormat[self.rgb_image_format],

            ms_image_count=self.ms_image_count,
            ms_image_width=self.ms_image_width,
            ms_image_height=self.ms_image_height,
            ms_sampling_delay=self.ms_sampling_delay,
            ms_image_format=ImageFormat[self.ms_image_format],

            ae_voltage_format=self.ae_voltage_format,
            ae_voltage_dbae=self.ae_voltage_dbae,
            ae_counts_log=self.ae_counts_log,
            ae_counts_lin=self.ae_counts_lin,
            ae_energy_format=self.ae_energy_format,
        )
