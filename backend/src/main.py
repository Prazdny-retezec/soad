import os

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.responses import HTMLResponse

import secrets
from measurement.router import router as measurement_router
from database import Base, engine
from scheduler import scheduler
from settings import AppSettings

# BE application instance

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
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

security = HTTPBasic()

def require_basic_auth(
    credentials: HTTPBasicCredentials = Depends(security),
):
    
    user = os.getenv("AUTH_USER")
    pw   = os.getenv("AUTH_PASSWORD")
    print(user,pw)
    if not (secrets.compare_digest(credentials.username, user)
            and secrets.compare_digest(credentials.password, pw)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    
# registration of routers
app.include_router(
    measurement_router,
    dependencies=[Depends(require_basic_auth)],
)


@app.get(
    "/docs",
    response_class=HTMLResponse,
    dependencies=[Depends(require_basic_auth)],
    include_in_schema=False,          
)
def swagger_docs():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Secure API Docs"
    )

@app.get(
    "/redoc",
    response_class=HTMLResponse,
    dependencies=[Depends(require_basic_auth)],
    include_in_schema=False,          
)
def redoc_docs():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Secure ReDoc"
    )

@app.get(
    "/openapi.json",
    dependencies=[Depends(require_basic_auth)],
    include_in_schema=False,          
)
def openapi_json():
    return app.openapi()

# TODO replace by non-deprecated feature
@app.on_event("startup")
def on_startup():
    settings = AppSettings()

    # create database if not exists
    create_db_and_tables()

    #  check directory for saving data exists and create one if it does not
    if not os.path.exists(settings.output_dir):
        os.mkdir(settings.output_dir)

    print(f"[DEBUG] AUTH_USER={os.getenv("AUTH_USER")!r}, AUTH_PASSWORD={os.getenv("AUTH_PASSWORD")!r}")
    # start task scheduler
    scheduler.start()


def create_db_and_tables():
    """
    DDL of database

    TODO replace with migration?
    """
    Base.metadata.create_all(bind=engine)
