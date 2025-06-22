from pydantic import BaseModel
from schemas.JwtTokenSchema import TokenInfo


class LoginRegistrationResponse(BaseModel):
    status: str
    token_info: TokenInfo
