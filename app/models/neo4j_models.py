from typing import Optional, Dict, Any, List
from datetime import datetime


class Organization:
    def __init__(
        self,
        id: str,
        name: str,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }


class CloudAccount:
    def __init__(
        self,
        id: str,
        org_id: str,
        name: str,
        provider: str,
        account_id: str,
        created_at: Optional[datetime] = None,
        last_synced: Optional[datetime] = None,
    ):
        self.id = id
        self.org_id = org_id
        self.name = name
        self.provider = provider
        self.account_id = account_id
        self.created_at = created_at or datetime.utcnow()
        self.last_synced = last_synced

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "org_id": self.org_id,
            "name": self.name,
            "provider": self.provider,
            "account_id": self.account_id,
            "created_at": self.created_at.isoformat(),
            "last_synced": self.last_synced.isoformat() if self.last_synced else None,
        }


class CloudResource:
    def __init__(
        self,
        id: str,
        org_id: str,
        name: str,
        resource_type: str,
        provider: str,
        account_id: str,
        metadata: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.org_id = org_id
        self.name = name
        self.resource_type = resource_type
        self.provider = provider
        self.account_id = account_id
        self.metadata = metadata or {}
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "org_id": self.org_id,
            "name": self.name,
            "resource_type": self.resource_type,
            "provider": self.provider,
            "account_id": self.account_id,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


class APIKey:
    def __init__(
        self,
        id: str,
        org_id: str,
        name: str,
        hashed_key: str,
        status: str = "active",
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.org_id = org_id
        self.name = name
        self.hashed_key = hashed_key
        self.status = status
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "org_id": self.org_id,
            "name": self.name,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }
