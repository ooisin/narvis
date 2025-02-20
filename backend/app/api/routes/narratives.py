import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from backend.app.api.deps import SessionDep, CurrentUser
from backend.app.models.models import Narrative, NarrativesPublic, NarrativePublic, NarrativeCreate

router = APIRouter(prefix="/narratives", tags=["narratives"])


@router.get("/", response_model=NarrativesPublic)
def get_narratives(session: SessionDep, current_user: CurrentUser, limit: int = 100) -> Any:

    if current_user.is_superuser:
        # TODO: Abstract this logic to a crud method!
        # Needs error handling etc
        count_statement = select(func.count()).select_from(Narrative)
        count = session.exec(count_statement).one()
        statement = select(Narrative).limit(limit)
        narratives = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Narrative)
            .where(Narrative.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Narrative)
            .where(Narrative.owner_id == current_user.id)
            .limit(limit)
        )
        narratives = session.exec(statement).all()

    return NarrativesPublic(data=narratives, count=count)


@router.get("/{id}", response_model=NarrativePublic)
def get_narrative(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:

    narrative = session.get(Narrative, id)
    if not narrative:
        raise HTTPException(status_code=404, detail=f"Narrative with id {id} not found")
    if not current_user.is_superuser and (narrative.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to access this narrative")
    return narrative


@router.post("/", response_model=NarrativePublic)
def create_narrative(session: SessionDep, current_user: CurrentUser, narrative_in: NarrativeCreate) -> Any:
    narrative = Narrative.model_validate(narrative_in, update={"owner_id": current_user.id})
    session.add(narrative)
    session.commit()
    session.refresh(narrative)
    return narrative


@router.delete("/{id}")
def delete_narrative(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> str:
    narrative = session.get(Narrative, id)
    if not narrative:
        raise HTTPException(status_code=404, detail=f"Narrative with id {id} not found")
    if not current_user.is_superuser and (narrative.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to delete this narrative")
    session.delete(narrative)
    session.commit()
    return f"Narrative: {id} deleted successfully"



