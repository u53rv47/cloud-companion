from typing import List, Dict
from app.services.neo4j import Neo4jService
from app.models.neo4j_models import CloudAccount


class CloudAccountRepository:
    def __init__(self, driver: Neo4jService):
        self.driver = driver

    async def create(self, account: CloudAccount) -> CloudAccount | None:
        query = """
        MATCH (o:Organization {id: $org_id})
        CREATE (c:CloudAccount $props)
        CREATE (o)-[:OWNS]->(c)
        RETURN c
        """
        results = await self.driver.execute_query(
            query,
            {
                "org_id": account.org_id,
                "props": account.to_dict(),
            },
        )
        return CloudAccount(**results[0]["c"]) if results else None

    async def list(self, org_id: str) -> List[CloudAccount]:
        query = """
        MATCH (o:Organization {id: $org_id})-[:OWNS]->(c)
        RETURN c
        """
        results = await self.driver.execute_query(query, {"org_id": org_id})
        return [CloudAccount(**r["c"]) for r in results]
