from pydantic import BaseModel
from uuid import UUID


class UserSchema(BaseModel):
    email: str
    phone_number: str | None
    first_name: str | None
    last_name: str | None
    middle_name: str | None
    city_id: UUID | None


class UserPatchSchema(BaseModel):
    phone_number: str | None
    first_name: str | None
    last_name: str | None
    middle_name: str | None
    city_id: UUID | None
