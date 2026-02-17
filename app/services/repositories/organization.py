from typing import List, Dict
from app.services.neo4j import Neo4jService
from app.models.neo4j_models import Organization


class OrganizationRepository:
    def __init__(self, driver: Neo4jService):
        self.driver = driver

    async def create(self, org: Organization) -> Dict:
        query = """
        CREATE (o:Organization $props)
        RETURN o
        """
        result = await self.driver.execute_query(query, {"props": org.to_dict()})
        return result[0] if result else None

    async def list(self) -> List[Dict]:
        query = """
        MATCH (o:Organization)
        RETURN o
        """
        return await self.driver.execute_query(query)

    async def delete(self, org_id: str) -> None:
        query = """
        MATCH (o:Organization {id: $id})
        DETACH DELETE o
        """
        await self.driver.execute_query(query, {"id": org_id})
