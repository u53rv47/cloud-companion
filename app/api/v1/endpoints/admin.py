import logging
import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from app.api.deps import RequestContext, get_request_context
from app.models.schemas import OrganizationCreate, OrganizationResponse
from app.services.neo4j import Neo4jService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])
neo4j_service = Neo4jService()


@router.get("/organization", response_model=OrganizationResponse)
async def get_organization(
    context: RequestContext = Depends(get_request_context),
):
    try:
        query = """
        MATCH (org:Organization {id: $org_id})
        RETURN org
        """

        results = await neo4j_service.execute_query(
            query,
            {"org_id": context.org_id},
        )

        if not results:
            raise HTTPException(status_code=404, detail="Organization not found")

        org = results[0].get("org")
        return OrganizationResponse(
            id=org.get("id"),
            name=org.get("name"),
            description=org.get("description"),
            created_at=org.get("created_at"),
            updated_at=org.get("updated_at"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get organization: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get organization")


@router.get("/keys")
async def list_api_keys(
    context: RequestContext = Depends(get_request_context),
):
    try:
        query = """
        MATCH (org:Organization {id: $org_id})-[:HAS_KEY]->(k:APIKey)
        RETURN k.id as id, k.name as name, k.status as status, k.created_at as created_at
        """

        results = await neo4j_service.execute_query(
            query,
            {"org_id": context.org_id},
        )

        return results

    except Exception as e:
        logger.error(f"Failed to list API keys: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list API keys")
