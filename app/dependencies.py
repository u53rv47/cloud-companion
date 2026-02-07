import logging
from fastapi import Request, HTTPException, status, Depends
from typing import Optional, Dict, Any
from app.core.security import verify_api_key, hash_api_key
from app.services.neo4j import Neo4jService
from app.core.exceptions import AuthenticationError, AuthorizationError

logger = logging.getLogger(__name__)

neo4j_service = Neo4jService()


class RequestContext:
    def __init__(self, org_id: str, api_key_id: str, account_ids: list[str]):
        self.org_id = org_id
        self.api_key_id = api_key_id
        self.account_ids = account_ids


async def verify_api_key_header(request: Request) -> RequestContext:
    api_key = request.headers.get("X-API-Key")

    if not api_key:
        raise AuthenticationError("API key missing")

    try:
        hashed_key = hash_api_key(api_key)

        query = """
        MATCH (k:APIKey {hashed_key: $hashed_key, status: 'active'})
        MATCH (k)-[:BELONGS_TO]->(org:Organization)
        MATCH (org)-[:HAS_ACCOUNT]->(acc:CloudAccount)
        RETURN k.id as key_id, org.id as org_id, collect(acc.id) as account_ids
        """

        results = await neo4j_service.execute_query(query, {"hashed_key": hashed_key})

        if not results:
            raise AuthenticationError("Invalid or revoked API key")

        result = results[0]
        return RequestContext(
            org_id=result.get("org_id"),
            api_key_id=result.get("key_id"),
            account_ids=result.get("account_ids", []),
        )
    except AuthenticationError:
        raise
    except Exception as e:
        logger.error(f"API key verification error: {str(e)}")
        raise AuthenticationError("Failed to verify API key")


async def get_request_context(request: Request) -> RequestContext:
    return await verify_api_key_header(request)
