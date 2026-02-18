from typing import List, Dict, Optional
from app.services.neo4j import Neo4jService
from app.models.neo4j_models import APIKey


class APIKeyRepository:
    def __init__(self, driver: Neo4jService):
        self.driver = driver

    async def create(self, key: APIKey) -> APIKey | None:
        query = """
        MATCH (o:Organization {id: $org_id})
        CREATE (k:APIKey $props)
        CREATE (o)-[:HAS_API_KEY]->(k)
        RETURN k
        """
        results = await self.driver.execute_query(
            query,
            {
                "org_id": key.org_id,
                "props": key.to_dict() | {"hashed_key": key.hashed_key},
            },
        )
        return APIKey(**results[0]["k"]) if results else None

    async def list(self, org_id: str) -> List[APIKey]:
        query = """
        MATCH (o:Organization {id: $org_id})-[:HAS_API_KEY]->(k)
        RETURN k
        """
        results = await self.driver.execute_query(query, {"org_id": org_id})
        return [APIKey(**r["k"]) for r in results]

    async def revoke(self, key_id: str):
        query = """
        MATCH (k:APIKey {id: $id})
        SET k.is_active = false
        """
        await self.driver.execute_query(query, {"id": key_id})

    async def find_by_hash(self, hashed: str) -> APIKey | None:
        query = """
        MATCH (k:APIKey {hashed_key: $hash})
        RETURN k
        """
        results = await self.driver.execute_query(query, {"hash": hashed})
        return APIKey(**results[0]["k"]) if results else None
