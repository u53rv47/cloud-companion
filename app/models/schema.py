from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.core.constants import CloudProvider, APIKey


class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationResponse(OrganizationBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CloudAccountBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    provider: CloudProvider
    account_id: str = Field(..., min_length=1)


class CloudAccountCreate(CloudAccountBase):
    credentials_encrypted: str


class CloudAccountResponse(CloudAccountBase):
    id: str
    org_id: str
    created_at: datetime
    last_synced: Optional[datetime] = None

    class Config:
        from_attributes = True


class APIKeyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)


class APIKeyCreate(APIKeyBase):
    pass


class APIKeyResponse(APIKeyBase):
    id: str
    key: str
    status: APIKeyStatus
    org_id: str
    created_at: datetime
    expires_at: datetime
    last_used: Optional[datetime] = None

    class Config:
        from_attributes = True


class CloudResourceBase(BaseModel):
    name: str = Field(..., min_length=1)
    resource_type: str
    provider: CloudProvider
    account_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CloudResourceResponse(CloudResourceBase):
    id: str
    org_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatMessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
    role: str = Field(..., pattern="^(user|assistant)$")


class ChatMessageRequest(ChatMessageBase):
    conversation_id: Optional[str] = None
    context_resources: Optional[List[str]] = None


class ChatMessageResponse(ChatMessageBase):
    id: str
    conversation_id: str
    org_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    message_id: str
    conversation_id: str
    content: str
    sources: Optional[List[Dict[str, Any]]] = None
    confidence: float = Field(ge=0.0, le=1.0)


class HealthResponse(BaseModel):
    status: str
    version: str
    components: Dict[str, bool]
