from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from src.dependencies.database import get_db_session
from src.routes.base import router
from src.utils.error import error_handler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.session = get_db_session()
    try:
        return await call_next(request)
    except Exception as exception:
        request.state.session.rollback()
        raise exception
    finally:
        request.state.session.close()


app.include_router(router, prefix="/api")


@app.exception_handler(HTTPException)
@app.exception_handler(RequestValidationError)
@app.exception_handler(Exception)
async def exception_handler(request: Request, exception: Exception):
    return error_handler(request, exception)
