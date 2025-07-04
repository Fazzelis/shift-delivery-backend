from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.get_session import get_db
from service.user_service import UserService
from schemas.response.user_response import UserResponse
from fastapi.security import HTTPAuthorizationCredentials
from configuration import settings
from schemas.user_schema import UserPatchSchema


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get("/info", response_model=UserResponse)
async def get_info_about_user(
        # encoded_jwt: str | None = Header(None, alias="Authorization"),
        encoded_jwt: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        db: AsyncSession = Depends(get_db)
        ):
    return await UserService(db).get_user_info(encoded_jwt.credentials)


@router.patch("/update-info", response_model=UserResponse)
async def update_user_info(
        new_user_info: UserPatchSchema,
        encoded_jwt: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        db: AsyncSession = Depends(get_db)
):
    return await UserService(db).update_user_info(new_user_info=new_user_info, encoded_jwt=encoded_jwt.credentials)
