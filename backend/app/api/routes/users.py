import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, func

from backend.app.api.deps import SessionDep, get_current_active_superuser, CurrentUser
from backend.app.crud import crud
from backend.app.models.models import User, UserPublic, UserCreate, UserRegister, UsersPublic

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserPublic, dependencies=[Depends(get_current_active_superuser)])
def create_user(session: SessionDep, user_new: UserCreate) -> Any:
    user = crud.get_user_by_email(session=session, email=user_new.email)
    if user:
        raise HTTPException(status_code=400, detail=f"User with email {user.email} already exists")

    user = crud.create_user(session=session, user_create=user_new)

    # TODO: Add some email verification that account has been created

    return user


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    return current_user


@router.post("/register", response_model=UserPublic)
def register_user(session: SessionDep, user_new: UserRegister) -> Any:
    user = crud.get_user_by_email(session=session, email=user_new.email)
    if user:
        raise HTTPException(status_code=400, detail=f"User with email {user.email} already exists")

    user_create = UserCreate.model_validate(user_new)
    user = crud.create_user(session=session, user_create=user_create)
    return user


@router.get("/{user_id}", response_model=UserPublic)
def get_user_by_id(id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> Any:
    user = session.get(User, id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The current user is not superuser - permission denied")
    return user


@router.get("/", dependencies=[Depends(get_current_active_superuser)], response_model=UsersPublic)
def read_users(session: SessionDep) -> Any:
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()

    statement = select(User).limit(100) # could parameterise this later stages
    users = session.exec(statement).all()

    return UsersPublic(data=users, count=count)