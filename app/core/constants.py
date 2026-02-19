from enum import Enum


class Node(str, Enum):
    ORGANIZATION = "Organization"
    API_KEY = "APIKey"
    ACCOUNT = "Account"
    REGION = "Region"
    AVAILABILITY_ZONE = "AvailabilityZone"
    VIRTUAL_NETWORK = "VirtualNetwork"
    SUBNET = "Subnet"
    ROUTE_TABLE = "RouteTable"
    SECURITY_BOUNDARY = "SecurityBoundary"
    GATEWAY = "Gateway"
    IDENTITY = "Identity"
    POLICY = "Policy"
    RESOURCE = "Resource"


class Relation(str, Enum):
    # Organizational
    OWNS = "OWNS"
    MANAGES = "MANAGES"
    HAS_API_KEY = "HAS_API_KEY"

    # Location
    LOCATED_IN = "LOCATED_IN"
    DEPLOYED_IN = "DEPLOYED_IN"

    # Structural
    CONTAINS = "CONTAINS"
    PART_OF = "PART_OF"

    # Network
    HOSTS = "HOSTS"
    ATTACHED_TO = "ATTACHED_TO"
    ASSOCIATED_WITH = "ASSOCIATED_WITH"
    ROUTES_TO = "ROUTES_TO"
    PROTECTS = "PROTECTS"
    EXPOSES = "EXPOSES"
    CONNECTS_TO = "CONNECTS_TO"

    # IAM / Access
    HAS_POLICY = "HAS_POLICY"
    GRANTS_PERMISSION = "GRANTS_PERMISSION"
    HAS_ACCESS_TO = "HAS_ACCESS_TO"
    ASSUMES_IDENTITY = "ASSUMES_IDENTITY"
    TRUSTS = "TRUSTS"
    IMPERSONATES = "IMPERSONATES"

    # Compute / Storage
    RUNS_ON = "RUNS_ON"
    USES = "USES"
    MOUNTS = "MOUNTS"
    BACKED_BY = "BACKED_BY"

    # Data Flow
    READS_FROM = "READS_FROM"
    WRITES_TO = "WRITES_TO"
    FORWARDS_TO = "FORWARDS_TO"
    ALLOWS_TRAFFIC_TO = "ALLOWS_TRAFFIC_TO"
    DENIES_TRAFFIC_TO = "DENIES_TRAFFIC_TO"

    # Dependency
    DEPENDS_ON = "DEPENDS_ON"
    CALLS = "CALLS"
    TRIGGERS = "TRIGGERS"
    REPLICATES_TO = "REPLICATES_TO"
    FAILS_OVER_TO = "FAILS_OVER_TO"

    # Observability
    EMITS_LOGS_TO = "EMITS_LOGS_TO"
    EMITS_METRICS_TO = "EMITS_METRICS_TO"
    MONITORED_BY = "MONITORED_BY"


class CloudProvider(str, Enum):
    AWS = "AWS"
    AZURE = "AZURE"
    GCP = "GCP"


class Region:
    class AWS(Enum):
        # North America
        US_EAST_1 = ("us-east-1", "US East (N. Virginia)")
        US_EAST_2 = ("us-east-2", "US East (Ohio)")
        US_WEST_1 = ("us-west-1", "US West (N. California)")
        US_WEST_2 = ("us-west-2", "US West (Oregon)")
        CA_CENTRAL_1 = ("ca-central-1", "Canada (Central)")
        MX_CENTRAL_1 = ("mx-central-1", "Mexico (Central)")

        # Europe & Middle East
        EU_WEST_1 = ("eu-west-1", "Europe (Ireland)")
        EU_WEST_2 = ("eu-west-2", "Europe (London)")
        EU_CENTRAL_1 = ("eu-central-1", "Europe (Frankfurt)")
        EU_SOUTH_2 = ("eu-south-2", "Europe (Spain)")
        ME_CENTRAL_1 = ("me-central-1", "Middle East (UAE)")
        IL_CENTRAL_1 = ("il-central-1", "Israel (Tel Aviv)")

        # Asia Pacific
        AP_SOUTH_1 = ("ap-south-1", "Asia Pacific (Mumbai)")
        AP_SOUTHEAST_1 = ("ap-southeast-1", "Asia Pacific (Singapore)")
        AP_SOUTHEAST_2 = ("ap-southeast-2", "Asia Pacific (Sydney)")
        AP_NORTHEAST_1 = ("ap-northeast-1", "Asia Pacific (Tokyo)")

        @property
        def code(self):
            return self.value[0]

        @property
        def name(self):
            return self.value[1]

    class AZURE(Enum):
        # North America
        EAST_US = ("eastus", "East US")
        EAST_US_2 = ("eastus2", "East US 2")
        WEST_US_2 = ("westus2", "West US 2")
        CENTRAL_US = ("centralus", "Central US")
        MEXICO_CENTRAL = ("mexicocentral", "Mexico Central")

        # Europe
        NORTH_EUROPE = ("northeurope", "North Europe (Ireland)")
        WEST_EUROPE = ("westeurope", "West Europe (Netherlands)")
        UK_SOUTH = ("uksouth", "UK South")
        FRANCE_CENTRAL = ("francecentral", "France Central")
        ITALY_NORTH = ("italynorth", "Italy North")

        # Asia
        SOUTHEAST_ASIA = ("southeastasia", "Southeast Asia (Singapore)")
        EAST_ASIA = ("eastasia", "East Asia (Hong Kong)")
        JAPAN_EAST = ("japaneast", "Japan East")
        CENTRAL_INDIA = ("centralindia", "Central India")

        @property
        def code(self):
            return self.value[0]

        @property
        def name(self):
            return self.value[1]

    class GCP(Enum):
        # North America
        US_CENTRAL_1 = ("us-central1", "Iowa, USA")
        US_EAST_1 = ("us-east1", "South Carolina, USA")
        US_EAST_4 = ("us-east4", "N. Virginia, USA")
        US_WEST_1 = ("us-west1", "Oregon, USA")
        NORTHAMERICA_SOUTH_1 = ("northamerica-south1", "Queretaro, Mexico")

        # Europe
        EUROPE_WEST_1 = ("europe-west1", "Belgium")
        EUROPE_WEST_2 = ("europe-west2", "London, UK")
        EUROPE_WEST_3 = ("europe-west3", "Frankfurt, Germany")
        EUROPE_SOUTHWEST_1 = ("europe-southwest1", "Madrid, Spain")

        # Asia
        ASIA_SOUTH_1 = ("asia-south1", "Mumbai, India")
        ASIA_SOUTHEAST_1 = ("asia-southeast1", "Singapore")
        ASIA_NORTHEAST_1 = ("asia-northeast1", "Tokyo, Japan")
        AUSTRALIA_SOUTHEAST_1 = ("australia-southeast1", "Sydney, Australia")

        @property
        def code(self):
            return self.value[0]

        @property
        def name(self):
            return self.value[1]


from enum import Enum


class ResourceType:

    class AWS(str, Enum):
        # Compute
        EC2 = "AWS_EC2"
        AUTO_SCALING_GROUP = "AWS_AutoScalingGroup"
        LAMBDA = "AWS_Lambda"
        ECS = "AWS_ECS"
        EKS = "AWS_EKS"
        FARGATE = "AWS_Fargate"
        APP_RUNNER = "AWS_AppRunner"
        BATCH = "AWS_Batch"
        LIGHTSAIL = "AWS_Lightsail"

        # Networking
        VPC = "AWS_VPC"
        SUBNET = "AWS_Subnet"
        ROUTE_TABLE = "AWS_RouteTable"
        INTERNET_GATEWAY = "AWS_InternetGateway"
        NAT_GATEWAY = "AWS_NATGateway"
        TRANSIT_GATEWAY = "AWS_TransitGateway"
        VPC_PEERING = "AWS_VPCPeering"
        SECURITY_GROUP = "AWS_SecurityGroup"
        NETWORK_ACL = "AWS_NetworkACL"
        APPLICATION_LOAD_BALANCER = "AWS_ApplicationLoadBalancer"
        NETWORK_LOAD_BALANCER = "AWS_NetworkLoadBalancer"
        GATEWAY_LOAD_BALANCER = "AWS_GatewayLoadBalancer"
        CLOUDFRONT = "AWS_CloudFront"
        ROUTE53 = "AWS_Route53"
        API_GATEWAY = "AWS_APIGateway"
        GLOBAL_ACCELERATOR = "AWS_GlobalAccelerator"

        # Storage
        S3 = "AWS_S3"
        EBS = "AWS_EBS"
        EFS = "AWS_EFS"
        FSX = "AWS_FSx"
        BACKUP = "AWS_Backup"

        # Databases
        RDS = "AWS_RDS"
        AURORA = "AWS_Aurora"
        DYNAMODB = "AWS_DynamoDB"
        REDSHIFT = "AWS_Redshift"
        ELASTICACHE = "AWS_ElastiCache"
        OPENSEARCH = "AWS_OpenSearch"
        DOCUMENTDB = "AWS_DocumentDB"
        NEPTUNE = "AWS_Neptune"

        # Messaging & Streaming
        SQS = "AWS_SQS"
        SNS = "AWS_SNS"
        EVENTBRIDGE = "AWS_EventBridge"
        KINESIS = "AWS_Kinesis"
        MSK = "AWS_MSK"

        # Identity & Security
        IAM_ROLE = "AWS_IAMRole"
        IAM_USER = "AWS_IAMUser"
        IAM_POLICY = "AWS_IAMPolicy"
        IAM_GROUP = "AWS_IAMGroup"
        KMS_KEY = "AWS_KMSKey"
        SECRETS_MANAGER = "AWS_SecretsManager"
        CERTIFICATE_MANAGER = "AWS_CertificateManager"
        WAF = "AWS_WAF"
        SHIELD = "AWS_Shield"
        COGNITO = "AWS_Cognito"

        # Observability
        CLOUDWATCH = "AWS_CloudWatch"
        CLOUDTRAIL = "AWS_CloudTrail"
        XRAY = "AWS_XRay"

        # Data & Analytics
        ATHENA = "AWS_Athena"
        GLUE = "AWS_Glue"
        EMR = "AWS_EMR"
        QUICKSIGHT = "AWS_QuickSight"

        # DevOps
        CODEBUILD = "AWS_CodeBuild"
        CODEPIPELINE = "AWS_CodePipeline"
        CODEDEPLOY = "AWS_CodeDeploy"
        CLOUDFORMATION = "AWS_CloudFormation"

    class AZURE(str, Enum):
        # Compute
        VIRTUAL_MACHINE = "AZURE_VirtualMachine"
        VM_SCALE_SET = "AZURE_VMScaleSet"
        FUNCTIONS = "AZURE_FunctionApp"
        APP_SERVICE = "AZURE_AppService"
        CONTAINER_APPS = "AZURE_ContainerApps"
        AKS = "AZURE_AKS"
        BATCH = "AZURE_Batch"

        # Networking
        VIRTUAL_NETWORK = "AZURE_VirtualNetwork"
        SUBNET = "AZURE_Subnet"
        NETWORK_SECURITY_GROUP = "AZURE_NetworkSecurityGroup"
        APPLICATION_GATEWAY = "AZURE_ApplicationGateway"
        LOAD_BALANCER = "AZURE_LoadBalancer"
        FRONT_DOOR = "AZURE_FrontDoor"
        TRAFFIC_MANAGER = "AZURE_TrafficManager"
        PRIVATE_ENDPOINT = "AZURE_PrivateEndpoint"
        VPN_GATEWAY = "AZURE_VPNGateway"
        EXPRESS_ROUTE = "AZURE_ExpressRoute"
        DNS_ZONE = "AZURE_DNSZone"

        # Storage
        BLOB_STORAGE = "AZURE_BlobStorage"
        FILE_SHARE = "AZURE_FileShare"
        MANAGED_DISK = "AZURE_ManagedDisk"
        DATA_LAKE = "AZURE_DataLake"

        # Databases
        SQL_DATABASE = "AZURE_SQLDatabase"
        SQL_MANAGED_INSTANCE = "AZURE_SQLManagedInstance"
        COSMOS_DB = "AZURE_CosmosDB"
        POSTGRESQL = "AZURE_PostgreSQL"
        MYSQL = "AZURE_MySQL"
        REDIS_CACHE = "AZURE_RedisCache"

        # Messaging
        SERVICE_BUS = "AZURE_ServiceBus"
        EVENT_GRID = "AZURE_EventGrid"
        EVENT_HUBS = "AZURE_EventHubs"

        # Identity & Security
        ENTRA_ID_USER = "AZURE_EntraIDUser"
        ENTRA_ID_GROUP = "AZURE_EntraIDGroup"
        ROLE_ASSIGNMENT = "AZURE_RoleAssignment"
        KEY_VAULT = "AZURE_KeyVault"
        POLICY = "AZURE_Policy"
        DEFENDER = "AZURE_Defender"
        WAF = "AZURE_WAF"

        # Observability
        MONITOR = "AZURE_Monitor"
        LOG_ANALYTICS = "AZURE_LogAnalytics"
        APPLICATION_INSIGHTS = "AZURE_ApplicationInsights"

        # DevOps
        DEVOPS_PIPELINE = "AZURE_DevOpsPipeline"
        RESOURCE_MANAGER = "AZURE_ResourceManager"

    class GCP(str, Enum):
        # Compute
        COMPUTE_ENGINE = "GCP_ComputeEngine"
        GKE = "GCP_GKE"
        CLOUD_RUN = "GCP_CloudRun"
        CLOUD_FUNCTIONS = "GCP_CloudFunctions"
        APP_ENGINE = "GCP_AppEngine"
        CLOUD_BATCH = "GCP_Batch"

        # Networking
        VPC = "GCP_VPC"
        SUBNET = "GCP_Subnet"
        FIREWALL = "GCP_Firewall"
        CLOUD_LOAD_BALANCER = "GCP_LoadBalancer"
        CLOUD_ARMOR = "GCP_CloudArmor"
        CLOUD_DNS = "GCP_CloudDNS"
        CLOUD_NAT = "GCP_CloudNAT"
        VPN = "GCP_VPN"
        INTERCONNECT = "GCP_Interconnect"

        # Storage
        CLOUD_STORAGE = "GCP_CloudStorage"
        PERSISTENT_DISK = "GCP_PersistentDisk"
        FILestore = "GCP_Filestore"

        # Databases
        CLOUD_SQL = "GCP_CloudSQL"
        SPANNER = "GCP_Spanner"
        BIGTABLE = "GCP_Bigtable"
        FIRESTORE = "GCP_Firestore"
        MEMORYSTORE = "GCP_Memorystore"
        BIGQUERY = "GCP_BigQuery"

        # Messaging
        PUBSUB = "GCP_PubSub"
        EVENTARC = "GCP_Eventarc"

        # Identity & Security
        IAM_USER = "GCP_IAMUser"
        SERVICE_ACCOUNT = "GCP_ServiceAccount"
        IAM_POLICY = "GCP_IAMPolicy"
        KMS_KEY = "GCP_KMSKey"
        SECRET_MANAGER = "GCP_SecretManager"
        CLOUD_IAP = "GCP_IdentityAwareProxy"
        CLOUD_ARMOR_POLICY = "GCP_CloudArmorPolicy"

        # Observability
        CLOUD_MONITORING = "GCP_CloudMonitoring"
        CLOUD_LOGGING = "GCP_CloudLogging"
        CLOUD_TRACE = "GCP_CloudTrace"

        # DevOps
        CLOUD_BUILD = "GCP_CloudBuild"
        DEPLOYMENT_MANAGER = "GCP_DeploymentManager"
