import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, func

from app.models.models import ExperienceComponentCreate
from backend.app.api.deps import SessionDep, get_current_active_superuser, CurrentUser
from backend.app.models.models import Experience, ExperienceComponentsPublic, ExperienceComponentPublic, \
    ExperienceCreate, ExperienceComponent

router = APIRouter(prefix="/experience_components`", tags=["experience_components"])


@router.get("/{id}", response_model=ExperienceComponentPublic)
def get_experience_component(id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> Any:
    experience_component = session.get(ExperienceComponent, id)
    if not experience_component:
        raise HTTPException(status_code=404, detail="Experience Component not found")
    if not current_user.is_superuser and (experience_component.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to access this Experience Component")
    return experience_component


@router.get("/", response_model=ExperienceComponentsPublic)
def get_experience_components(session: SessionDep, current_user: CurrentUser, experience: Experience, limit: int = 100) -> Any:
    if current_user.is_superuser:
        count_statement = (
            select(func.count())
            .select_from(ExperienceComponent)
            .where(ExperienceComponent.experience_id == experience.id)
        )
        count = session.exec(count_statement).one()
        statement = select(ExperienceComponent).limit(limit)
        experience_components = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(ExperienceComponent)
            .where(ExperienceComponent.experience_id == experience.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(ExperienceComponent)
            .where(ExperienceComponent.experience_id == experience.id)
            .limit(limit)
        )
        experience_components = session.exec(statement).all()

    return ExperienceComponentsPublic(data=experience_components, count=count)


@router.post("/", response_model=ExperienceComponentPublic)
def create_experience_component(session: SessionDep, experience_components_in: ExperienceComponentCreate, current_user: CurrentUser) -> Any:
    experience_components = ExperienceComponent.model_validate(experience_components_in, update={"owner_id": current_user.id})
    session.add(experience_components)
    session.commit()
    session.refresh(experience_components)
    return experience_components


@router.delete("/{id}")
def delete_experience_component(id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> str:
    experience_components = session.get(ExperienceComponent, id)
    if not experience_components:
        raise HTTPException(status_code=404, detail="Experience Component not found")
    if not current_user.is_superuser and (experience_components.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to delete this experience_components")
    session.delete(experience_components)
    session.commit()
    return f"Experience Component: {id} deleted successfully"