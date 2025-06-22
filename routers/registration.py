from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.login_registration_schema import LoginRegistrationSchema
from database.get_session import get_db
from service.registration_service import RegistrationService
from schemas.response.login_registration_response import LoginRegistrationResponse

router = APIRouter(
    prefix="/registration",
    tags=["Registration"]
)


@router.post("", response_model=LoginRegistrationResponse)
async def login(payload: LoginRegistrationSchema, db: AsyncSession = Depends(get_db)):
    return await RegistrationService(db).register(payload)
