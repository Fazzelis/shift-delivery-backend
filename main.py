from fastapi import FastAPI
from database.database_conf import engine, Base
from models import User, City
from routers.routers import router
from utils.city_utils import fill_cities_info
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router)
origins = ["*"]
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
