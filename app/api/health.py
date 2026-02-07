import logging
from fastapi import APIRouter, Depends, status
from app.dependencies import RequestContext, get_request_context
from app.models.schemas import HealthResponse
from app.services.neo4j import Neo4jService
from app.services.weaviate import WeaviateService
from app.services.llm import LLMService

logger = logging.getLogger(__name__)

router = APIRouter()

neo4j_service = Neo4jService()
weaviate_service = WeaviateService()
llm_service = LLMService()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    neo4j_health = await neo4j_service.health_check()
    weaviate_health = await weaviate_service.health_check()
    llm_health = await llm_service.health_check()

    return HealthResponse(
        status="healthy" if all([neo4j_health, weaviate_health, llm_health]) else "degraded",
        version="0.1.0",
        components={
            "neo4j": neo4j_health,
            "weaviate": weaviate_health,
            "llm": llm_health,
        },
    )
