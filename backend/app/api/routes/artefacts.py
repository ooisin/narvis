import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, func

from backend.app.api.deps import SessionDep, get_current_active_superuser, CurrentUser
from backend.app.crud import crud
from backend.app.models.models import Artefact, ArtefactCreate, ArtefactsPublic, ArtefactPublic

router = APIRouter(prefix="/artefacts", tags=["artefacts"])


@router.get("/{id}", response_model=ArtefactPublic)
def get_artefact(id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> Any:
    artefact = session.get(Artefact, id)
    if not artefact:
        raise HTTPException(status_code=404, detail="Artefact not found")
    if not current_user.is_superuser and (artefact.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to access this artefact")
    return artefact


@router.get("/", response_model=ArtefactsPublic)
def get_artefacts(session: SessionDep, current_user: CurrentUser, limit: int = 100) -> Any:
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Artefact)
        count = session.exec(count_statement).one()
        statement = select(Artefact).limit(limit)
        artefacts = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Artefact)
            .where(Artefact.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Artefact)
            .where(Artefact.owner_id == current_user.id)
            .limit(limit)
        )
        artefacts = session.exec(statement).all()

    return ArtefactsPublic(data=artefacts, count=count)


@router.post("/", response_model=ArtefactPublic)
def create_artefact(session: SessionDep, artefact_in: ArtefactCreate, current_user: CurrentUser) -> Any:
    artefact = Artefact.model_validate(artefact_in, update={"owner_id": current_user.id})
    session.add(artefact)
    session.commit()
    session.refresh(artefact)
    return artefact


@router.delete("/{id}")
def delete_artefact(id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> str:
    artefact = session.get(Artefact, id)
    if not artefact:
        raise HTTPException(status_code=404, detail="Artefact not found")
    if not current_user.is_superuser and (artefact.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to delete this artefact")
    session.delete(artefact)
    session.commit()
    return f"Artefact: {id} deleted successfully"