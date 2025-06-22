import os
import uuid
from datetime import datetime, timezone, timedelta
import jwt


def encode_jwt(
        payload: dict,
        private_key: str = os.getenv("PRIVATE_KEY"),
        algorithm: str = os.getenv("ALGORITHM"),
        expire_minutes: int = 15):
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
