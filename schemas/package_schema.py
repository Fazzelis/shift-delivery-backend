from pydantic import BaseModel
from uuid import UUID


class PackageSchema(BaseModel):
    id: UUID
    name: str
    length: int
    width: int
    height: int
    icon_id: UUID | None

    class Config:
        orm_mode = True
        from_attributes = True


class PackagePost(BaseModel):
    name: str
    length: int
    width: int
    height: int


class PackageSchemaForResponse(BaseModel):
    id: UUID
    name: str
    length: int
    width: int
    height: int
    icon_url: str
