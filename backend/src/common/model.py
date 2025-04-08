from datetime import datetime
from sqlalchemy import Column, DateTime

from database import Base


class Auditable(Base):
    __abstract__ = True

    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now())
    deleted_at = Column(DateTime, nullable=True, default=None)
