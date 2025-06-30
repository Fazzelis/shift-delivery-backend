from pydantic import BaseModel
from schemas.city_schema import CitySchema


class CitiesResponse(BaseModel):
    status: str
    cities: list[CitySchema]
