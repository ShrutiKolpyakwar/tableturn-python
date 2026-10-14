from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from tableturn.errors import TableTurnError


async def tableturn_error_handler(
    request: Request,
    exc: TableTurnError,
):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
        media_type="application/problem+json",
    )


async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
):
    errors = [
        {
            "field": ".".join(
                str(part)
                for part in error.get("loc", ())
                if part != "body"
            ),
            "message": error.get("msg", "Invalid input"),
            "type": error.get("type", "value_error"),
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "type": "/errors/validation",
            "title": "Validation Error",
            "status": 422,
            "detail": "Request validation failed.",
            "errors": errors,
        },
        media_type="application/problem+json",
    )