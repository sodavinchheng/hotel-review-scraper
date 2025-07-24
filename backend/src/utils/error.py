from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse


def error_handler(request: Request, exception: Exception) -> JSONResponse:
    """
    Handles exceptions raised during request processing.

    Args:
        request: The request object.
        exception: The exception that was raised.

    Returns:
        A JSON response with the error details.
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_detail = {
        "error_code": "INTERNAL_SERVER_ERROR",
        "message": "An unexpected error occurred.",
        "detail": {},
    }

    if isinstance(exception, HTTPException):
        status_code = exception.status_code
        error_detail = exception.detail
    elif isinstance(exception, RequestValidationError):
        detail = {}
        for error in exception.errors():
            key = ".".join(error["loc"])
            msg = error["msg"]
            detail[key] = msg

        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        error_detail = {
            "error_code": "9999",
            "message": "Invalid request data",
            "detail": detail,
        }
    elif isinstance(exception, ResponseValidationError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_detail = {
            "error_code": "9999",
            "message": "Response validation failed",
            "detail": {
                "errors": exception.errors(),
            },
        }

    return JSONResponse(
        status_code=status_code,
        content={
            "error_code": error_detail["error_code"],
            "message": error_detail["message"],
            "detail": error_detail.get("detail", {}),
        },
    )
