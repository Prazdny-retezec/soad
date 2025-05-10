import logging
import os
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    database_url: str = os.environ.get("DATABASE_URL")
    secret: str = os.environ.get("SECRET")
    output_dir: str = os.environ.get("OUTPUT_DIR")
    mock_ae: bool = Field(default=False, alias="MOCK_ACOUSTIC_EMISSION")
    mock_rgb: bool = Field(default=False, alias="MOCK_RGB_CAMERA")
    mock_msc: bool = Field(default=False, alias="MOCK_MULTI_SPECTRAL_CAMERA")

    # load settings from .env file
    model_config = SettingsConfigDict(env_file=".env")

    def __init__(self, **values: Any):
        super().__init__(**values)

        if self.mock_ae:
            logging.warn("App is using mock data for AcousticEmissionController")

        if self.mock_rgb:
            logging.warn("App is using mock data for RgbCameraController")

        if self.mock_msc:
            logging.warn("App is using mock data for MultiSpectralCameraController")
