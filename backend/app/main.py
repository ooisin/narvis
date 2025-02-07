from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine
from backend.app.api.main import api_router
app = FastAPI()

# TODO: Initial routing generation and CORS stuff
app.include_router(api_router)