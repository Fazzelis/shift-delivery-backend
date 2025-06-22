from sqlalchemy.ext.asyncio import AsyncSession
from schemas.login_registration_schema import LoginRegistrationSchema
from sqlalchemy import select
from models import User
from fastapi import HTTPException
from utils.password_hashing import match_hash
from schemas.response.login_registration_response import LoginRegistrationResponse
from schemas.JwtTokenSchema import TokenInfo
from utils.jwt_utils import encode_jwt


class LoginService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def login(self, payload: LoginRegistrationSchema):
        result = await self.db.execute(select(User).where(User.email == payload.email))
        optional_user = result.scalar_one_or_none()
        if not optional_user:
            raise HTTPException(status_code=404, detail="User with this email not found")
        if not match_hash(payload.password, optional_user.password_hash):
            raise HTTPException(status_code=409, detail="Password is not correct")

        jwt_payload = {
            "sub": str(optional_user.id)
        }
        jwt_token = encode_jwt(payload=jwt_payload)

        return LoginRegistrationResponse(
            status="success",
            token_info=TokenInfo(
                token=jwt_token,
                token_type="Bearer"
            )
        )
