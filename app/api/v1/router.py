from fastapi import APIRouter
from app.api.v1.endpoints import auth, chat, resources, admin

router = APIRouter(prefix="/v1")

router.include_router(auth.router)
router.include_router(chat.router)
router.include_router(resources.router)
router.include_router(admin.router)
