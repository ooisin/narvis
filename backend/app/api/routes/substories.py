import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, func

from backend.app.api.deps import SessionDep, get_current_active_superuser, CurrentUser
from backend.app.crud import crud
from backend.app.models.models import Substory, SubstoryBase, SubstoryPublic, SubstoriesPublic, SubstoryCreate

router = APIRouter(prefix="/substories", tags=["substories"])


@router.get("/{id}", response_model=SubstoryPublic)
def get_substory(id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> Any:
    substory = session.get(Substory, id)
    if not substory:
        raise HTTPException(status_code=404, detail="Substory not found")
    if not current_user.is_superuser and (substory.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to access this substory")
    return substory


@router.get("/", response_model=SubstoriesPublic)
def get_substories(session: SessionDep, current_user: CurrentUser, limit: int = 100) -> Any:
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Substory)
        count = session.exec(count_statement).one()
        statement = select(Substory).limit(limit)
        substories = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Substory)
            .where(Substory.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Substory)
            .where(Substory.owner_id == current_user.id)
            .limit(limit)
        )
        substories = session.exec(statement).all()

    return SubstoriesPublic(data=substories, count=count)


@router.post("/", response_model=SubstoryPublic)
def create_substory(session: SessionDep, substory_in: SubstoryCreate, current_user: CurrentUser) -> Any:
    substory = Substory.model_validate(substory_in, update={"owner_id": current_user.id})
    session.add(substory)
    session.commit()
    session.refresh(substory)
    return substory


@router.delete("/{id}")
def delete_substory(id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> str:
    substory = session.get(Substory, id)
    if not substory:
        raise HTTPException(status_code=404, detail="Substory not found")
    if not current_user.is_superuser and (substory.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to delete this substory")
    session.delete(substory)
    session.commit()
    return f"Substory: {id} deleted successfully"