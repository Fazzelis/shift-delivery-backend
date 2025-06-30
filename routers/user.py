from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from database.get_session import get_db
from service.user_service import UserService
from schemas.response.user_response import UserResponse


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get("/info", response_model=UserResponse)
async def get_info_about_user(encoded_jwt: str | None = Header(None, alias="Authorization"), db: AsyncSession = Depends(get_db)):
    return await UserService(db).get_user_info(encoded_jwt)
