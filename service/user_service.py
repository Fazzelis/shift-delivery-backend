from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select
from models import User
from fastapi import HTTPException
from schemas.user_schema import UserSchema
from schemas.response.user_response import UserResponse
from utils.jwt_utils import decode_jwt
from jwt import ExpiredSignatureError


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_info(self, encoded_jwt: str | None) -> UserResponse:
        if not encoded_jwt:
            raise HTTPException(status_code=401, detail="Access token not found")
        try:
            user_id = decode_jwt(encoded_jwt)
            result = await self.db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return UserResponse(
                status="success",
                user_info=UserSchema(
                    email=user.email,
                    phone_number=user.phone_number,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    middle_name=user.middle_name
                )
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Access token expired")
        except HTTPException as error:
            raise error
