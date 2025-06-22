from fastapi import APIRouter
from routers.login import router as login_router
from routers.registration import router as registration_router
from routers.package import router as package_router

router = APIRouter()
router.include_router(login_router)
router.include_router(registration_router)
router.include_router(package_router)
