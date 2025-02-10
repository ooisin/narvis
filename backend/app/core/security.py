from passlib.context import CryptContext
import jwt
from typing import Any
from backend.app.core.config import settings
from datetime import datetime, timedelta, timezone


def generate_token(entity: str | Any, expires_delta: timedelta) -> str:
    pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pass


def get_password_hash(password: str) -> str:
    pass