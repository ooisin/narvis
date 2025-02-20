import shutil
from typing import Optional

from fastapi import HTTPException, UploadFile, File
from sqlmodel import select, Session

from backend.app.models.models import Narrative, ExperienceComponent
from backend.app.models.models import UserCreate, User
from backend.app.core.security import get_password_hash, verify_password


# TODO: Possibly split crud.py into specific files for User, Narrative ... operations

""" USER """
def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def authenticate_user(session: Session, email: str, passwd: str) -> Optional[User]:
    check_user = get_user_by_email(session, email)
    if not check_user:
        return None
    if not verify_password(passwd, check_user.hashed_password):
        return None
    return check_user


def create_db_user(session: Session, user_create: UserCreate ) -> User:
    new_user = User.model_validate(user_create, update={"hashed_password": get_password_hash(user_create.password)})
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user



def read_components(session: Session):
    statement = select(ExperienceComponent)
    return session.exec(statement).all()


def read_component(component_id: int, session: Session):
    statement = select(ExperienceComponent).where(ExperienceComponent.id == component_id)
    return session.exec(statement).first()


# Try logic should be handled at the service/api/route level
def create_component(component: ExperienceComponent, session: Session):
    try:
        session.add(component)
        session.commit()
        session.refresh(component)
        return component
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to insert component: {str(e)}")


def update_component(component_id: int, updated_component: ExperienceComponent, session: Session):
    try:
        statement = select(ExperienceComponent).where(ExperienceComponent.id == component_id)
        component = session.exec(statement).first()
        if component is None:
            raise HTTPException(status_code=404, detail=f"Component with id {component_id} not found")
        for k, v in updated_component.model_dump(exclude_unset=True).items():
            setattr(component, k, v)
        session.add(component)
        session.commit()
        session.refresh(component)
        return component
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update component: {str(e)}")


def delete_component(component_id: int, session: Session):
    try:
        session.delete(component_id)
        session.commit()
        session.refresh(component_id)
        return {"ok - component deleted successfully": True}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete component: {str(e)}")


def get_narratives(session: Session):
    statement = select(Narrative)
    return session.exec(statement).all()


def get_narrative_by_id(narrative_id: int, session: Session):
    statement = select(Narrative).where(Narrative.id == narrative_id)
    return session.exec(statement).first()


def create_narrative(narrative: Narrative, session: Session):
    session.add(narrative)
    session.commit()
    session.refresh(narrative)
    return narrative


def update_narrative(narrative_id: int, updated_narrative: Narrative, session: Session):
    try:
        statement = select(Narrative).where(Narrative.id == narrative_id)
        narrative = session.exec(statement).first()
        if narrative is None:
            raise HTTPException(status_code=404, detail=f"Narrative with id {narrative_id} not found")
        for k, v in updated_narrative.model_dump(exclude_unset=True).items():
            setattr(narrative, k, v)
        session.add(narrative)
        session.commit()
        session.refresh(narrative)
        return narrative
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update narrative: {str(e)}")


def delete_narrative(narrative_id: int, session: Session) -> None:
    narrative = session.get(Narrative, narrative_id)
    if not narrative:
        raise ValueError(f"Narrative with ID {narrative_id} not found")
    session.delete(narrative)
    session.commit()



# Rudimentary file upload method for initial development using Swagger UI docs
async def upload_file(file: UploadFile = File(...)):
    file_path = f"backend/test_uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}