from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData

from src.config.database import DB_SCHEMA

Base = declarative_base(metadata=MetaData(schema=DB_SCHEMA))


class TimestampMixin:
    created_at = Column(
        "created_at", DateTime(timezone=True), nullable=True, server_default=func.now())
    updated_at = Column(
        "updated_at", DateTime(timezone=True), nullable=True, server_default=func.now(), onupdate=func.now())


class SoftDeleteMixin:
    deleted_at = Column(
        "deleted_at", DateTime(timezone=True), nullable=True)
