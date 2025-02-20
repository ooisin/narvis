from fastapi import APIRouter

from backend.app.api.routes import narratives, users, login, experiences, experience_components, substories, sites, tours

from backend.app.core.config import settings

api_router = APIRouter()
api_router.include_router(narratives.router)
api_router.include_router(users.router)
api_router.include_router(login.router)
api_router.include_router(experiences.router)
api_router.include_router(experience_components.router)
api_router.include_router(substories.router)
api_router.include_router(sites.router)
api_router.include_router(tours.router)