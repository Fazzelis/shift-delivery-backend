from sqlalchemy.ext.asyncio import AsyncSession
from schemas.login_registration_schema import LoginRegistrationSchema
from sqlalchemy import select
from models import User
from fastapi import HTTPException
from utils.password_hashing import match_hash
from schemas.response.login_registration_response import LoginRegistrationResponse
from schemas.JwtTokenSchema import TokenInfo
from utils.jwt_utils import encode_jwt
from fastapi import Response
from configuration import settings


class LoginService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def login(self, payload: LoginRegistrationSchema, response: Response):
        result = await self.db.execute(select(User).where(User.email == payload.email))
        optional_user = result.scalar_one_or_none()
        if not optional_user:
            raise HTTPException(status_code=404, detail="User with this email not found")
        if not match_hash(payload.password, optional_user.password_hash):
            raise HTTPException(status_code=409, detail="Password is not correct")

        access_jwt_payload = {
            "sub": str(optional_user.id)
        }
        refresh_jwt_payload = {
            "sub": str(optional_user.id)
        }

        access_token = encode_jwt(payload=access_jwt_payload, token_type="access")
        refresh_token = encode_jwt(payload=refresh_jwt_payload, token_type="refresh")

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="none",
            max_age=settings.expiration_time_of_refresh_token_for_browser
        )

        return LoginRegistrationResponse(
            status="success",
            user_id=optional_user.id,
            token_info=TokenInfo(
                token=access_token,
                token_type="Bearer"
            )
        )
