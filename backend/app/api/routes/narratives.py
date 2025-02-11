import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from backend.app.api.deps import SessionDep, CurrentUser
from backend.app.models.models import Narrative, NarrativesPublic, NarrativePublic, NarrativeCreate

router = APIRouter(prefix="/narratives", tags=["narratives"])


@router.get("/", response_model=NarrativesPublic)
def read_narratives(session: SessionDep, current_user: CurrentUser, limit: int = 100) -> Any:

    if current_user.is_superuser:
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
def read_narrative(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:

    item = session.get(Narrative, id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Narrative with id {id} not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to access this narrative")
    return item


@router.post("/", response_model=NarrativePublic)
def create_item(*, session: SessionDep, current_user: CurrentUser, narrative_in: NarrativeCreate) -> Any:

    narrative = Narrative.model_validate(narrative_in, update={"owner_id": current_user.id})
    session.add(narrative)
    session.commit()
    session.refresh(narrative)
    return narrative



