from pydantic import BaseModel
from schemas.user_schema import UserSchema


class UserResponse(BaseModel):
    status: str
    user_info: UserSchema
