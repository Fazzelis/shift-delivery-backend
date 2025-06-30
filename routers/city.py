from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.get_session import get_db
from service.city_service import CityService
from schemas.response.city_response import CitiesResponse


router = APIRouter(
    prefix="/city",
    tags=["City"]
)


@router.get("/get-all-cities", response_model=CitiesResponse)
async def get_all_cities(db: AsyncSession = Depends(get_db)):
    return await CityService(db).get_all_cities()
