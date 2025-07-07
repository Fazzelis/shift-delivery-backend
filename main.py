from fastapi import FastAPI
from database.database_conf import engine, Base
from models import User, City
from routers.routers import router
from utils.city_utils import fill_cities_info
from fastapi.middleware.cors import CORSMiddleware
from os import getenv
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()
app.include_router(router)
origins = [
    getenv("FRONTEND_IP"),
    getenv("BACKEND_IP")
]
# origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # await fill_cities_info()

# старт: uvicorn main:app --host {ip} --port {default -> 8000} --ssl-certfile cert.pem --ssl-keyfile key.pem --reload
# uvicorn main:app --host 26.122.80.20 --port 8000 --ssl-certfile cert.pem --ssl-keyfile key.pem --reload

