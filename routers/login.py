from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.login_registration_schema import LoginRegistrationSchema
from service.login_service import LoginService
from database.get_session import get_db
from schemas.response.login_registration_response import LoginRegistrationResponse
from fastapi import Response, Request

router = APIRouter(
    prefix="/login",
    tags=["Auth"]
)


@router.post("", response_model=LoginRegistrationResponse)
async def login(payload: LoginRegistrationSchema, response: Response, db: AsyncSession = Depends(get_db)):
    return await LoginService(db).login(payload, response)
