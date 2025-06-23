import os
import uuid
from datetime import datetime, timezone, timedelta
import jwt
from configuration import settings
from fastapi import HTTPException


def encode_jwt(
        payload: dict,
        token_type: str,
        private_key: str = os.getenv("PRIVATE_KEY"),
        algorithm: str = os.getenv("ALGORITHM")
        ):
    if token_type == "access":
        expire_minutes = settings.expiration_time_of_access_token
    elif token_type == "refresh":
        expire_minutes = settings.expiration_time_of_refresh_token
    else:
        raise HTTPException(status_code=400, detail="Unknown token type")
    now = datetime.now(timezone.utc)
    expire_time = now + timedelta(minutes=expire_minutes)
    payload.update(
        exp=expire_time.timestamp(),
        iat=now.timestamp()
    )
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm
    )
    return encoded


def decode_jwt(token, public_key: str = os.getenv("PUBLIC_KEY"), algorithm: str = os.getenv("ALGORITHM")):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
        leeway=10
    )
    return uuid.UUID(decoded["sub"])
