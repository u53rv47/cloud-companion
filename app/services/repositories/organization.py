from typing import List, Dict
from app.services.neo4j import Neo4jService
from app.models.neo4j_models import Organization


class OrganizationRepository:
    def __init__(self, driver: Neo4jService):
        self.driver = driver

    async def create(self, org: Organization) -> Organization | None:
        query = """
        CREATE (o:Organization $props)
        RETURN o
        """
        results = await self.driver.execute_query(query, {"props": org.to_dict()})
        return Organization(**results[0]["o"]) if results else None

    async def get_by_name(self, name: str) -> Organization | None:
        query = """
        MATCH (o:Organization {name: $name})
        RETURN o
        """
        results = await self.driver.execute_query(query, {"name": name})
        return Organization(**results[0]["o"]) if results else None

    async def list(self) -> List[Organization]:
        query = """
        MATCH (o:Organization)
        RETURN o
        """
        results = await self.driver.execute_query(query)
        return [Organization(**r["o"]) for r in results]

    async def delete(self, org_id: str) -> None:
        query = """
        MATCH (o:Organization {id: $id})
        DETACH DELETE o
        """
        await self.driver.execute_query(query, {"id": org_id})
