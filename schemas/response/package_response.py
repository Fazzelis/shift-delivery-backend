from pydantic import BaseModel
from schemas.package_schema import PackageSchema, PackageSchemaForResponse


class PackagesResponse(BaseModel):
    status: str
    packages: list[PackageSchemaForResponse]


class PackageResponse(BaseModel):
    status: str
    package_info: PackageSchema
