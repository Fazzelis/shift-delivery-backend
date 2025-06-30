from sqlalchemy.ext.asyncio import AsyncSession
from utils.jwt_utils import decode_jwt, encode_jwt
from jwt import ExpiredSignatureError
from fastapi import HTTPException
from sqlalchemy import select
from models import User
from fastapi import Response
from configuration import settings
from schemas.response.login_registration_response import LoginRegistrationResponse
from schemas.JwtTokenSchema import TokenInfo


class RefreshTokenService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def refresh_token(self, refresh_token: str | None, response: Response) -> LoginRegistrationResponse:
        try:
            user_id = decode_jwt(token=refresh_token)
            result = await self.db.execute(select(User).where(User.id == user_id))
            optional_user = result.scalar_one_or_none()
            if not optional_user:
                raise HTTPException(status_code=404, detail="User not found")
            access_jwt_payload = {
                "sub": str(optional_user.id)
            }
            refresh_jwt_payload = {
                "sub": str(optional_user.id)
            }

            refresh_token = encode_jwt(payload=refresh_jwt_payload, token_type="refresh")
            access_token = encode_jwt(payload=access_jwt_payload, token_type="access")

            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                samesite="lax",
                max_age=settings.expiration_time_of_refresh_token
            )
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                samesite="lax",
                max_age=settings.expiration_time_of_access_token
            )

            return LoginRegistrationResponse(
                status="success",
                user_id=optional_user.id,
                token_info=TokenInfo(
                    token=access_token,
                    token_type="Bearer"
                )
            )

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token is expired")
