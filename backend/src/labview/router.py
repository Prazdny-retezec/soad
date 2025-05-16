from fastapi import APIRouter, Depends

from controller.multi_spectral_camera import MultiSpectralCameraController
from controllers import get_ms_camera_controller

router = APIRouter(
    prefix="/labview",
    tags=["LabVIEW"],
)


@router.get(
    path="/should-capture-photo",
    summary="Příznak focení MS kamerou",
    description="Návratová hodnota z endpointu říká, jestli má LabVIEW uložit MS fotku nebo ne. Vrací se 0 nebo 1."
)
async def should_capture_image(controller: MultiSpectralCameraController = Depends(get_ms_camera_controller)) -> int:
    return int(controller.should_capture_photo)


@router.get(
    path="/photo-path",
    summary="Absolutní cesta MS fotky",
    description="Endpoint oznamuje LabVIEW kam má ukládat MS fotku pomocí absolutní cesty."
)
async def get_photo_path(controller: MultiSpectralCameraController = Depends(get_ms_camera_controller)) -> str:
    return controller.get_full_image_name()
