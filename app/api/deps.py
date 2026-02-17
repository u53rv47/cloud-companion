import hmac
import hashlib
import logging
from datetime import datetime
from fastapi import Request, Header, HTTPException, Depends
from app.core.application import Application
from app.core.config import settings

logger = logging.getLogger(__name__)


async def get_app(request: Request):
    return request.app.state.app


def hash_api_key(raw_key: str) -> str:
    return hmac.new(
        settings.API_HMAC_SECRET.encode(),
        raw_key.encode(),
        hashlib.sha256,
    ).hexdigest()


async def verify_api_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
    app: Application = Depends(get_app),
):
    key_hash = hash_api_key(x_api_key)

    record = await app.api_key_repo.find_by_hash(key_hash)

    if not record:
        raise HTTPException(status_code=401, detail="Invalid API key")

    key_node = record["k"]
    org_id = record["org_id"]

    if not key_node.get("is_active", True):
        raise HTTPException(status_code=403, detail="API key disabled")

    expires_at = key_node.get("expires_at")
    if expires_at:
        # Neo4j datetime is not Python datetime
        expires_at = expires_at.to_native() if hasattr(expires_at, "to_native") else expires_at
        if expires_at < datetime.utcnow():
            raise HTTPException(status_code=403, detail="API key expired")

    return {
        "org_id": org_id,
        "key_id": key_node.get("id"),
        "name": key_node.get("name"),
    }
