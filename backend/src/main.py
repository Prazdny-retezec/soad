import os

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from labview.router import router as labview_router
from measurement.router import router as measurement_router
from scheduler import scheduler
from security import require_basic_auth
from settings import AppSettings

description = """
Systém SOAD slouží k synchronizaci a správě obrazových a akustických dat. 🚀

## Funkcionalita systému

1. **Získávání dat ze senzorů** – Systém sbírá data z různých typů senzorů, včetně akustických zařízení a kamer (RGB, multispektrálních).
2. **Ukládání dat** – Nasbíraná data jsou nejprve ukládána lokálně a následně synchronizována do centrálního úložiště.
3. **Transformace dat** – Data jsou automaticky převáděna do vhodných formátů jako PNG nebo TIFF.
4. **Automatické měření** – Systém podporuje automatické spuštění měření na základě kritérií jako je čas nebo událost.
5. **Webová administrace** – Poskytuje uživatelské rozhraní pro konfiguraci systému a plánování měření.

## Measurement

Zde naleznete operace pro vytváření, aktualizaci, plánování a mazání měření, včetně podpory periodických měření.

## Auth

You will be able to:

* **Login** (_not implemented_).
"""

# BE application instance
app = FastAPI(
    title="Soad",
    description=description,
    summary="Synchronizace obrazových a akustických dat.",
    version="1.0.0",
    contact={
        "name": "Prázdný řetězec",
        "url": "https://github.com/Prazdny-retezec",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# CORS
origins = ["http://localhost:5000", "http://mchoster.alwaysdata.net/" ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# registration of routers
app.include_router(measurement_router, dependencies=[Depends(require_basic_auth)])
app.include_router(labview_router)


# TODO replace by non-deprecated feature
@app.on_event("startup")
def on_startup():
    settings = AppSettings()

    # create database if not exists
    create_db_and_tables()

    #  check directory for saving data exists and create one if it does not
    if not os.path.exists(settings.output_dir):
        os.mkdir(settings.output_dir)

    print(f"[DEBUG] AUTH_USER={settings.auth_user!r}, AUTH_PASSWORD={settings.auth_password!r}")
    # start task scheduler
    scheduler.start()


def create_db_and_tables():
    """
    DDL of database

    TODO replace with migration?
    """
    Base.metadata.create_all(bind=engine)
