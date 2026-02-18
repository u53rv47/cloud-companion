import hmac
import hashlib
import logging
from datetime import datetime, timezone
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

    key_node = await app.api_key_repo.find_by_hash(key_hash)

    if not key_node:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if not key_node.is_active:
        raise HTTPException(status_code=403, detail="API key disabled")

    expires_at = key_node.expires_at
    if expires_at:
        if expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=403, detail="API key expired")

    return {
        "org_id": key_node.org_id,
        "key_id": key_node.id,
        "name": key_node.name,
    }
