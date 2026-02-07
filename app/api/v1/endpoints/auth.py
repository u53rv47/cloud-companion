import logging
import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from app.dependencies import RequestContext, get_request_context
from app.models.schemas import APIKeyResponse, APIKeyCreate
from app.services.neo4j import Neo4jService
from app.core.security import generate_api_key, hash_api_key
from datetime import datetime, timedelta
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])
neo4j_service = Neo4jService()


@router.post("/keys", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    key_data: APIKeyCreate,
    context: RequestContext = Depends(get_request_context),
):
    try:
        api_key = generate_api_key()
        hashed_key = hash_api_key(api_key)
        key_id = str(uuid.uuid4())

        expires_at = datetime.utcnow() + timedelta(days=settings.API_KEY_EXPIRY_DAYS)

        query = """
        MATCH (org:Organization {id: $org_id})
        CREATE (k:APIKey {
            id: $id,
            name: $name,
            hashed_key: $hashed_key,
            status: 'active',
            created_at: datetime(),
            expires_at: $expires_at
        })
        CREATE (org)-[:HAS_KEY]->(k)
        RETURN k.id as id, k.status as status, k.created_at as created_at, k.expires_at as expires_at
        """

        results = await neo4j_service.execute_query(
            query,
            {
                "org_id": context.org_id,
                "id": key_id,
                "name": key_data.name,
                "hashed_key": hashed_key,
                "expires_at": expires_at.isoformat(),
            },
        )

        if results:
            return APIKeyResponse(
                id=key_id,
                name=key_data.name,
                description=key_data.description,
                key=api_key,
                status="active",
                org_id=context.org_id,
                created_at=datetime.utcnow(),
                expires_at=expires_at,
            )

        raise HTTPException(status_code=500, detail="Failed to create API key")

    except Exception as e:
        logger.error(f"Failed to create API key: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create API key")


@router.delete("/keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_key(
    key_id: str,
    context: RequestContext = Depends(get_request_context),
):
    try:
        query = """
        MATCH (org:Organization {id: $org_id})-[:HAS_KEY]->(k:APIKey {id: $key_id})
        SET k.status = 'revoked'
        RETURN k.id
        """

        results = await neo4j_service.execute_query(
            query,
            {"org_id": context.org_id, "key_id": key_id},
        )

        if not results:
            raise HTTPException(status_code=404, detail="API key not found")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to revoke API key: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to revoke API key")
