from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Package, Attachment
from schemas.package_schema import PackageSchema
from schemas.response.package_response import PackagesResponse, PackageResponse
from schemas.package_schema import PackagePost, PackageSchemaForResponse
from fastapi import HTTPException
from uuid import UUID
from configuration import settings


class PackageService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_packages(self) -> PackagesResponse:
        result = await self.db.execute(select(Package))
        packages = result.scalars().all()
        packages_schemas = []
        for package in packages:
            packages_schemas.append(PackageSchemaForResponse(
                id=package.id,
                name=package.name,
                length=package.length,
                width=package.width,
                height=package.height,
                icon_url=f"{settings.url}/attachment/get?attachment_id={package.icon_id}"
            ))
        return PackagesResponse(
            status="success",
            packages=packages_schemas
        )

    async def post_package(self, payload: PackagePost) -> PackageResponse:
        result = await self.db.execute(select(Package).where(Package.name == payload.name))
        optional_package = result.scalar_one_or_none()
        if optional_package:
            raise HTTPException(status_code=400, detail="Package with this name already exist")
        package = Package(
            name=payload.name,
            length=payload.length,
            width=payload.width,
            height=payload.height
        )
        self.db.add(package)
        await self.db.commit()
        await self.db.refresh(package)
        return PackageResponse(
            status="success",
            package_info=PackageSchema.from_orm(package)
        )

    async def add_icon(self, icon_id: UUID, package_id: UUID) -> PackageResponse:
        result = await self.db.execute(select(Package).where(Package.id == package_id))
        optional_package = result.scalar_one_or_none()
        if not optional_package:
            raise HTTPException(status_code=404, detail="Package not found")
        result = await self.db.execute(select(Attachment).where(Attachment.id == icon_id))
        optional_icon = result.scalar_one_or_none()
        if not optional_icon:
            raise HTTPException(status_code=404, detail="Icon not found")
        optional_package.icon_id = icon_id
        self.db.add(optional_package)
        await self.db.commit()
        await self.db.refresh(optional_package)

        return PackageResponse(
            status="success",
            package_info=PackageSchema.from_orm(optional_package)
        )
