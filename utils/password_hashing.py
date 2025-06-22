from passlib.context import CryptContext

hashing_password = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return hashing_password.hash(password)


def match_hash(password: str, password_hash: str) -> bool:
    return hashing_password.verify(password, password_hash)