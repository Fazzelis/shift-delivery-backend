from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import User
from fastapi import HTTPException
from schemas.user_schema import UserSchema, UserPatchSchema
from schemas.city_schema import CitySchema
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
            result = await self.db.execute(select(User).options(selectinload(User.city)).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            city_info = None
            if user.city is not None:
                city_info = CitySchema(
                    id=user.city.id,
                    name=user.city.name
                )

            return UserResponse(
                status="success",
                user_info=UserSchema(
                    email=user.email,
                    phone_number=user.phone_number,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    middle_name=user.middle_name,
                    city_info=city_info
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
            result = await self.db.execute(select(User).options(selectinload(User.city)).where(User.id == user_id))
            optional_user = result.scalar_one_or_none()
            if not optional_user:
                raise HTTPException(status_code=404, detail="User not found")

            new_data = new_user_info.dict(exclude_unset=True)
            for key, value in new_data.items():
                setattr(optional_user, key, value)

            # if new_user_info.last_name is not None:
            #     optional_user.last_name = new_user_info.last_name
            # if new_user_info.first_name is not None:
            #     optional_user.first_name = new_user_info.first_name
            # if new_user_info.middle_name is not None:
            #     optional_user.middle_name = new_user_info.middle_name
            # if new_user_info.phone_number is not None:
            #     optional_user.phone_number = new_user_info.phone_number
            # if new_user_info.city_id is not None:
            #     optional_user.city_id = new_user_info.city_id

            self.db.add(optional_user)
            await self.db.commit()
            await self.db.refresh(optional_user)

            city_info = None
            if optional_user.city is not None:
                city_info = CitySchema(
                    id=optional_user.city.id,
                    name=optional_user.city.name
                )

            return UserResponse(
                status="success",
                user_info=UserSchema(
                    email=optional_user.email,
                    phone_number=optional_user.phone_number,
                    first_name=optional_user.first_name,
                    last_name=optional_user.last_name,
                    middle_name=optional_user.middle_name,
                    city_info=city_info
                )
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token not found")
        except HTTPException as error:
            raise error
