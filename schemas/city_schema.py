from pydantic import BaseModel
from uuid import UUID


class CitySchema(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True
        from_attributes = True
