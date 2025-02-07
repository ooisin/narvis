from fastapi import APIRouter

from backend.app.api.routes import narratives

from backend.app.core import settings

api_router = APIRouter()
api_router.include_router(narratives.router)


