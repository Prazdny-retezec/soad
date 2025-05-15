import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    database_url: str = os.environ.get("DATABASE_URL")
    secret: str = os.environ.get("SECRET")
    gdrive_credentials_dir: str = os.environ.get("GDRIVE_CREDENTIALS_DIR")
    output_dir: str = os.environ.get("OUTPUT_DIR")
    ae_ip_address: str = os.environ.get("AE_IP_ADDRESS")
    ae_port: int = os.environ.get("AE_PORT")
    msc_exposure_time: int = os.environ.get("MSC_EXPOSURE_TIME")
    mock_data_dir: str = os.environ.get("MOCK_DATA_DIR")
    mock_ae: bool = Field(default=False, alias="MOCK_ACOUSTIC_EMISSION")
    mock_rgb: bool = Field(default=False, alias="MOCK_RGB_CAMERA")
    mock_msc: bool = Field(default=False, alias="MOCK_MULTI_SPECTRAL_CAMERA")

    # load settings from .env file
    model_config = SettingsConfigDict(env_file=".env")