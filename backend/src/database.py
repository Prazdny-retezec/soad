import logging
from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from settings import AppSettings

engine = create_engine(url=AppSettings().database_url)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger = logging.getLogger("uvicorn")

Base = declarative_base()


def get_db() -> Generator[Session, Any, None]:
    db = sessionLocal()
    try:
        yield db
    finally:
        logger.debug("Closing database connection")
        db.close()
