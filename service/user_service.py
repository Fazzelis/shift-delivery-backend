from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select
from models import User
from fastapi import HTTPException
from schemas.user_schema import UserSchema, UserPatchSchema
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
                    middle_name=user.middle_name,
                    city_id=user.city_id
                )
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Access token expired")
        except HTTPException as error:
            raise error

    async def update_user_info(self, new_user_info: UserPatchSchema, encoded_jwt: str | None) -> UserResponse:
        if not encoded_jwt:
            raise HTTPException(status_code=401, detail="Token not found")
        try:
            user_id = decode_jwt(encoded_jwt)
            result = await self.db.execute(select(User).where(User.id == user_id))
            optional_user = result.scalar_one_or_none()
            if not optional_user:
                raise HTTPException(status_code=404, detail="User not found")
            if new_user_info.last_name is not None:
                optional_user.last_name = new_user_info.last_name
            if new_user_info.first_name is not None:
                optional_user.first_name = new_user_info.first_name
            if new_user_info.middle_name is not None:
                optional_user.middle_name = new_user_info.middle_name
            if new_user_info.phone_number is not None:
                optional_user.phone_number = new_user_info.phone_number
            if new_user_info.city_id is not None:
                optional_user.city_id = new_user_info.city_id
            self.db.add(optional_user)
            await self.db.commit()
            await self.db.refresh(optional_user)

            return UserResponse(
                status="success",
                user_info=UserSchema(
                    email=optional_user.email,
                    phone_number=optional_user.phone_number,
                    first_name=optional_user.first_name,
                    last_name=optional_user.last_name,
                    middle_name=optional_user.middle_name,
                    city_id=optional_user.city_id
                )
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token not found")
        except HTTPException as error:
            raise error
