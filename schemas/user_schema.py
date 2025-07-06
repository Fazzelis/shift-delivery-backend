from pydantic import BaseModel
from uuid import UUID
from schemas.city_schema import CitySchema


class UserSchema(BaseModel):
    email: str
    phone_number: str | None
    first_name: str | None
    last_name: str | None
    middle_name: str | None
    city_info: CitySchema | None


class UserPatchSchema(BaseModel):
    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    city_id: UUID | None = None
