import logging
from app.services.neo4j import Neo4jService
from app.services.weaviate import WeaviateService

from app.services.repositories.organization import OrganizationRepository
from app.services.repositories.resource import ResourceRepository

logger = logging.getLogger("cloud-companion")


class Repositories:
    def __init__(self, neo4j):
        self.organization = OrganizationRepository(neo4j)


class Application:
    def __init__(self):
        self.neo4j = Neo4jService()
        self.weaviate = WeaviateService()
        self.started = False

    async def start(self):
        if self.started:
            return

        logger.info("Starting application services")
        await self.neo4j.connect()
        await self.weaviate.connect()

        self.repo = Repositories(self.neo4j)

        self.started = True
        logger.info("Application started")

    async def stop(self):
        if not self.started:
            return

        logger.info("Stopping application services")
        await self.neo4j.close()
        await self.weaviate.close()

        self.started = False
        logger.info("Application stopped")
