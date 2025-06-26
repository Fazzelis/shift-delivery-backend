from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    expiration_time_of_access_token: int = 5
    expiration_time_of_refresh_token: int = 21600
    url: str = "http://26.122.80.20:8000"


settings = Settings()
