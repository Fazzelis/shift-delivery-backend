from fastapi import APIRouter, Depends
from service.package_service import PackageService
from sqlalchemy.ext.asyncio import AsyncSession
from database.get_session import get_db
from schemas.response.package_response import PackagesResponse, PackageResponse
from schemas.package_schema import PackagePost
from uuid import UUID

router = APIRouter(
    prefix="/package",
    tags=["Package"]
)


@router.get("/all-packages", response_model=PackagesResponse)
async def get_all_packages(db: AsyncSession = Depends(get_db)):
    return await PackageService(db).get_all_packages()


@router.post("/add-package", response_model=PackageResponse)
async def post_package(payload: PackagePost, db: AsyncSession = Depends(get_db)):
    return await PackageService(db).post_package(payload=payload)


@router.post("/add_icon", response_model=PackageResponse)
async def add_icon(icon_id: UUID, package_id: UUID, db: AsyncSession = Depends(get_db)):
    return await PackageService(db).add_icon(icon_id, package_id)
