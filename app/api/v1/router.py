from fastapi import APIRouter, Depends
from app.api.deps import verify_api_key
from app.api.v1.endpoints import auth, chat, resources, admin

router = APIRouter(prefix="/v1", dependencies=[Depends(verify_api_key)])

router.include_router(auth.router)
router.include_router(chat.router)
router.include_router(resources.router)
router.include_router(admin.router)
