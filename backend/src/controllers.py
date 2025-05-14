import logging

from controller.acoustic_emission import AcousticEmissionController
from controller.mock.acoustic_emission import AcousticEmissionMockController
from controller.mock.multi_spectral_camera import MultiSpectralCameraMockController
from controller.mock.rgb_camera import RgbCameraMockController
from controller.multi_spectral_camera import MultiSpectralCameraController
from controller.rgb_camera import RgbCameraController
from settings import AppSettings

settings = AppSettings()


def get_acoustic_emission_controller() -> AcousticEmissionController:
    if settings.mock_ae:
        logging.warn("App is using mock data for AcousticEmissionController")
        return AcousticEmissionMockController(settings.ae_ip_address, settings.ae_port, settings.output_dir)

    return AcousticEmissionController(settings.ae_ip_address, settings.ae_port, settings.output_dir)


def get_rgb_camera_controller(width: int, height: int) -> RgbCameraController:
    if settings.mock_rgb:
        logging.warn("App is using mock data for RgbCameraController")
        return RgbCameraMockController(settings.output_dir, width, height)

    return RgbCameraController(settings.output_dir, width, height)


def get_ms_camera_controller() -> MultiSpectralCameraController:
    if settings.mock_rgb:
        logging.warn("App is using mock data for MultiSpectralCameraController")
        return MultiSpectralCameraMockController(settings.output_dir)

    return MultiSpectralCameraController(settings.output_dir)
