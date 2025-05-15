import logging

from controller.acoustic_emission import AcousticEmissionController
from controller.mock.acoustic_emission import AcousticEmissionMockController
from controller.mock.multi_spectral_camera import MultiSpectralCameraMockController
from controller.mock.rgb_camera import RgbCameraMockController
from controller.multi_spectral_camera import MultiSpectralCameraController
from controller.rgb_camera import RgbCameraController
from settings import AppSettings

settings = AppSettings()

rgb_camera_controller = None
ms_camera_controller = None
acoustic_emission_controller = None


def get_rgb_camera_controller() -> RgbCameraController:
    return rgb_camera_controller


def get_ms_camera_controller() -> MultiSpectralCameraController:
    return ms_camera_controller


def get_acoustic_emission_controller() -> AcousticEmissionController:
    return acoustic_emission_controller


# RGB camera
if settings.mock_rgb:
    logging.warn("App is using mock data for RgbCameraController")
    rgb_camera_controller = RgbCameraMockController(settings.output_dir)
else:
    rgb_camera_controller = RgbCameraController(settings.output_dir)

# Acoustic emission
if settings.mock_ae:
    logging.warn("App is using mock data for AcousticEmissionController")
    acoustic_emission_controller = AcousticEmissionMockController(
        ip_address=settings.ae_ip_address,
        port=settings.ae_port,
        output_dir=settings.output_dir
    )
else:
    acoustic_emission_controller = AcousticEmissionController(
        ip_address=settings.ae_ip_address,
        port=settings.ae_port,
        output_dir=settings.output_dir
    )

# Multispectral camera
if settings.mock_msc:
    logging.warn("App is using mock data for MultiSpectralCameraController")
    ms_camera_controller = MultiSpectralCameraMockController(settings.output_dir, settings.msc_exposure_time)
else:
    ms_camera_controller = MultiSpectralCameraController(settings.output_dir, settings.msc_exposure_time)
