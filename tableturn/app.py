from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from tableturn.errors import TableTurnError
from tableturn.handlers import (
    tableturn_error_handler,
    validation_error_handler,
)
from tableturn.routers.tables import router as tables_router
from tableturn.services.seed import initialize_database
from tableturn.routers.parties import router as parties_router
from tableturn.routers.waitlist import router as waitlist_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


def create_app():
    app = FastAPI(
        title="TableTurn",
        lifespan=lifespan,
    )

    app.add_exception_handler(
        TableTurnError,
        tableturn_error_handler,
    )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request,
        exc: RequestValidationError,
    ):
        return await validation_error_handler(request, exc)

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_error(
        request: Request,
        exc: StarletteHTTPException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "type": f"/errors/http-{exc.status_code}",
                "title": "HTTP Error",
                "status": exc.status_code,
                "detail": str(exc.detail),
            },
            media_type="application/problem+json",
        )

    app.include_router(tables_router)
    app.include_router(parties_router)
    app.include_router(waitlist_router)
    return app


app = create_app()