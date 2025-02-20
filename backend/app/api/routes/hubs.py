import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from backend.app.api.deps import SessionDep, CurrentUser
from backend.app.models.models import Hub, HubCreate, HubsPublic, HubPublic

router = APIRouter(prefix="/hubs", tags=["hubs"])


@router.get("/", response_model=HubsPublic)
def get_hubs(session: SessionDep, current_user: CurrentUser, limit: int = 100) -> Any:
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Hub)
        count = session.exec(count_statement).one()
        statement = select(Hub).limit(limit)
        hubs = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Hub)
            .where(Hub.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Hub)
            .where(Hub.owner_id == current_user.id)
            .limit(limit)
        )
        hubs = session.exec(statement).all()

    return HubsPublic(data=hubs, count=count)


@router.get("/{id}", response_model=HubPublic)
def get_hub(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    hub = session.get(Hub, id)
    if not hub:
        raise HTTPException(status_code=404, detail="Hub not found")
    if not current_user.is_superuser and (hub.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to access this hub")


@router.post("/", response_model=HubPublic)
def create_hub(session: SessionDep, hub_in: HubCreate, current_user: CurrentUser) -> Any:
    hub = Hub.model_validate(hub_in, update={"owner_id": current_user.id})
    session.add(hub)
    session.commit()
    session.refresh(hub)
    return hub


@router.delete("/{id}")
def delete_hub(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> str:
    hub = session.get(Hub, id)
    if not hub:
        raise HTTPException(status_code=404, detail="Hub not found")
    if not current_user.is_superuser and (hub.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to delete this hub")
    session.delete(hub)