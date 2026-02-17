from typing import List, Dict
from app.services.neo4j import Neo4jService
from app.models.neo4j_models import CloudAccount


class CloudAccountRepository:
    def __init__(self, driver: Neo4jService):
        self.driver = driver

    async def create(self, account: CloudAccount):
        query = """
        MATCH (o:Organization {id: $org_id})
        CREATE (c:CloudAccount $props)
        CREATE (o)-[:HAS_ACCOUNT]->(c)
        RETURN c
        """
        return await self.driver.execute_query(
            query,
            {
                "org_id": account.org_id,
                "props": account.to_dict(),
            },
        )

    async def list(self, org_id: str) -> List[Dict]:
        query = """
        MATCH (o:Organization {id: $org_id})-[:HAS_ACCOUNT]->(c)
        RETURN c
        """
        return await self.driver.execute_query(query, {"org_id": org_id})
