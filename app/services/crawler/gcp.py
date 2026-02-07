import logging
from typing import Optional, Dict, Any
from app.services.crawler.base import CloudCrawlerBase
from app.models.neo4j_models import CloudResource
from app.core.exceptions import CloudAPIError

logger = logging.getLogger(__name__)


class GCPCrawler(CloudCrawlerBase):
    def __init__(self, neo4j_service):
        super().__init__(neo4j_service)
        self.provider = "gcp"

    async def crawl_resources(
        self, org_id: str, account_id: str, credentials: dict
    ) -> list[CloudResource]:
        try:
            from google.cloud import compute_v1
            from google.oauth2 import service_account

            credentials_json = credentials.get("service_account_json")
            project_id = credentials.get("project_id")

            gcp_credentials = service_account.Credentials.from_service_account_info(
                credentials_json
            )

            instances_client = compute_v1.InstancesClient(credentials=gcp_credentials)

            resources = []
            request = compute_v1.AggregatedListInstancesRequest(project=project_id)

            for zone, response in instances_client.aggregated_list(request=request):
                if response.instances:
                    for instance in response.instances:
                        resource = CloudResource(
                            id=instance.id,
                            org_id=org_id,
                            name=instance.name,
                            resource_type="gcp_compute",
                            provider="gcp",
                            account_id=account_id,
                            metadata={
                                "status": instance.status,
                                "machine_type": instance.machine_type,
                                "zone": zone,
                            },
                        )
                        resources.append(resource)

            return resources
        except Exception as e:
            logger.error(f"GCP crawl error: {str(e)}")
            raise CloudAPIError("GCP", str(e))
