import secrets

from pydantic import computed_field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_ignore_empty=True,
        extra="ignore"
    )

    SECRET_KEY: str = secrets.token_urlsafe(32)
    HASHING_ALGORITHM: str = "HS256" # TODO: Should this be abstracted?
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7
    FRONTEND_HOST: str = "http://localhost:5173"

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
            path=self.POSTGRES_DB, # f"/{self.POSTGRES_DB}"
        )

try:
    settings = Settings()
except ValidationError as e:
    print(f"Settings config error: {str(e)}")