from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.login_registration_schema import LoginRegistrationSchema
from models import User
from fastapi import HTTPException
from utils.password_hashing import get_password_hash
from schemas.JwtTokenSchema import TokenInfo
from schemas.response.login_registration_response import LoginRegistrationResponse
from utils.jwt_utils import encode_jwt
from fastapi import Response
from configuration import settings


class RegistrationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, payload: LoginRegistrationSchema, response: Response) -> LoginRegistrationResponse:
        result = await self.db.execute(select(User).where(User.email == payload.email))
        optional_user = result.scalar_one_or_none()
        if optional_user:
            raise HTTPException(status_code=409, detail="User with this email already exist")
        new_user = User(email=payload.email, password_hash=get_password_hash(payload.password))
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        access_jwt_payload = {
            "sub": str(new_user.id)
        }
        refresh_jwt_payload = {
            "sub": str(new_user.id)
        }

        access_jwt_token = encode_jwt(payload=access_jwt_payload, token_type="access")
        refresh_jwt_token = encode_jwt(payload=refresh_jwt_payload, token_type="refresh")

        response.set_cookie(
            key="refresh_token",
            value=refresh_jwt_token,
            httponly=True,
            samesite="lax",
            max_age=settings.expiration_time_of_refresh_token
        )
        response.set_cookie(
            key="access_token",
            value=access_jwt_token,
            httponly=True,
            samesite="lax",
            max_age=settings.expiration_time_of_access_token
        )

        return LoginRegistrationResponse(
            status="success",
            user_id=new_user.id,
            token_info=TokenInfo(
                token=access_jwt_token,
                token_type="Bearer"
            )
        )
