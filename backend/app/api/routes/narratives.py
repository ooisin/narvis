import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.exceptions import ValidationException
from sqlmodel import func, select

from backend.app.api.deps import SessionDep
from backend.app.crud import get_narrative_by_id, get_narratives, delete_narrative, create_narrative
from backend.app.models import Narrative

router = APIRouter(prefix="/narratives", tags=["narratives"])


@router.get("/", response_model=list[Narrative])
def read_narratives(session: SessionDep) -> Any:
    try:
        narratives = get_narratives(session=session)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error getting narratives: {str(e)}")
    return narratives

# TODO: Need to add current user logic
@router.get("/{narrative_id}", response_model=Narrative)
def read_narrative(narrative_id: int, session: SessionDep) -> Any:
    narrative = get_narrative_by_id(session=session, narrative_id=narrative_id)
    if not narrative:
        raise HTTPException(status_code=404, detail="Narrative not found")
    # User can only access thUse own created narratives - admin can oversee/query all
    return narrative


@router.post("/", response_model=Narrative)
def new_narrative(narrative: Narrative, session: SessionDep) -> Any:
    try:
        narrative = Narrative.model_validate(narrative) # Add the user id
        create_narrative(narrative=narrative, session=session)
    except ValidationException as e:
        raise HTTPException(status_code=422, detail=f"Error validating narrative: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating narrative: {str(e)}")
    return narrative


@router.delete("/{narrative_id}", response_model=Narrative)
def remove_narrative(narrative_id: int, session: SessionDep) -> Any:
    narrative = get_narrative_by_id(session=session, narrative_id=narrative_id)
    if not narrative:
        raise HTTPException(status_code=404, detail="Narrative not found")
    try:
        delete_narrative(narrative_id=narrative_id, session=session)
        return narrative
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"Narrative with ID {narrative_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting narrative: {str(e)}")




