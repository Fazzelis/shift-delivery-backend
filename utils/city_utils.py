from sqlalchemy.ext.asyncio import AsyncSession
from database.get_session import get_db
from fastapi import Depends
import requests
from models import City
from sqlalchemy import select


def get_coordinates(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1,
        "accept-language": "ru"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; Windows NT 10.4;) AppleWebKit/534.22 (KHTML, like Gecko) Chrome/52.0.3497.264 Safari/537.3 Edge/8.90371"
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        print("error")
    data = response.json()
    if data:
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon
    else:
        return None, None


def get_cities_coordinates():
    with open("utils/city.txt", "r", encoding="utf-8") as file:
        cities = [line.strip() for line in file if line.strip()]
    results = []
    for city in cities:
        lat, lon = get_coordinates(city)
        results.append([city, lat, lon])
    return results


def get_distance_between_cities(lat1, lat2, lon1, lon2):
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error")
        exit()
    data = response.json()
    route = data["routes"][0]
    return route["distance"], route["duration"]


async def fill_cities_info():
    cities_info = get_cities_coordinates()
    async for db in get_db():
        for city in cities_info:
            result = await db.execute(select(City).where(City.name == city[0]))
            optional_city = result.scalar_one_or_none()
            if optional_city:
                continue
            db.add(City(
                name=city[0],
                lat=str(city[1]),
                lon=str(city[2])
            ))
        await db.commit()
