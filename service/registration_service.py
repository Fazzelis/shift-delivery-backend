from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.login_registration_schema import LoginRegistrationSchema
from models import User
from fastapi import HTTPException
from utils.password_hashing import get_password_hash
from schemas.JwtTokenSchema import TokenInfo
from schemas.response.login_registration_response import LoginRegistrationResponse
from utils.jwt_utils import encode_jwt


class RegistrationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, payload: LoginRegistrationSchema) -> LoginRegistrationResponse:
        result = await self.db.execute(select(User).where(User.email == payload.email))
        optional_user = result.scalar_one_or_none()
        if optional_user:
            raise HTTPException(status_code=409, detail="User with this email already exist")
        new_user = User(email=payload.email, password_hash=get_password_hash(payload.password))
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        jwt_payload = {
            "sub": str(new_user.id)
        }
        jwt_token = encode_jwt(payload=jwt_payload)

        return LoginRegistrationResponse(
            status="success",
            token_info=TokenInfo(
                token=jwt_token,
                token_type="Bearer"
            )
        )
