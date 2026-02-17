from enum import Enum


class CloudProvider(str, Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


class APIKeyStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"


from enum import Enum


class ResourceType:
    class AWS(str, Enum):
        EC2 = "aws_ec2"
        RDS = "aws_rds"
        S3 = "aws_s3"
        VPC = "aws_vpc"
        LAMBDA = "aws_lambda"
        IAM = "aws_iam"
        CLOUDWATCH = "aws_cloudwatch"

    class AZURE(str, Enum):
        VM = "azure_vm"
        SQL = "azure_sql"

    class GCP(str, Enum):
        COMPUTE = "gcp_compute"
        STORAGE = "gcp_storage"
