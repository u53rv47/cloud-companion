from datetime import datetime
from typing import Optional, Dict, Any
from uuid import uuid4
from app.core.constants import CloudProvider


class Organization:
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id or str(uuid4())
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.now()

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
        org_id: str,
        name: str,
        provider: CloudProvider,
        account_id: str,
        created_at: Optional[datetime] = None,
        last_synced: Optional[datetime] = None,
    ):
        self.org_id = org_id
        self.name = name
        self.provider = provider
        self.account_id = account_id
        self.created_at = created_at or datetime.utcnow()
        self.last_synced = last_synced

    def to_dict(self) -> Dict[str, Any]:
        return {
            "org_id": self.org_id,
            "name": self.name,
            "provider": self.provider.value,
            "account_id": self.account_id,
            "created_at": self.created_at.isoformat(),
            "last_synced": self.last_synced.isoformat() if self.last_synced else None,
        }


class APIKey:
    def __init__(
        self,
        org_id: str,
        name: str,
        hashed_key: str,
        id: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        expires_at: Optional[datetime] = None,
    ):
        self.id = id or str(uuid4())
        self.org_id = org_id
        self.name = name
        self.hashed_key = hashed_key
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.expires_at = expires_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "org_id": self.org_id,
            "name": self.name,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }
