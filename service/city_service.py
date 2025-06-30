from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import City
from schemas.city_schema import CitySchema
from schemas.response.city_response import CitiesResponse


class CityService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_cities(self) -> CitiesResponse:
        result = await self.db.execute(select(City))
        cities = result.scalars().all()
        if cities:
            cities_schemas = [CitySchema.from_orm(city) for city in cities]
        else:
            cities_schemas = []

        return CitiesResponse(
            status="success",
            cities=cities_schemas
        )
