import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.middleware.error_handler import setup_exception_handlers
from app.middleware.logging import LoggingMiddleware
from app.api.v1.router import router as v1_router
from app.api.health import router as health_router
from app.services.neo4j import Neo4jService
from app.services.weaviate import WeaviateService

# Root directory of the cloud-companion project
ROOT_DIR = Path(__file__).parent.parent

logger = logging.getLogger("cloud-companion")

neo4j_service = Neo4jService()
weaviate_service = WeaviateService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    await neo4j_service.connect()

    await weaviate_service.connect()
    yield
    logger.info("Shutting down application")
    await neo4j_service.close()
    await weaviate_service.close()


def create_application() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.DESCRIPTION,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(LoggingMiddleware)

    setup_exception_handlers(app)

    app.include_router(health_router)
    app.include_router(v1_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_application()
