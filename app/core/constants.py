from enum import Enum


class CloudProvider(str, Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


class SkillLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    PROFESSIONAL = "Pro"


class APIKeyStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"


class ResourceType(str, Enum):
    EC2 = "ec2"
    RDS = "rds"
    S3 = "s3"
    VPC = "vpc"
    LAMBDA = "lambda"
    IAM = "iam"
    CLOUDWATCH = "cloudwatch"
    AZURE_VM = "azure_vm"
    AZURE_SQL = "azure_sql"
    GCP_COMPUTE = "gcp_compute"
    GCP_STORAGE = "gcp_storage"
