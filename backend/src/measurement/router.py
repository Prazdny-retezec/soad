from typing import List
from fastapi import APIRouter, status, Depends

from measurement.dto import MeasurementCreateDto, MeasurementUpdateDto, MeasurementListDto, MeasurementDetailDto, \
    MeasurementCreatePeriodicDto, MeasurementPlanDto
from measurement.service import MeasurementService

router = APIRouter(
    prefix="/measurement",
    tags=["Measurement"],
)


@router.get("",
    summary="Získat seznam měření",
    description="Vrací seznam všech uložených měření."
            )
async def list_measurements(
        service: MeasurementService = Depends(MeasurementService)
) -> List[MeasurementListDto]:
    return service.list_measurements()


@router.get("/{id}",
    summary="Získat detail měření",
    description="Vrací detailní informace o měření podle zadaného ID."
            )
async def get_measurement(
        id: int,
        service: MeasurementService = Depends(MeasurementService)
) -> MeasurementDetailDto:
    return service.get_measurement(id)


@router.post("", status_code=status.HTTP_201_CREATED,
    summary="Vytvořit nové měření",
    description="Vytvoří nové měření na základě vstupních dat a vrátí jeho přehled."
             )
async def create_measurement(
        dto: MeasurementCreateDto,
        service: MeasurementService = Depends(MeasurementService)
) -> MeasurementListDto:
    return service.create_measurement(dto)


@router.post("/periodic", status_code=status.HTTP_201_CREATED,
    summary="Vytvořit periodická měření",
    description="Na základě vstupních dat vytvoří více měření v pravidelných intervalech."
             )
async def create_periodic_measurement(
        dto: MeasurementCreatePeriodicDto,
        service: MeasurementService = Depends(MeasurementService)
) -> list[MeasurementListDto]:
    return service.create_periodic_measurement(dto)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED,
    summary="Aktualizovat měření",
    description="Upraví existující měření podle ID a dodaných aktualizačních dat."
            )
async def update_measurement(
        id: int,
        dto: MeasurementUpdateDto,
        service: MeasurementService = Depends(MeasurementService)
) -> MeasurementListDto:
    return service.update_measurement(id, dto)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,
    summary="Smazat měření",
    description="Smaže měření se zadaným ID."
               )
async def delete_measurement(id: int, service: MeasurementService = Depends(MeasurementService)):
    service.delete_measurement(id)


@router.post("/{id}/plan", status_code=status.HTTP_200_OK,
    summary="Naplánovat měření",
    description="Naplánuje měření na zvolený čas s volitelnou odchylkou."
             )
async def plan_measurement(id: int, dto: MeasurementPlanDto, service: MeasurementService = Depends(MeasurementService)):
    service.plan_measurement(id, plan_at=dto.plan_at, ae_delta=dto.ae_delta)


@router.delete("/{id}/plan", status_code=status.HTTP_200_OK,
    summary="Zrušit plánování měření",
    description="Zruší naplánování konkrétního měření."
               )
async def unplan_measurement(id: int, service: MeasurementService = Depends(MeasurementService)):
    service.unplan_measurement(id)

# TODO exception handling (handle errors that are thrown in service layer)
#  see https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers
