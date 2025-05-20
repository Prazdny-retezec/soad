from typing import List, Optional
import logging
from fastapi import APIRouter, status, Depends
from fastapi import HTTPException, Query

from common.enum import OrderDir
from measurement.dto import MeasurementCreateDto, MeasurementUpdateDto, MeasurementListDto, MeasurementDetailDto, \
    MeasurementCreatePeriodicDto, MeasurementPlanDto
from measurement.model import MeasurementState
from measurement.service import MeasurementService
from fastapi import APIRouter, Depends
from datetime import datetime

router = APIRouter(
    prefix="/measurement",
    tags=["Measurement"],
)


@router.get(
    path="",
    summary="Získat seznam měření",
    description="Vrací seznam všech uložených měření.",
    response_model=list[MeasurementListDto]
)
async def list_measurements(
        state: Optional[MeasurementState] = None,
        date: Optional[datetime] = None,
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=20),
        order_by: Optional[str] = Query(default=None),
        order_dir: OrderDir = Query(OrderDir.desc),
        service: MeasurementService = Depends(MeasurementService)
):
    return service.list_measurements(state, date, page, page_size, order_by, order_dir)


@router.get(
    path="/{id}",
    summary="Získat detail měření",
    description="Vrací detailní informace o měření podle zadaného ID."
)
async def get_measurement(
        id: int,
        service: MeasurementService = Depends(MeasurementService)
) -> MeasurementDetailDto:
    return service.get_measurement(id)


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    summary="Vytvořit nové měření",
    description="Vytvoří nové měření na základě vstupních dat a vrátí jeho přehled."
)
async def create_measurement(
        dto: MeasurementCreateDto,
        service: MeasurementService = Depends(MeasurementService)
) -> MeasurementListDto:
    return service.create_measurement(dto)


@router.post(
    path="/periodic",
    status_code=status.HTTP_201_CREATED,
    summary="Vytvořit periodická měření",
    description="Na základě vstupních dat vytvoří více měření v pravidelných intervalech."
)
async def create_periodic_measurement(
        dto: MeasurementCreatePeriodicDto,
        service: MeasurementService = Depends(MeasurementService)
) -> list[MeasurementListDto]:
    return service.create_periodic_measurement(dto)


@router.put(
    path="/{id}", status_code=status.HTTP_202_ACCEPTED,
    summary="Aktualizovat měření",
    description="Upraví existující měření podle ID a dodaných aktualizačních dat."
)
async def update_measurement(
        id: int,
        dto: MeasurementUpdateDto,
        service: MeasurementService = Depends(MeasurementService)
) -> MeasurementListDto:
    return service.update_measurement(id, dto)


@router.delete(
    path="/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Smazat měření",
    description="Smaže měření se zadaným ID."
)
async def delete_measurement(id: int, service: MeasurementService = Depends(MeasurementService)):
    service.delete_measurement(id)


@router.post(
    path="/{id}/plan", status_code=status.HTTP_200_OK,
    summary="Naplánovat měření",
    description="Naplánuje měření na zvolený čas s volitelnou odchylkou."
)
async def plan_measurement(id: int, dto: MeasurementPlanDto, service: MeasurementService = Depends(MeasurementService)):
    return service.plan_measurement(id, plan_at=dto.plan_at, ae_delta=dto.ae_delta)


@router.delete(
    path="/{id}/plan",
    status_code=status.HTTP_200_OK,
    summary="Zrušit plánování měření",
    description="Zruší naplánování konkrétního měření."
)
async def unplan_measurement(id: int, service: MeasurementService = Depends(MeasurementService)):
    service.unplan_measurement(id)


@router.get("/conflict")
async def check_conflict(plan_from: str, service: MeasurementService = Depends(MeasurementService)) -> dict:
    # converts ISO to datetime object
    plan_from = datetime.fromisoformat(plan_from)

    # checks if conflict exists
    conflict = service.check_for_conflicting_measurements(plan_from)

    return {"conflict": conflict}

# TODO exception handling (handle errors that are thrown in service layer)
#  see https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers
