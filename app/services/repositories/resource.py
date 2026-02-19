from app.services.neo4j import Neo4jService


class ResourceRepository:
    """Repository for generic :Resource nodes and relationship helpers.

    All cloud services are stored as `:Resource` with cloud-specific
    attributes placed into the `metadata` property.
    Methods are organization-scoped where applicable.
    """

    def __init__(self, driver: Neo4jService):
        self.driver = driver
