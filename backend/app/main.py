import logging

from contextlib import asynccontextmanager

from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.api.routers.api import api_router
from app.api.middlewares.log_request import LogRequestMiddleware
from fastapi.encoders import jsonable_encoder

from app.config.logging import setup_logging

from app.core.mongodb import client as mongodb_client
from app.core.qdrant import client as qdrant_client

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await qdrant_client.setup()
    mongodb_client.connect()
    yield
    await mongodb_client.close()


# Setup logging
setup_logging()


#  Define the app (this should be readed from another file)
app = FastAPI(
    title="Efes Backend",
    version="0.0.1",
    docs_url="/docs",
    openapi_url="/api/docs/openapi.json",
    redoc_url="/documentation",  # Enhable Redoc UI,
    lifespan=lifespan
)


# Include the routers
app.include_router(api_router)


# Include middlewares
app.add_middleware(LogRequestMiddleware)

# Define the error handlers

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": jsonable_encoder(exc.errors(), exclude={"input","url", "ctx"})})


@app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
async def error_500(_: Request, error: HTTPException):
    """
    TODO: Handle the error with our own error handling system.
    """
    log.error(
        "500 - Internal Server Error",
        exc_info=(type(error), error, error.__traceback__),
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Server got itself in trouble",
        },
    )


from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization"],
)
