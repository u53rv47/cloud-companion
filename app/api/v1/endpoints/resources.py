import logging
import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from app.api.deps import RequestContext, get_request_context
from app.models.schema import CloudResourceResponse
from app.services.neo4j import Neo4jService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/resources", tags=["resources"])
neo4j_service = Neo4jService()


@router.get("", response_model=list[CloudResourceResponse])
async def list_resources(
    skip: int = 0,
    limit: int = 100,
    context: RequestContext = Depends(get_request_context),
):
    try:
        query = """
        MATCH (r:CloudResource {org_id: $org_id})
        RETURN r
        SKIP $skip
        LIMIT $limit
        """

        results = await neo4j_service.execute_query(
            query,
            {"org_id": context.org_id, "skip": skip, "limit": limit},
        )

        return [
            CloudResourceResponse(
                id=r.get("r").get("id"),
                name=r.get("r").get("name"),
                resource_type=r.get("r").get("type"),
                provider=r.get("r").get("provider"),
                account_id=r.get("r").get("account_id"),
                metadata=r.get("r").get("metadata", {}),
                org_id=context.org_id,
                created_at=r.get("r").get("created_at"),
                updated_at=r.get("r").get("updated_at"),
            )
            for r in results
        ]

    except Exception as e:
        logger.error(f"Failed to list resources: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list resources")


@router.get("/{resource_id}", response_model=CloudResourceResponse)
async def get_resource(
    resource_id: str,
    context: RequestContext = Depends(get_request_context),
):
    try:
        query = """
        MATCH (r:CloudResource {id: $resource_id, org_id: $org_id})
        RETURN r
        """

        results = await neo4j_service.execute_query(
            query,
            {"resource_id": resource_id, "org_id": context.org_id},
        )

        if not results:
            raise HTTPException(status_code=404, detail="Resource not found")

        r = results[0]
        return CloudResourceResponse(
            id=r.get("r").get("id"),
            name=r.get("r").get("name"),
            resource_type=r.get("r").get("type"),
            provider=r.get("r").get("provider"),
            account_id=r.get("r").get("account_id"),
            metadata=r.get("r").get("metadata", {}),
            org_id=context.org_id,
            created_at=r.get("r").get("created_at"),
            updated_at=r.get("r").get("updated_at"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get resource: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get resource")
