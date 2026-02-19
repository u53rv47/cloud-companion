import logging
from fastapi import APIRouter, Depends
from app.api.deps import get_app
from app.core.application import Application
from app.models.schema import HealthResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check(app: Application = Depends(get_app)):
    neo4j_health = await app.neo4j.health_check()
    weaviate_health = await app.weaviate.health_check()

    return HealthResponse(
        status="healthy" if all([neo4j_health, weaviate_health]) else "degraded",
        version="0.1.0",
        components={"neo4j": neo4j_health, "weaviate": weaviate_health},
    )
