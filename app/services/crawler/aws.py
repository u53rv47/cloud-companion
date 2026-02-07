import logging
from typing import Optional, Dict, Any
from app.services.crawler.base import CloudCrawlerBase
from app.models.neo4j_models import CloudResource
from app.core.exceptions import CloudAPIError

logger = logging.getLogger(__name__)


class AWSCrawler(CloudCrawlerBase):
    def __init__(self, neo4j_service):
        super().__init__(neo4j_service)
        self.provider = "aws"

    async def crawl_resources(
        self, org_id: str, account_id: str, credentials: dict
    ) -> list[CloudResource]:
        try:
            import boto3

            access_key = credentials.get("access_key")
            secret_key = credentials.get("secret_key")
            region = credentials.get("region", "us-east-1")

            ec2 = boto3.client(
                "ec2",
                region_name=region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )

            resources = []
            instances = ec2.describe_instances()

            for reservation in instances.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    resource = CloudResource(
                        id=instance["InstanceId"],
                        org_id=org_id,
                        name=instance.get("PrivateDnsName", instance["InstanceId"]),
                        resource_type="ec2",
                        provider="aws",
                        account_id=account_id,
                        metadata={
                            "state": instance["State"]["Name"],
                            "instance_type": instance["InstanceType"],
                            "availability_zone": instance["Placement"]["AvailabilityZone"],
                        },
                    )
                    resources.append(resource)

            return resources
        except Exception as e:
            logger.error(f"AWS crawl error: {str(e)}")
            raise CloudAPIError("AWS", str(e))
