from fastapi import FastAPI

from measurement.router import router as measurement_router
from database import Base, engine

# BE application instance
app = FastAPI()


@app.get("/")
async def root():
    return {"health": "OK"}


# registration of other routers
app.include_router(measurement_router)


@app.on_event("startup")
def on_startup():
    # TODO replace by non-deprecated feature
    create_db_and_tables()


def create_db_and_tables():
    """
    DDL of database

    TODO replace with migration?
    """
    Base.metadata.create_all(bind=engine)
