from pydantic import BaseModel


class UserSchema(BaseModel):
    email: str
    phone_number: str | None
    first_name: str | None
    last_name: str | None
    middle_name: str | None
