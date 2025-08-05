from fastapi import Request
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.database import (
    DB_DIALECT,
    DB_DRIVER,
    DB_USERNAME,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_DATABASE,
)

database_url = sqlalchemy.engine.url.URL.create(
    drivername=f"{DB_DIALECT}+{DB_DRIVER}",
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_DATABASE,
)

engine = engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    return SessionLocal()


def get_session(request: Request):
    return request.state.session if hasattr(request.state, 'session') else get_db_session()
