"""The one place errors become HTTP: every domain refusal and every validation failure is application/problem+json
built by `problem`."""
from fastapi import Request
from fastapi.responses import JSONResponse

from tableturn.errors import TableTurnError


async def tableturn_error_handler(
    request: Request,
    exc: TableTurnError,
):
    error = exc.detail

    return JSONResponse(
        status_code=exc.status_code,
        content=error,
        media_type="application/problem+json",
    )


async def validation_error_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=400,
        content={
            "type": "/errors/validation",
            "title": "Validation Error",
            "status": 400,
            "detail": str(exc),
        },
        media_type="application/problem+json",
    )