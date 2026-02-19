import logging
from typing import Optional, Dict, Any
from app.services.crawler.base import CloudCrawlerBase
from app.models.graph import CloudResource
from app.core.exceptions import CloudAPIError

logger = logging.getLogger(__name__)


class AzureCrawler(CloudCrawlerBase):
    def __init__(self, neo4j_service):
        super().__init__(neo4j_service)
        self.provider = "azure"

    async def crawl_resources(
        self, org_id: str, account_id: str, credentials: dict
    ) -> list[CloudResource]:
        try:
            from azure.identity import ClientSecretCredential
            from azure.mgmt.compute import ComputeManagementClient

            client_id = credentials.get("client_id")
            client_secret = credentials.get("client_secret")
            tenant_id = credentials.get("tenant_id")
            subscription_id = credentials.get("subscription_id")

            credential = ClientSecretCredential(
                client_id=client_id,
                client_secret=client_secret,
                tenant_id=tenant_id,
            )

            compute_client = ComputeManagementClient(credential, subscription_id)

            resources = []
            for vm in compute_client.virtual_machines.list_all():
                resource = CloudResource(
                    id=vm.id,
                    org_id=org_id,
                    name=vm.name,
                    resource_type="azure_vm",
                    provider="azure",
                    account_id=account_id,
                    metadata={
                        "type": vm.type,
                        "location": vm.location,
                    },
                )
                resources.append(resource)

            return resources
        except Exception as e:
            logger.error(f"Azure crawl error: {str(e)}")
            raise CloudAPIError("Azure", str(e))
