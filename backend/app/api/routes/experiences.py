import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, func

from backend.app.api.deps import SessionDep, get_current_active_superuser, CurrentUser
from backend.app.crud import crud
from backend.app.models.models import ExperienceBase, Experience, ExperiencesPublic, ExperiencePublic, ExperienceCreate

router = APIRouter(prefix="/experiences", tags=["experiences"])


@router.get("/{id}", response_model=ExperiencePublic)
def get_experience(id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> Any:
    experience = session.get(Experience, id)
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    if not current_user.is_superuser and (experience.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to access this experience")
    return experience


@router.get("/", response_model=ExperiencesPublic)
def get_experiences(session: SessionDep, current_user: CurrentUser, limit: int = 100) -> Any:
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Experience)
        count = session.exec(count_statement).one()
        statement = select(Experience).limit(limit)
        experiences = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Experience)
            .where(Experience.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Experience)
            .where(Experience.owner_id == current_user.id)
            .limit(limit)
        )
        experiences = session.exec(statement).all()

    return ExperiencesPublic(data=experiences, count=count)


@router.post("/", response_model=ExperiencePublic)
def create_experience(session: SessionDep, experience_in: ExperienceCreate, current_user: CurrentUser) -> Any:
    experience = Experience.model_validate(experience_in, update={"owner_id": current_user.id})
    session.add(experience)
    session.commit()
    session.refresh(experience)
    return experience


@router.delete("/{id}")
def delete_experience(id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> str:
    experience = session.get(Experience, id)
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    if not current_user.is_superuser and (experience.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to delete this experience")
    session.delete(experience)
    session.commit()
    return f"Experience: {id} deleted successfully"