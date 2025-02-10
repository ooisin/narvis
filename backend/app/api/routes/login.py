from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.crud import crud
from backend.app.api.deps import CurrentUser, SessionDep
from backend.app.core import security
from backend.app.core.config import settings
from backend.app.models.models import Token, UserPublic


router = APIRouter(prefix="/login", tags=["login"])


@router.post("/access-token")
def login_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = crud.authenticate_user(session=session, email=form_data.username, passwd=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Authentication failed - invalid credentials")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    token_ttl = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    return Token(access_token=security.generate_token(user.id, alive_time=token_ttl))


@router.post("/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    return current_user