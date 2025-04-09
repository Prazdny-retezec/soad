from fastapi import FastAPI

from measurement.router import router as measurement_router
from database import Base, engine
from scheduler import scheduler

# BE application instance
app = FastAPI()

# registration of routers
app.include_router(measurement_router)


# TODO replace by non-deprecated feature
@app.on_event("startup")
def on_startup():
    # create database if not exists
    create_db_and_tables()

    # start task scheduler
    scheduler.start()


def create_db_and_tables():
    """
    DDL of database

    TODO replace with migration?
    """
    Base.metadata.create_all(bind=engine)
