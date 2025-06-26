from pydantic import BaseModel
from schemas.JwtTokenSchema import TokenInfo
from uuid import UUID


class LoginRegistrationResponse(BaseModel):
    status: str
    user_id: UUID
    token_info: TokenInfo
