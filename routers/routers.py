from fastapi import APIRouter
from routers.login import router as login_router
from routers.registration import router as registration_router
from routers.package import router as package_router
from routers.refresh_tokens import router as refresh_tokens_router
from routers.attachment import router as attachment_router
from routers.city import router as city_router
from routers.user import router as user_router
from routers.delivery import router as delivery_router

router = APIRouter()
router.include_router(login_router)
router.include_router(registration_router)
router.include_router(package_router)
router.include_router(refresh_tokens_router)
router.include_router(attachment_router)
router.include_router(city_router)
router.include_router(user_router)
router.include_router(delivery_router)
