from pydantic import BaseModel


class LoginRegistrationSchema(BaseModel):
    email: str
    password: str
