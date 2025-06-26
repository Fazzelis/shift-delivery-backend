from fastapi import APIRouter, Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.get_session import get_db
from service.refresh_token_service import RefreshTokenService
from fastapi import Response
from schemas.response.login_registration_response import LoginRegistrationResponse


router = APIRouter(
    prefix="/refresh",
    tags=["Auth"]
)


@router.post("/refresh", response_model=LoginRegistrationResponse)
async def refresh_tokens(
        response: Response,
        db: AsyncSession = Depends(get_db),
        refresh_token: str | None = Cookie(default=None)
        ):
    return await RefreshTokenService(db).refresh_token(refresh_token=refresh_token, response=response)
