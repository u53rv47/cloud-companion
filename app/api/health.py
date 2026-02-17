import logging
from fastapi import APIRouter, Depends, status
from app.api.deps import get_app
from app.models.schemas import HealthResponse
from app.services.neo4j import Neo4jService
from app.services.weaviate import WeaviateService
from app.services.llm import LLMService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check(app: Depends(get_app)):
    neo4j_health = await neo4j_service.health_check()
    weaviate_health = await weaviate_service.health_check()

    return HealthResponse(
        status="healthy" if all([neo4j_health, weaviate_health]) else "degraded",
        version="0.1.0",
        components={"neo4j": neo4j_health, "weaviate": weaviate_health},
    )
