from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine
from backend.app.api.main import api_router
from backend.app.core.config import settings
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)