from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.login_registration_schema import LoginRegistrationSchema
from database.get_session import get_db
from service.registration_service import RegistrationService
from schemas.response.login_registration_response import LoginRegistrationResponse
from fastapi import Response

router = APIRouter(
    prefix="/registration",
    tags=["Auth"]
)


@router.post("", response_model=LoginRegistrationResponse)
async def login(payload: LoginRegistrationSchema, response: Response, db: AsyncSession = Depends(get_db)):
    return await RegistrationService(db).register(payload, response)
