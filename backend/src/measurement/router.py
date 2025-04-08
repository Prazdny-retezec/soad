from typing import List
from fastapi import APIRouter, status, Depends

from measurement.dto import MeasurementCreateDto, MeasurementUpdateDto, MeasurementListDto, MeasurementDetailDto
from measurement.service import MeasurementService

router = APIRouter(
    prefix="/measurement",
    tags=["Measurement"],
)


@router.get("")
async def list_measurements(
        service: MeasurementService = Depends(MeasurementService)
) -> List[MeasurementListDto]:
    return service.list_measurements()


@router.get("/{id}")
async def get_measurement(
        id: int,
        service: MeasurementService = Depends(MeasurementService)
) -> MeasurementDetailDto:
    return service.get_measurement(id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_measurement(
        dto: MeasurementCreateDto,
        service: MeasurementService = Depends(MeasurementService)
) -> MeasurementListDto:
    return service.create_measurement(dto)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_measurement(
        id: int,
        dto: MeasurementUpdateDto,
        service: MeasurementService = Depends(MeasurementService)
) -> MeasurementListDto:
    return service.update_measurement(id, dto)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_measurement(id, service: MeasurementService = Depends(MeasurementService)):
    service.delete_measurement(id)

# TODO exception handling (handle errors that are thrown in service layer)
#  see https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers
