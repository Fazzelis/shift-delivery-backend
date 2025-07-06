from pydantic_settings import BaseSettings
from fastapi.security import HTTPBearer
from typing import ClassVar


class Settings(BaseSettings):
    expiration_time_of_access_token: int = 5
    expiration_time_of_refresh_token: int = 20160
    expiration_time_of_access_token_for_browser: int = expiration_time_of_access_token*60
    expiration_time_of_refresh_token_for_browser: int = expiration_time_of_refresh_token*60
    url: str = "https://26.122.80.20:8000"
    http_bearer: ClassVar = HTTPBearer()


settings = Settings()
