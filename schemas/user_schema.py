from pydantic import BaseModel


class UserSchema(BaseModel):
    email: str
    phone_number: str
    first_name: str
    last_name: str
    middle_name: str
