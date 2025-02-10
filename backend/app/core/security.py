from passlib.context import CryptContext
import jwt
from typing import Any
from backend.app.core.config import settings
from datetime import datetime, timedelta, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_token(entity: str | Any, alive_time: timedelta) -> str:
    expire_time = datetime.now(timezone.utc) + alive_time
    encode_entity = {"exp": expire_time, "sub": str(entity)}
    encoded_token = jwt.encode(encode_entity, settings.SECRET_KEY, algorithm=settings.HASHING_ALGORITHM)
    return encoded_token


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)