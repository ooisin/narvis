import secrets
import os
from typing import Self

from pydantic import computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl

# TODO: Pain in the arse - will need to be fixed but later issue...
env_file_path = '/home/koro/PycharmProjects/narvis/.env'
if os.path.exists(env_file_path):
    print(f".env file found at: {os.path.abspath(env_file_path)}")
    with open(env_file_path, 'r') as f:
        first_line = f.readline().strip()
        print(f"First line of .env: {first_line}")
else:
    print(f".env file not found sat: {os.path.abspath(env_file_path)}")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_file_path,
        env_ignore_empty=True,
        extra="ignore"
    )

    SECRET_KEY: str = secrets.token_urlsafe(32)
    HASHING_ALGORITHM: str = "HS256" # TODO: Should this be abstracted?
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7
    FRONTEND_HOST: str = "http://localhost:3000"
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    PROJECT_NAME: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""


    @computed_field
    @property
    def DATABASE_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()