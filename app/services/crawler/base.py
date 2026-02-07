import logging
import uuid
from typing import Optional
from app.services.neo4j import Neo4jService
from app.core.exceptions import ResourceNotFoundError
from app.models.neo4j_models import CloudResource

logger = logging.getLogger(__name__)


class CloudCrawlerBase:
    def __init__(self, neo4j_service: Neo4jService):
        self.neo4j = neo4j_service
        self.provider = None

    async def crawl_resources(
        self, org_id: str, account_id: str, credentials: dict
    ) -> list[CloudResource]:
        raise NotImplementedError

    async def store_resource(
        self, org_id: str, account_id: str, resource: CloudResource
    ) -> Optional[str]:
        try:
            resource_id = str(uuid.uuid4())
            query = """
            MERGE (org:Organization {id: $org_id})
            MERGE (account:CloudAccount {id: $account_id})
            MERGE (resource:CloudResource {id: $resource_id})
            SET resource.name = $name,
                resource.type = $type,
                resource.provider = $provider,
                resource.metadata = $metadata,
                resource.created_at = datetime()
            CREATE (org)-[:HAS_ACCOUNT]->(account)
            CREATE (account)-[:HAS_RESOURCE]->(resource)
            RETURN resource.id
            """
            results = await self.neo4j.execute_query(
                query,
                {
                    "org_id": org_id,
                    "account_id": account_id,
                    "resource_id": resource_id,
                    "name": resource.name,
                    "type": resource.resource_type,
                    "provider": resource.provider,
                    "metadata": resource.metadata,
                },
            )
            return results[0]["resource.id"] if results else None
        except Exception as e:
            logger.error(f"Failed to store resource: {str(e)}")
            raise
